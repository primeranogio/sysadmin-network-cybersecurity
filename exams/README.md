# Demone 
## Regole per gli Script Python CLI
Pipelining degli errori (```sys.stderr```):
I messaggi di errore vanno stampati specificando ```file=sys.stderr```. In questo modo le utility Unix e ```systemd``` possono separare gli output standard dagli errori.

Codici di Uscita (```sys.exit(1)```):
Uscire con codice non nullo (```!= 0```) notifica al sistema o a systemd che l'esecuzione è fallita (attivando ad esempio le regole di ```Restart=on-failure```).

Gestione File in Append (```open(path, "a")```):
Sempre usare la modalità ```"a"``` per i file di log per evitare l'azzeramento del contenuto a ogni scrittura.
## Regole per i Servizi Systemd Utente (systemd --user)
Percorso dei file di servizio:
I servizi creati a livello utente (senza privilegi ```root```) vanno posizionati sempre in:
```~/.config/systemd/user/<nome_servizio>.service```

Gli Specifier di Systemd (Variabili Utili):
- ```%h```: Rappresenta la Home Directory dell'utente (equivalente a ```$HOME``` o ```~```).
- ```%u```: Nome dell'utente.

La variabile ```PYTHONUNBUFFERED=1```:
Di default Python mantiene i messaggi di ```print()``` in memoria buffer prima di scriverli su disco/terminale. Nei servizi in background, ```PYTHONUNBUFFERED=1``` forza la scrittura immediata nel journal di systemd (```journalctl```).

Comandi di Gestione da Memorizzare:
```
# Ricarica la configurazione se modifichi il file .service
systemctl --user daemon-reload

# Abilita l'avvio automatico del servizio
systemctl --user enable dir-size-monitor.service

# Avvia il servizio
systemctl --user start dir-size-monitor.service

# Controlla lo stato e legge gli ultimi print/log dello script
systemctl --user status dir-size-monitor.service
```

## ESEMPIO:
```
# path: $HOME/dir-size-monitor/app.py

import argparse
from datetime import datetime
import os
import sys
import time

# -------------------------------------------------------------------
# FUNZIONE RICORSIVA PER IL CALCOLO DELLA DIMENSIONE
# -------------------------------------------------------------------
def get_total_size(target_dir):
    total_size = 0
    # Scansiona tutti i file e cartelle contenuti in target_dir
    for filename in os.listdir(target_dir):
        path = os.path.join(target_dir, filename)
        
        # Se è un file normale, sommo la sua dimensione in byte
        if os.path.isfile(path):
            total_size += os.path.getsize(path)
        # Se è una sottodirectory, richiamo ricorsivamente la funzione
        elif os.path.isdir(path):
            total_size += get_total_size(path)
            
    return total_size


def main():
    # -------------------------------------------------------------------
    # 1. PARSING DEGLI ARGOMENTI
    # -------------------------------------------------------------------
    parser = argparse.ArgumentParser(description="dir size monitor")
    
    parser.add_argument(
        "--target", type=str, required=True, 
        help="absolute path to the directory to monitor"
    )
    parser.add_argument(
        "--threshold", type=int, required=True, 
        help="size threshold in bytes"
    )
    parser.add_argument(
        "--interval", type=int, required=True, 
        help="interval in seconds between checks"
    )
    parser.add_argument(
        "--log", type=str, required=True, 
        help="directory where to save the log file"
    )
    
    args = parser.parse_args()

    # -------------------------------------------------------------------
    # 2. VALIDAZIONE RIGIDA DEGLI INPUT
    # -------------------------------------------------------------------
    # Controlli per --target (deve essere assoluto, esistere ed essere una directory)
    if not os.path.isabs(args.target):
        print(f"error: {args.target} is not an absolute path", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(args.target):
        print(f"error: {args.target} does not exist", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(args.target):
        print(f"error: {args.target} is not a directory", file=sys.stderr)
        sys.exit(1)

    # Controlli sui valori numerici (devono essere interi positivi)
    if args.threshold <= 0:
        print(f"error: --threshold must be a positive integer", file=sys.stderr)
        sys.exit(1)
    if args.interval <= 0:
        print(f"error: --interval must be a positive integer", file=sys.stderr)
        sys.exit(1)

    # Controlli per --log (deve essere assoluto, esistere ed essere una directory)
    if not os.path.isabs(args.log):
        print(f"error: {args.log} is not an absolute path", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(args.log):
        print(f"error: {args.log} does not exist", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(args.log):
        print(f"error: {args.log} is not a directory", file=sys.stderr)
        sys.exit(1)

    # Definisce il percorso completo del file di log
    log_path = os.path.join(args.log, "dir-size-monitor.log")

    # -------------------------------------------------------------------
    # 3. CICLO DI MONITORAGGIO INFINITO (DEMONE)
    # -------------------------------------------------------------------
    while True:
        total_size = get_total_size(args.target)
        
        # Se la dimensione calcolata supera la soglia, scrive nel file di log
        if total_size > args.threshold:
            # Modalità "a" (append) per non sovrascrivere i log precedenti
            with open(log_path, "a") as log_file:
                log_file.write(f"{datetime.now()} {total_size}\n")
            print(f"total size {total_size} bytes exceeds threshold {args.threshold}")
            
        # Attende l'intervallo specificato prima del controllo successivo
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
```

```
# path: ~/.config/systemd/user/dir-size-monitor.service

[Unit]
Description=dir size monitor service

[Service]
# Disabilita il buffering dell'output di Python per vedere i print subito nei log di systemd
Environment=PYTHONUNBUFFERED=1

# Imposta la directory di lavoro in cui cercare lo script
WorkingDirectory=%h/dir-size-monitor

# Comando da eseguire (%h viene sostituito automaticamente con la home dell'utente, es. /home/username)
ExecStart=/usr/bin/python3 app.py --target %h/documents --threshold 1000 --interval 60 --log %h

# Politica di riavvio: riavvia automaticamente il servizio se crolla (exit code != 0)
Restart=on-failure

# Attende 5 secondi prima di tentare il riavvio
RestartSec=5

[Install]
# Assicura che il servizio parte automaticamente all'avvio della sessione utente
WantedBy=default.target
```

# Processo periodico
## Regole Fondamentali sui Timer Systemd
Abbinamento Nomi (Naming Convention):
Se il timer e il service hanno lo stesso identico nome base (es. ```extension-sorter.timer``` e ```extension-sorter.service```), la riga ```Unit=extension-sorter.service``` nel file ```.timer``` è facoltativa ma è ottima prassi scriverla esplicitamente.

Sintassi di ```OnCalendar```:
- Giorni della settimana: ```Mon```, ```Tue```, ```Wed```, ```Thu```, ```Fri```, ```Sat```, ```Sun``` (es. ```Wed,Sat```).
- Format data/ora: ```GiornoDellaSettimana AAAA-MM-GG HH:MM:SS```
- Joker / Wildcards (```*```): Usare ```*-*-*``` significa "qualsiasi anno, qualsiasi mese, qualsiasi giorno" (valido se si specificano solo i giorni della settimana o l'orario).
- Esempi Utili da Memorizzare:
    - ```*-*-* 00:00:00``` -> Ogni giorno a mezzanotte.
    - ```Mon *-*-* 08:00:00``` -> Ogni lunedì mattina alle 08:00.
    - ```*-*-01 04:00:00``` -> Il primo giorno di ogni mese alle 04:00.
 
Comandi per Abilitare un Timer Utente:
Per mettere in funzione un timer non basta abilitare il servizio, occorre gestire il timer:
```
# Ricarica le unità
systemctl --user daemon-reload

# Abilita ed avvia il TIMER (non il servizio)
systemctl --user enable extension-sorter.timer
systemctl --user start extension-sorter.timer

# Verifica la lista dei timer attivi e la prossima esecuzione
systemctl --user list-timers
```

## ESEMPIO:
```
# path: ~/extension-sorter/app.py

import argparse
from datetime import datetime
import os
import shutil
import sys

# -------------------------------------------------------------------
# FUNZIONE RICORSIVA DI SCANSIONE E SPOSTAMENTO
# -------------------------------------------------------------------
def walk(target_dir, dest_dir, extensions, log_path):
    # Elenca il contenuto della directory corrente
    for filename in os.listdir(target_dir):
        path = os.path.join(target_dir, filename)
        
        # Se è un file normale
        if os.path.isfile(path):
            for extension in extensions:
                # Controlla se il file termina con l'estensione richiesta (es. .pdf)
                if filename.endswith(f".{extension}"):
                    target_subdir = os.path.join(dest_dir, extension)
                    
                    # Sposta il file nella sottocartella dedicata (es. ~/sorted/pdf)
                    shutil.move(path, target_subdir)
                    
                    # Traccia lo spostamento nel file di log (modalità append "a")
                    with open(log_path, "a") as log_file:
                        log_file.write(f"{datetime.now()} {path} {target_subdir}\n")
                        
        # Se è una directory, invoca ricorsivamente la funzione per esplorarla
        elif os.path.isdir(path):
            walk(path, dest_dir, extensions, log_path)


def main():
    # -------------------------------------------------------------------
    # 1. PARSING DEGLI ARGOMENTI CLI
    # -------------------------------------------------------------------
    parser = argparse.ArgumentParser(description="extension sorter")
    
    parser.add_argument(
        "--path", type=str, required=True, 
        help="absolute path of the directory to scan"
    )
    parser.add_argument(
        "--dest", type=str, required=True, 
        help="absolute path of the destination directory"
    )
    parser.add_argument(
        "--extensions", type=str, required=True, 
        help="comma-separated extensions to monitor"
    )
    parser.add_argument(
        "--log", type=str, required=True, 
        help="absolute path of the log file"
    )
    
    args = parser.parse_args()

    # -------------------------------------------------------------------
    # 2. VALIDAZIONE DEGLI INPUT
    # -------------------------------------------------------------------
    # Controlli per --path (directory sorgente)
    if not os.path.isabs(args.path):
        print(f"error: {args.path} is not an absolute path", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(args.path):
        print(f"error: {args.path} does not exist", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(args.path):
        print(f"error: {args.path} is not a directory", file=sys.stderr)
        sys.exit(1)

    # Controlli per --dest (directory destinazione)
    if not os.path.isabs(args.dest):
        print(f"error: {args.dest} is not an absolute path", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(args.dest):
        print(f"error: {args.dest} does not exist", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(args.dest):
        print(f"error: {args.dest} is not a directory", file=sys.stderr)
        sys.exit(1)

    # Parsing e validazione della lista di estensioni
    extensions = args.extensions.split(",")
    for extension in extensions:
        if not extension:  # Se l'estensione è vuota (es. "pdf,,txt")
            print("error: empty extension", file=sys.stderr)
            sys.exit(1)

    # Controllo per --log (deve essere un percorso assoluto)
    if not os.path.isabs(args.log):
        print(f"error: {args.log} is not an absolute path", file=sys.stderr)
        sys.exit(1)

    # -------------------------------------------------------------------
    # 3. PREPARAZIONE DELLE DIRECTORY ED ESECUZIONE
    # -------------------------------------------------------------------
    # Crea la directory genitrice del file di log se non esiste
    os.makedirs(os.path.dirname(args.log), exist_ok=True)
    
    # Crea le sottocartelle di destinazione per ogni estensione (es. ~/sorted/pdf, ~/sorted/txt)
    for extension in extensions:
        os.makedirs(os.path.join(args.dest, extension), exist_ok=True)
        
    # Avvia la scansione e lo spostamento
    walk(args.path, args.dest, extensions, args.log)


if __name__ == "__main__":
    main()
```

```
# path: ~/.config/systemd/user/extension-sorter.service

[Unit]
Description=extension sorter service

[Service]
# Disabilita il buffering dell'output per scrivere subito nei log di systemd
Environment=PYTHONUNBUFFERED=1

# Directory di lavoro
WorkingDirectory=%h/extension-sorter

# Comando da eseguire con tutti i parametri richiesti
ExecStart=/usr/bin/python3 app.py --path %h/inbox --dest %h/sorted --extensions pdf,txt --log %h/extension-sorter.log

# Nota: Non serve la sezione [Install] qui, perché l'avvio è gestito dal TIMER!
```

```
# path: ~/.config/systemd/user/extension-sorter.timer

[Unit]
Description=extension sorter timer

[Timer]
# Specifica quale unità .service attivare allo scoccare del timer
Unit=extension-sorter.service

# Calendario: Mercoledì (Wed) e Sabato (Sat) alle 05:30:00 ( *-*-* indica ogni anno/mese/giorno )
OnCalendar=Wed,Sat *-*-* 05:30

[Install]
# Assicura che il timer sia attivo all'avvio dell'ambiente utente
WantedBy=timers.target
```

# Filtraggio dei pacchetti e NAT
## Ogni comando **iptables** segue una struttura ben precisa:
**iptables** [-t tabella] -A/D/I catena [criteri di match] -j azione

Tabella (```-t```): Specifica la tabella. Se omessa, la tabella predefinita è ```filter```. Le più usate sono ```filter``` e ```nat```.

Comando (```-A```, ```-P```, ```-F```):
- ```-A``` (Append): Aggiunge una regola in fondo alla catena.
- ```-P``` (Policy): Imposta la politica di default della catena (es. ```DROP``` o ```ACCEPT```).
- ```-F``` (Flush): Cancella tutte le regole della tabella.

Catena: Indica il momento/punto in cui il pacchetto viene esaminato (```INPUT```, ```OUTPUT```, ```FORWARD```, ```PREROUTING```, ```POSTROUTING```).

Azione (```-j``` / Jump): Specifica cosa fare con il pacchetto se soddisfa i criteri (```ACCEPT```, ```DROP```, ```REJECT```, ```DNAT```, ```SNAT```, ```MASQUERADE```).

## ESEMPIO:
```
# path/identificazione studente

# -------------------------------------------------------------------
# 1. PULIZIA DELLE REGOLE ESISTENTI (Flush)
# -------------------------------------------------------------------
# Elimina tutte le regole esistenti dalla tabella di default (filter)
-F

# Elimina tutte le regole esistenti dalla tabella NAT
-t nat -F


# -------------------------------------------------------------------
# 2. POLITICHE DI DEFAULT (Default Policies - Whitelisting)
# -------------------------------------------------------------------
# Scarta (DROP) di default tutto il traffico in ingresso diretto al firewall stesso
-P INPUT DROP

# Scarta (DROP) di default tutto il traffico in transito (da una rete all'altra)
-P FORWARD DROP


# -------------------------------------------------------------------
# 3. REGOLE PER LA CATENA INPUT (Traffico DIRETTO AL FIREWALL)
# -------------------------------------------------------------------
# Accetta pacchetti ICMP (ping) se provengono dalla rete interna (eth1)
-A INPUT -i eth1 -p icmp -j ACCEPT

# Accetta connessioni SSH (TCP porta 22) per la gestione remota, ma solo da eth1 (rete interna)
-A INPUT -i eth1 -p tcp --dport 22 -j ACCEPT


# -------------------------------------------------------------------
# 4. REGOLE PER LA CATENA FORWARD (Traffico IN TRANSITO)
# -------------------------------------------------------------------
# Consenti il traffico HTTP (80) e HTTPS (443) che entra da eth0 o eth1
-A FORWARD -i eth0 -p tcp --dport 80 -j ACCEPT
-A FORWARD -i eth0 -p tcp --dport 443 -j ACCEPT
-A FORWARD -i eth1 -p tcp --dport 80 -j ACCEPT
-A FORWARD -i eth1 -p tcp --dport 443 -j ACCEPT

# Stateful Inspection: Consenti il passaggio di tutti i pacchetti appartenenti
# a connessioni già stabilite (ESTABLISHED) o correlate (RELATED)
-A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT


# -------------------------------------------------------------------
# 5. MASQUERADE / SNAT (Navigazione da LAN a Internet)
# -------------------------------------------------------------------
# Modifica l'IP sorgente dei pacchetti in uscita su eth0 (verso Internet)
# usando l'IP pubblico del firewall, permettendo alla LAN di navigare
-t nat -A POSTROUTING -o eth0 -j MASQUERADE


# -------------------------------------------------------------------
# 6. PORT FORWARDING / DNAT (Server Web Interno su 10.20.30.100)
# -------------------------------------------------------------------
# Port Forwarding HTTP: Reindirizza il traffico in arrivo su eth0:80 verso 10.20.30.100:8080
-t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j DNAT --to-destination 10.20.30.100:8080

# Permette l'attraversamento del firewall per il traffico reindirizzato alla porta 8080
-A FORWARD -i eth0 -o eth1 -p tcp -d 10.20.30.100 --dport 8080 -j ACCEPT

# Port Forwarding HTTPS: Reindirizza il traffico in arrivo su eth0:443 verso 10.20.30.100:8443
-t nat -A PREROUTING -i eth0 -p tcp --dport 443 -j DNAT --to-destination 10.20.30.100:8443

# Permette l'attraversamento del firewall per il traffico reindirizzato alla porta 8443
-A FORWARD -i eth0 -o eth1 -p tcp -d 10.20.30.100 --dport 8443 -j ACCEPT
```

# Amministrazione degli account
## Sintassi standard di una regola in **sudo**:
**Chi** (Utente/Gruppo) **Dove** (Host) = (*Come chi* (Utente RunAs)) [Opzioni] **Cosa** (Comandi)

```%```: Un prefisso ```%``` indica un gruppo del sistema operativo (es. ```%acct```).

```NOPASSWD:```: Consente di eseguire il comando senza inserire la password.

```(ALL)``` o ```(utente)```: Definisce l'utente target sotto le cui spoglie eseguire il comando. Se omesso, di default ```sudo``` assume ```(root)```.

## ESEMPIO:
```
# path: /etc/sudoers.d/site

# -------------------------------------------------------------------
# ALIAS PER HOST
# Raggruppano specifici server della rete sotto un unico nome
# -------------------------------------------------------------------
Host_Alias  WEB = web01, web02, web03
Host_Alias  DB  = db01, db02

# -------------------------------------------------------------------
# ALIAS PER COMANDI
# Raggruppano percorsi assoluti di file eseguibili
# -------------------------------------------------------------------
Cmnd_Alias  FWTOOLS = /usr/sbin/iptables, /usr/bin/tcpdump
Cmnd_Alias  ACCTMGM = /usr/sbin/useradd, /usr/sbin/usermod
Cmnd_Alias  PKGMGM  = /usr/bin/apt, /usr/bin/dpkg

# -------------------------------------------------------------------
# REGOLE DI PERMESSO
# -------------------------------------------------------------------

# alma può eseguire qualsiasi comando (ALL) come qualsiasi utente (ALL) su qualsiasi host (ALL)
alma        ALL  = (ALL) ALL

# bruno può eseguire qualsiasi comando come qualsiasi utente su tutti gli host,
# ad eccezione dei comandi definiti in FWTOOLS
bruno       ALL  = (ALL) ALL, !FWTOOLS

# I membri del gruppo 'acct' possono eseguire i comandi di gestione account (ACCTMGM)
# come root sui soli host del gruppo WEB
%acct       WEB  = ACCTMGM

# I membri del gruppo 'pkg' possono eseguire i comandi di gestione pacchetti (PKGMGM)
# come root sui soli host del gruppo DB, senza inserire la password
%pkg        DB   = NOPASSWD: PKGMGM

# cleo può leggere il file /etc/gshadow tramite cat come root su tutti gli host,
# senza inserire la password
cleo        ALL  = NOPASSWD: /usr/bin/cat /etc/gshadow

# dario può eseguire il comando 'id' specificatamente come utente 'elin' solo sul server db01
dario       db01 = (elin) /usr/bin/id

# I membri dei gruppi 'net' e 'pkg' possono eseguire il comando 'ip'
# come root su tutti gli host, senza inserire la password
%net, %pkg  ALL  = NOPASSWD: /usr/sbin/ip
```
