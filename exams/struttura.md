# SCHEDA D'ESAME
## Python · systemd · sudoers · iptables

---

# 0\. METODO UNIVERSALE

Quando leggi una traccia:

```
TRACCIA
   ↓
QUAL È LA FAMIGLIA?
   ↓
QUAL È LO SCHELETRO?
   ↓
QUALI PARAMETRI CAMBIANO?
   ↓
VALIDAZIONE
   ↓
IMPLEMENTAZIONE
   ↓
CONTROLLO DEGLI ERRORI
```

## Mappa immediata

| La traccia parla di... | Pensa a... |
| --- | --- |
| directory / sottodirectory | ricorsione |
| file dentro directory | `os.listdir()` |
| percorso completo | `os.path.join()` |
| distinguere file/directory | `isfile()` / `isdir()` |
| cercare contenuto | lettura file |
| spostare file | `shutil.move()` |
| dimensione directory | ricorsione + `getsize()` |
| programma sempre attivo | `while True` |
| ogni N secondi | `sleep()` |
| ogni giorno/lunedì/alle 03:00 | systemd timer |
| programma eseguito una volta | service/timer |
| utenti/gruppi sudo | sudoers |
| gruppi di host | `Host_Alias` |
| gruppi di comandi | `Cmnd_Alias` |
| senza password | `NOPASSWD` |
| eseguire come altro utente | `(utente)` |
| traffico verso firewall | `INPUT` |
| traffico attraverso firewall | `FORWARD` |
| modifica destinazione | `DNAT` |
| modifica sorgente | `SNAT` / `MASQUERADE` |
| traffico di ritorno | `ESTABLISHED,RELATED` |
| NAT in uscita | `POSTROUTING` |
| NAT in ingresso | `PREROUTING` |

---

# 1\. PYTHON — SCHELETRO GENERALE

```
import argparse
import os
import sys

def main():

    # =========================
    # ARGOMENTI
    # =========================

    parser = argparse.ArgumentParser()

    parser.add_argument("--arg1", required=True)
    parser.add_argument("--arg2", required=True)

    args = parser.parse_args()

    # =========================
    # VALIDAZIONE
    # =========================

    # ...

    # =========================
    # PREPARAZIONE
    # =========================

    # ...

    # =========================
    # ELABORAZIONE
    # =========================

    # ...

if __name__ == "__main__":
    main()
```

## Struttura mentale

```
argparse
   ↓
validation
   ↓
preparation
   ↓
processing
   ↓
fine
```

---

# 2\. `argparse`

## Argomento obbligatorio

```
parser.add_argument(
    "--path",
    required=True
)
```

## Argomento intero

```
parser.add_argument(
    "--threshold",
    required=True,
    type=int
)
```

## Più argomenti

```
parser.add_argument("--path", required=True)
parser.add_argument("--threshold", required=True, type=int)
parser.add_argument("--interval", required=True, type=int)
parser.add_argument("--log", required=True)
```

Poi:

```
args = parser.parse_args()
```

Si accede con:

```
args.path
args.threshold
args.interval
args.log
```

---

# 3\. VALIDAZIONE

## Percorso assoluto

```
if not os.path.isabs(args.path):
    print("path must be absolute", file=sys.stderr)
    sys.exit(1)
```

## Percorso esistente

```
if not os.path.exists(args.path):
    print("path does not exist", file=sys.stderr)
    sys.exit(1)
```

## Deve essere una directory

```
if not os.path.isdir(args.path):
    print("path is not a directory", file=sys.stderr)
    sys.exit(1)
```

## Schema completo directory

```
if not os.path.isabs(args.path):
    print("path must be absolute", file=sys.stderr)
    sys.exit(1)

if not os.path.exists(args.path):
    print("path does not exist", file=sys.stderr)
    sys.exit(1)

if not os.path.isdir(args.path):
    print("path is not a directory", file=sys.stderr)
    sys.exit(1)
```

## Stringa non vuota

```
if not args.pattern.strip():
    print("pattern must not be empty", file=sys.stderr)
    sys.exit(1)
```

## Intero positivo

```
if args.threshold <= 0:
    print("threshold must be positive", file=sys.stderr)
    sys.exit(1)
```

## Intervallo positivo

```
if args.interval <= 0:
    print("interval must be positive", file=sys.stderr)
    sys.exit(1)
```

---

# 4\. FILESYSTEM — FUNZIONI FONDAMENTALI

## Elenco directory

```
os.listdir(path)
```

## Unire percorsi

```
fullpath = os.path.join(path, name)
```

## Verificare file

```
os.path.isfile(fullpath)
```

## Verificare directory

```
os.path.isdir(fullpath)
```

## Dimensione

```
os.path.getsize(fullpath)
```

## Estensione

```
name.endswith(".log")
```

## Directory padre

```
parent = os.path.dirname(path)
```

## Creare directory

```
os.makedirs(path, exist_ok=True)
```

---

# 5\. WALKER RICORSIVO — SCHELETRO FONDAMENTALE

Questo è uno degli scheletri più importanti.

```
def walk(path):

    for name in os.listdir(path):

        fullpath = os.path.join(path, name)

        if os.path.isfile(fullpath):

            # elaborazione file

        elif os.path.isdir(fullpath):

            walk(fullpath)
```

## Da ricordare

```
os.listdir()
      ↓
os.path.join()
      ↓
isfile() / isdir()
      ↓
file → elaboro
directory → ricorsione
```

---

# 6\. WALKER SOLO PER DETERMINATE ESTENSIONI

```
def walk(path):

    for name in os.listdir(path):

        fullpath = os.path.join(path, name)

        if os.path.isfile(fullpath):

            if name.endswith(".log"):

                # elaborazione

        elif os.path.isdir(fullpath):

            walk(fullpath)
```

---

# 7\. PIÙ ESTENSIONI

Se la traccia fornisce:

```
pdf,txt,csv
```

puoi fare:

```
extensions = args.extensions.split(",")
```

Poi:

```
for extension in extensions:

    if name.endswith("." + extension):

        # elaborazione
```

Oppure:

```
if any(
    name.endswith("." + ext)
    for ext in extensions
):
    # elaborazione
```

---

# 8\. LEGGERE UN FILE

## Tutto il contenuto

```
with open(fullpath, "r") as f:

    content = f.read()
```

## Riga per riga

```
with open(fullpath, "r") as f:

    for line in f:

        # elaborazione
```

---

# 9\. CERCARE UN PATTERN

```
with open(fullpath, "r") as f:

    for line in f:

        if args.pattern in line:

            # linea trovata
```

## Salvare le righe

```
matching_lines = []

with open(fullpath, "r") as f:

    for line in f:

        if args.pattern in line:

            matching_lines.append(line)
```

---

# 10\. SCRIVERE UN FILE

## Sovrascrivere

```
with open(destination, "w") as f:

    f.write(message)
```

## Aggiungere

```
with open(logfile, "a") as f:

    f.write(message)
```

## Scrivere più righe

```
with open(destination, "w") as f:

    f.writelines(matching_lines)
```

---

# 11\. CREARE DIRECTORY DI DESTINAZIONE

```
os.makedirs(destination, exist_ok=True)
```

Per il padre di un file:

```
parent = os.path.dirname(logfile)

os.makedirs(parent, exist_ok=True)
```

---

# 12\. SPOSTARE FILE

Import:

```
import shutil
```

Poi:

```
shutil.move(
    fullpath,
    destination
)
```

Schema tipico:

```
destination = os.path.join(dest, extension)

os.makedirs(destination, exist_ok=True)

shutil.move(
    fullpath,
    destination
)
```

---

# 13\. DIMENSIONE RICORSIVA

Schema fondamentale:

```
def get_size(path):

    total = 0

    for name in os.listdir(path):

        fullpath = os.path.join(path, name)

        if os.path.isfile(fullpath):

            total += os.path.getsize(fullpath)

        elif os.path.isdir(fullpath):

            total += get_size(fullpath)

    return total
```

## Punto fondamentale

Deve essere:

```
total += get_size(fullpath)
```

e non semplicemente:

```
get_size(fullpath)
```

perché il valore restituito deve essere sommato.

---

# 14\. WALKER GENERICO DA COMPLETARE

Quando non sai ancora cosa richiede esattamente la traccia:

```
def walk(path):

    for name in os.listdir(path):

        fullpath = os.path.join(path, name)

        if os.path.isfile(fullpath):

            # COSA FARE CON IL FILE?

            pass

        elif os.path.isdir(fullpath):

            # COSA FARE CON LA DIRECTORY?

            walk(fullpath)
```

---

# 15\. DATA E ORA

```
from datetime import datetime
```

Poi:

```
now = datetime.now()
```

Log:

```
with open(logfile, "a") as f:

    f.write(
        f"{datetime.now()} {message}\n"
    )
```

---

# 16\. DEMONE

## Quando usarlo

La traccia dice:

```
continuamente
ogni N secondi
periodicamente mentre il programma rimane attivo
```

→ `while True`.

## Scheletro

```
import time

def main():

    # argparse
    # validation

    while True:

        # =====================
        # ANALISI
        # =====================

        result = ...

        # =====================
        # AZIONE
        # =====================

        if ...:

            ...

        # =====================
        # ATTESA
        # =====================

        time.sleep(interval)

if __name__ == "__main__":
    main()
```

---

# 17\. DEMONE CON DIMENSIONE DIRECTORY

```
def main():

    # argparse
    # validation

    while True:

        total = get_size(args.target)

        if total >= args.threshold:

            with open(args.log, "a") as f:

                f.write(
                    f"{datetime.now()} {total}\n"
                )

        time.sleep(args.interval)
```

La funzione di analisi può essere sostituita con:

```
get_size()
cerca pattern
controlla file
controlla directory
controlla timestamp
controlla condizione
...
```

---

# 18\. DEMONE VS PROCESSO PERIODICO

## DEMONE

```
Python
  ↓
analizza
  ↓
sleep
  ↓
analizza
  ↓
sleep
  ↓
analizza
  ↓
...
```

Codice:

```
while True:

    ...

    time.sleep(interval)
```

## PROCESSO PERIODICO

```
systemd timer
      ↓
service
      ↓
Python
      ↓
elaborazione
      ↓
exit
```

Nel Python:

```
def main():

    # argparse
    # validation
    # elaborazione

if __name__ == "__main__":
    main()
```

**Non mettere****`while True`****se è systemd a doverlo eseguire periodicamente.**

---

# 19\. SYSTEMD — SERVICE

Schema:

```
[Unit]
Description=DESCRIZIONE

[Service]
ExecStart=%h/PERCORSO/app.py ARGOMENTI
```

Versione con riavvio:

```
[Unit]
Description=DESCRIZIONE

[Service]
ExecStart=%h/PERCORSO/app.py ARGOMENTI
Restart=on-failure

[Install]
WantedBy=default.target
```

---

# 20\. `%h`

Nei servizi utente:

```
%h
```

rappresenta la home dell'utente.

Quindi:

```
ExecStart=%h/app/app.py
```

rappresenta concettualmente:

```
/home/utente/app/app.py
```

---

# 21\. SYSTEMD — TIMER

Schema:

```
[Unit]
Description=DESCRIZIONE

[Timer]
Unit=nome.service
OnCalendar=ESPRESSIONE

[Install]
WantedBy=timers.target
```

---

# 22\. `OnCalendar`

## Ogni giorno alle 03:00

```
OnCalendar=*-*-* 03:00
```

## Ogni lunedì alle 02:00

```
OnCalendar=Mon *-*-* 02:00
```

## Ogni mercoledì alle 14:00

```
OnCalendar=Wed *-*-* 14:00
```

## Mercoledì e sabato alle 05:30

```
OnCalendar=Wed,Sat *-*-* 05:30
```

## Regola mentale

```
GIORNO + DATA + ORA
```

---

# 23\. SERVICE + TIMER

Quando la traccia dice:

> crea programma + esecuzione periodica

pensa automaticamente:

```
             TIMER
               │
               ▼
             SERVICE
               │
               ▼
             PYTHON
               │
               ▼
          ELABORAZIONE
               │
               ▼
              EXIT
```

---

# 24\. COMANDI SYSTEMD UTENTE

```
systemctl --user daemon-reload
```

Avviare:

```
systemctl --user start nome.timer
```

Abilitare:

```
systemctl --user enable nome.timer
```

Controllare:

```
systemctl --user status nome.timer
```

Elencare timer:

```
systemctl --user list-timers
```

Verificare un `OnCalendar`:

```
systemd-analyze calendar 'Wed,Sat *-*-* 05:30'
```

---

# 25\. SUDOERS — MODELLO MENTALE

Per ogni regola chiediti:

```
CHI?
 ↓
DOVE?
 ↓
COME CHI?
 ↓
QUALI COMANDI?
 ↓
PASSWORD?
 ↓
ECCEZIONI?
```

La forma generale è:

```
CHI HOST = (UTENTE) [NOPASSWD:] COMANDI
```

---

# 26\. `Host_Alias`

Se la traccia parla di gruppi di host:

```
Host_Alias WEB = web01, web02, web03
```

Altro esempio:

```
Host_Alias DB = db01, db02
```

Schema:

```
gruppo di host
      ↓
Host_Alias
```

---

# 27\. `Cmnd_Alias`

Esempio:

```
Cmnd_Alias FWTOOLS = /usr/sbin/iptables, /usr/bin/tcpdump
```

Più comandi:

```
Cmnd_Alias USERMGM = \
    /usr/sbin/useradd, \
    /usr/sbin/userdel, \
    /usr/sbin/usermod
```

Altro esempio:

```
Cmnd_Alias PKGMGM = \
    /usr/bin/apt, \
    /usr/bin/dpkg
```

Schema:

```
gruppo di comandi
      ↓
Cmnd_Alias
```

---

# 28\. REGOLA SUDOERS BASE

```
alice ALL = (ALL) ALL
```

Significa:

```
alice
 ↓
tutti gli host
 ↓
come qualsiasi utente
 ↓
qualsiasi comando
```

---

# 29\. GRUPPO

Il simbolo `%` indica un gruppo.

Utente:

```
alice
```

Gruppo:

```
%ops
```

Esempio:

```
%ops WEB = (root) USERMGM
```

Significa:

```
gruppo ops
 ↓
host WEB
 ↓
come root
 ↓
comandi USERMGM
```

---

# 30\. `NOPASSWD`

Esempio:

```
%devs DB = (root) NOPASSWD: PKGINFO
```

Significa:

```
%devs
 ↓
DB
 ↓
root
 ↓
PKGINFO
 ↓
senza password
```

Pattern:

```
NOPASSWD:
```

---

# 31\. ESEGUIRE COME UN ALTRO UTENTE

```
dave DB = (nobody) /usr/bin/id
```

La parte:

```
(nobody)
```

significa:

```
esegui come nobody
```

---

# 32\. COMANDO CON ARGOMENTO SPECIFICO

Se la traccia dice:

```
cat /etc/shadow
```

non confondere:

```
/usr/bin/cat
```

con:

```
/usr/bin/cat /etc/shadow
```

Se l'argomento deve essere limitato, usa la forma specifica:

```
carol ALL = NOPASSWD: /usr/bin/cat /etc/shadow
```

---

# 33\. ECCEZIONI SUDOERS

Per escludere un comando:

```
bob ALL = (ALL) ALL, !SHELLS
```

Idea:

```
ALL
+
eccezione
```

Il `!` indica l'esclusione.

---

# 34\. PROCEDURA SUDOERS DA ESAME

Prendi la frase:

> Il gruppo `devs` può eseguire `dpkg` come root sui database senza password.

Trasformala:

```
CHI       = %devs
HOST      = DB
COME CHI  = root
COMANDO   = PKGINFO
PASSWORD  = NOPASSWD
```

Poi:

```
%devs DB = (root) NOPASSWD: PKGINFO
```

---

# 35\. IPTABLES — CAMBIO DI MENTALITÀ

La domanda fondamentale è:

> Il pacchetto è destinato al firewall oppure lo attraversa?

```
client → firewall
```

→ `INPUT`

```
client → firewall → server
```

→ `FORWARD`

---

# 36\. DIAGRAMMA IPTABLES

```
                    PACCHETTO
                        │
                        ▼
                  PREROUTING
                     │
              ┌──────┴──────┐
              │             │
         destinato       attraversa
         al firewall     il firewall
              │             │
              ▼             ▼
            INPUT         FORWARD
                            │
                            ▼
                       POSTROUTING
```

NAT:

```
PREROUTING
    │
    └── DNAT
```

```
POSTROUTING
    │
    ├── SNAT
    └── MASQUERADE
```

---

# 37\. RESET IPTABLES

```
iptables -F
iptables -t nat -F
```

---

# 38\. DEFAULT DENY

```
iptables -P INPUT DROP
iptables -P FORWARD DROP
```

In questo schema:

```
INPUT   → DROP
FORWARD → DROP
```

Poi si aggiungono le eccezioni.

`OUTPUT` normalmente rimane `ACCEPT` se la traccia non richiede diversamente.

---

# 39\. INPUT

Usa `INPUT` quando il pacchetto è destinato al firewall.

## Schema

```
iptables -A INPUT \
    -i INTERFACCIA \
    -p PROTOCOLLO \
    --dport PORTA \
    -j ACCEPT
```

## SSH

```
iptables -A INPUT \
    -i eth1 \
    -p tcp \
    --dport 22 \
    -j ACCEPT
```

## ICMP

```
iptables -A INPUT \
    -i eth1 \
    -p icmp \
    -j ACCEPT
```

---

# 40\. FORWARD

Usa `FORWARD` quando il pacchetto attraversa il firewall.

## Schema

```
iptables -A FORWARD \
    -i ETH_IN \
    -o ETH_OUT \
    -p tcp \
    --dport PORTA \
    -j ACCEPT
```

Esempio:

```
iptables -A FORWARD \
    -i eth0 \
    -o eth1 \
    -p tcp \
    --dport 8080 \
    -j ACCEPT
```

---

# 41\. `ESTABLISHED,RELATED`

Regola fondamentale:

```
iptables -A FORWARD \
    -m conntrack \
    --ctstate ESTABLISHED,RELATED \
    -j ACCEPT
```

Serve per permettere il traffico di ritorno di connessioni già autorizzate.

Mentalità:

```
A → B
 ↓
connessione autorizzata

B → A
 ↓
ESTABLISHED,RELATED
```

---

# 42\. NAT IN USCITA — MASQUERADE

Quando:

```
rete privata → Internet
```

usa:

```
iptables -t nat -A POSTROUTING \
    -o eth0 \
    -j MASQUERADE
```

Schema:

```
private IP
    ↓
MASQUERADE
    ↓
IP pubblico dell'interfaccia
```

---

# 43\. SNAT

Se conosci esplicitamente l'IP pubblico:

```
iptables -t nat -A POSTROUTING \
    -o eth0 \
    -j SNAT \
    --to-source 203.0.113.1
```

Differenza:

```
SNAT
→ specifico manualmente l'IP sorgente
```

```
MASQUERADE
→ usa l'IP dell'interfaccia
```

---

# 44\. DNAT

Quando la traccia dice:

```
Internet → server interno
```

e bisogna modificare la destinazione:

```
DNAT
```

## Schema

```
iptables -t nat -A PREROUTING \
    -i eth0 \
    -p tcp \
    --dport PORTA_PUBBLICA \
    -j DNAT \
    --to-destination IP_INTERNO:PORTA_INTERNA
```

Esempio:

```
iptables -t nat -A PREROUTING \
    -i eth0 \
    -p tcp \
    --dport 80 \
    -j DNAT \
    --to-destination 10.20.30.100:8080
```

---

# 45\. DNAT — ERRORE DA NON FARE

Non basta:

```
PREROUTING + DNAT
```

Dopo il DNAT il pacchetto deve poter attraversare il firewall.

Quindi:

```
DNAT
 ↓
FORWARD
 ↓
ESTABLISHED,RELATED
```

---

# 46\. DNAT COMPLETO

```
iptables -t nat -A PREROUTING \
    -i eth0 \
    -p tcp \
    --dport 80 \
    -j DNAT \
    --to-destination 10.20.30.100:8080

iptables -A FORWARD \
    -i eth0 \
    -o eth1 \
    -p tcp \
    --dport 8080 \
    -j ACCEPT

iptables -A FORWARD \
    -m conntrack \
    --ctstate ESTABLISHED,RELATED \
    -j ACCEPT
```

## Perché `8080` nel FORWARD?

Perché dopo:

```
80 → DNAT → 8080
```

il pacchetto viene valutato nel `FORWARD` con la destinazione modificata.

---

# 47\. DNAT HTTPS

Esempio:

```
porta pubblica 443
        ↓
server interno
        ↓
porta 8443
```

```
iptables -t nat -A PREROUTING \
    -i eth0 \
    -p tcp \
    --dport 443 \
    -j DNAT \
    --to-destination 10.20.30.100:8443

iptables -A FORWARD \
    -i eth0 \
    -o eth1 \
    -p tcp \
    --dport 8443 \
    -j ACCEPT
```

---

# 48\. MASTER SKELETON IPTABLES

```
# ============================
# RESET
# ============================

iptables -F
iptables -t nat -F

# ============================
# DEFAULT DENY
# ============================

iptables -P INPUT DROP
iptables -P FORWARD DROP

# ============================
# INPUT
# ============================

iptables -A INPUT \
    -i INTERFACCIA \
    -p PROTOCOLLO \
    --dport PORTA \
    -j ACCEPT

# ============================
# FORWARD
# ============================

iptables -A FORWARD \
    -i ETH_IN \
    -o ETH_OUT \
    -p tcp \
    --dport PORTA \
    -j ACCEPT

# ============================
# TRAFFICO DI RITORNO
# ============================

iptables -A FORWARD \
    -m conntrack \
    --ctstate ESTABLISHED,RELATED \
    -j ACCEPT

# ============================
# NAT IN USCITA
# ============================

iptables -t nat -A POSTROUTING \
    -o ETH_PUBLIC \
    -j MASQUERADE

# ============================
# DNAT
# ============================

iptables -t nat -A PREROUTING \
    -i ETH_PUBLIC \
    -p tcp \
    --dport PORTA_PUBBLICA \
    -j DNAT \
    --to-destination IP_INTERNO:PORTA_INTERNA

# ============================
# FORWARD POST-DNAT
# ============================

iptables -A FORWARD \
    -i ETH_PUBLIC \
    -o ETH_PRIVATE \
    -p tcp \
    --dport PORTA_INTERNA \
    -j ACCEPT
```

---

# 49\. COME RISOLVERE UNA TRACCIA IPTABLES

## Domanda 1

Il pacchetto è destinato al firewall?

```
SÌ → INPUT
NO → FORWARD
```

## Domanda 2

Da quale interfaccia arriva?

```
-i ...
```

## Domanda 3

Su quale interfaccia esce?

```
-o ...
```

Solo se necessario per quella catena.

## Domanda 4

Qual è il protocollo?

```
-p tcp
-p udp
-p icmp
```

## Domanda 5

Qual è la porta?

```
--dport 22
--dport 80
--dport 443
```

## Domanda 6

Devo permettere?

```
-j ACCEPT
```

## Domanda 7

È traffico di ritorno?

```
-m conntrack --ctstate ESTABLISHED,RELATED
```

## Domanda 8

C'è NAT?

```
destinazione modificata → DNAT
sorgente modificata → SNAT/MASQUERADE
```

---

# 50\. RICONOSCIMENTO RAPIDO NAT

| Frase della traccia | Soluzione |
| --- | --- |
| client privati → Internet | `MASQUERADE` |
| IP sorgente deve diventare X | `SNAT` |
| porta pubblica → server interno | `DNAT` |
| destinazione deve cambiare | `DNAT` |
| sorgente deve cambiare | `SNAT/MASQUERADE` |
| NAT ingresso | `PREROUTING` |
| NAT uscita | `POSTROUTING` |

---

# 51\. PYTHON — PATTERN COMPLETO FILE + RICORSIONE

```
import argparse
import os
import sys

def walk(path, pattern, output):

    for name in os.listdir(path):

        fullpath = os.path.join(path, name)

        if os.path.isfile(fullpath):

            if name.endswith(".log"):

                matches = []

                with open(fullpath, "r") as f:

                    for line in f:

                        if pattern in line:

                            matches.append(line)

                if matches:

                    with open(output, "a") as f:

                        f.writelines(matches)

        elif os.path.isdir(fullpath):

            walk(
                fullpath,
                pattern,
                output
            )

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--path",
        required=True
    )

    parser.add_argument(
        "--pattern",
        required=True
    )

    parser.add_argument(
        "--output",
        required=True
    )

    args = parser.parse_args()

    if not os.path.isabs(args.path):
        print(
            "path must be absolute",
            file=sys.stderr
        )
        sys.exit(1)

    if not os.path.isdir(args.path):
        print(
            "path must be a directory",
            file=sys.stderr
        )
        sys.exit(1)

    walk(
        args.path,
        args.pattern,
        args.output
    )

if __name__ == "__main__":
    main()
```

Questo è un **modello**, non da imparare parola per parola.

---

# 52\. PYTHON — PATTERN COMPLETO DEMONE

```
import argparse
import os
import sys
import time
from datetime import datetime

def get_size(path):

    total = 0

    for name in os.listdir(path):

        fullpath = os.path.join(path, name)

        if os.path.isfile(fullpath):

            total += os.path.getsize(fullpath)

        elif os.path.isdir(fullpath):

            total += get_size(fullpath)

    return total

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--target",
        required=True
    )

    parser.add_argument(
        "--threshold",
        required=True,
        type=int
    )

    parser.add_argument(
        "--interval",
        required=True,
        type=int
    )

    parser.add_argument(
        "--log",
        required=True
    )

    args = parser.parse_args()

    if not os.path.isabs(args.target):
        print(
            "target must be absolute",
            file=sys.stderr
        )
        sys.exit(1)

    if not os.path.isdir(args.target):
        print(
            "target must be a directory",
            file=sys.stderr
        )
        sys.exit(1)

    if args.threshold <= 0:
        print(
            "threshold must be positive",
            file=sys.stderr
        )
        sys.exit(1)

    if args.interval <= 0:
        print(
            "interval must be positive",
            file=sys.stderr
        )
        sys.exit(1)

    while True:

        total = get_size(args.target)

        if total >= args.threshold:

            with open(args.log, "a") as f:

                f.write(
                    f"{datetime.now()} {total}\n"
                )

        time.sleep(args.interval)

if __name__ == "__main__":
    main()
```

---

# 53\. PYTHON — PROCESSO PERIODICO

Se usa systemd timer, togli:

```
while True
```

e:

```
time.sleep(...)
```

Il programma diventa:

```
def main():

    # argparse

    # validation

    # analisi

    # azione

if __name__ == "__main__":
    main()
```

La periodicità appartiene a:

```
systemd timer
```

non al Python.

---

# 54\. SYSTEMD — ESEMPIO COMPLETO

## Service

```
[Unit]
Description=Directory monitor

[Service]
ExecStart=%h/dir-monitor/monitor.py --target %h/data --threshold 1000000 --log %h/monitor.log

[Install]
WantedBy=default.target
```

## Timer

```
[Unit]
Description=Run directory monitor periodically

[Timer]
Unit=dir-monitor.service
OnCalendar=Mon *-*-* 03:00

[Install]
WantedBy=timers.target
```

---

# 55\. SUDOERS — ESEMPIO COMPLETO

```
Host_Alias WEB = web01, web02, web03
Host_Alias DB = db01, db02

Cmnd_Alias USERMGM = \
    /usr/sbin/useradd, \
    /usr/sbin/userdel, \
    /usr/sbin/usermod

Cmnd_Alias PKGINFO = \
    /usr/bin/dpkg, \
    /usr/bin/apt

%ops WEB = (root) USERMGM

%devs DB = (root) NOPASSWD: PKGINFO

dave DB = (nobody) /usr/bin/id
```

---

# 56\. IPTABLES — ESEMPIO COMPLETO

```
iptables -F
iptables -t nat -F

iptables -P INPUT DROP
iptables -P FORWARD DROP

iptables -A INPUT \
    -i eth1 \
    -p tcp \
    --dport 22 \
    -j ACCEPT

iptables -A FORWARD \
    -i eth1 \
    -o eth0 \
    -p tcp \
    --dport 443 \
    -j ACCEPT

iptables -A FORWARD \
    -m conntrack \
    --ctstate ESTABLISHED,RELATED \
    -j ACCEPT

iptables -t nat -A POSTROUTING \
    -o eth0 \
    -j MASQUERADE
```

---

# 57\. ERRORI TIPICI PYTHON

## Errore 1 — dimenticare la ricorsione

Sbagliato:

```
elif os.path.isdir(fullpath):
    pass
```

Se devi visitare le sottodirectory:

```
elif os.path.isdir(fullpath):
    walk(fullpath)
```

---

## Errore 2 — perdere il valore della ricorsione

Sbagliato:

```
elif os.path.isdir(fullpath):
    get_size(fullpath)
```

Corretto:

```
elif os.path.isdir(fullpath):
    total += get_size(fullpath)
```

---

## Errore 3 — usare percorso relativo quando è richiesto assoluto

Controlla:

```
os.path.isabs(path)
```

---

## Errore 4 — confondere file e directory

Usa:

```
os.path.isfile(...)
```

e:

```
os.path.isdir(...)
```

---

## Errore 5 — dimenticare `exist_ok=True`

Se la directory può già esistere:

```
os.makedirs(path, exist_ok=True)
```

---

## Errore 6 — sovrascrivere un log

Se devi mantenere lo storico:

```
open(logfile, "a")
```

non:

```
open(logfile, "w")
```

---

# 58\. ERRORI TIPICI SYSTEMD

## Errore 1 — mettere `while True` quando c'è un timer

Se il timer deve avviare periodicamente il programma:

```
timer → service → Python → exit
```

Non:

```
timer → service → Python → while True
```

---

## Errore 2 — dimenticare `WantedBy`

Service:

```
[Install]
WantedBy=default.target
```

Timer:

```
[Install]
WantedBy=timers.target
```

---

## Errore 3 — confondere service e timer

```
.service
→ cosa eseguire

.timer
→ quando eseguirlo
```

---

# 59\. ERRORI TIPICI SUDOERS

## Errore 1 — dimenticare `%`

Utente:

```
alice
```

Gruppo:

```
%ops
```

---

## Errore 2 — confondere host e comando

```
Host_Alias
→ macchine

Cmnd_Alias
→ comandi
```

---

## Errore 3 — dimenticare `(utente)`

```
dave DB = (nobody) /usr/bin/id
```

`nobody` non è un host.

È l'utente con cui viene eseguito il comando.

---

## Errore 4 — usare `NOPASSWD` nel posto sbagliato

Schema:

```
CHI HOST = (UTENTE) NOPASSWD: COMANDI
```

---

# 60\. ERRORI TIPICI IPTABLES

## Errore 1 — usare INPUT per traffico destinato a un server interno

Se:

```
Internet
 ↓
firewall
 ↓
server interno
```

è:

```
FORWARD
```

non:

```
INPUT
```

---

## Errore 2 — dimenticare il traffico di ritorno

Aggiungi:

```
iptables -A FORWARD \
    -m conntrack \
    --ctstate ESTABLISHED,RELATED \
    -j ACCEPT
```

quando richiesto dal caso.

---

## Errore 3 — fare DNAT senza FORWARD

Non basta:

```
PREROUTING + DNAT
```

Serve anche il passaggio in:

```
FORWARD
```

---

## Errore 4 — usare la porta pubblica nel FORWARD dopo DNAT

Se:

```
80 → DNAT → 8080
```

nel `FORWARD` devi ragionare sulla destinazione post-DNAT:

```
--dport 8080
```

---

## Errore 5 — mettere MASQUERADE in FORWARD

Sbagliato concettualmente.

```
MASQUERADE
→ POSTROUTING
```

---

# 61\. TABELLA FINALE IPTABLES

| Situazione | Chain |
| --- | --- |
| traffico destinato al firewall | `INPUT` |
| traffico attraversa firewall | `FORWARD` |
| pacchetto prima del routing | `PREROUTING` |
| pacchetto dopo il routing | `POSTROUTING` |
| cambio destinazione | `DNAT` |
| cambio sorgente | `SNAT` |
| NAT con IP dell'interfaccia | `MASQUERADE` |
| connessione già stabilita | `ESTABLISHED,RELATED` |

---

# 62\. I 14 MATTONI DA SAPERE

Non devi memorizzare 50 programmi.

Devi sapere ricostruire questi:

```
1.  argparse
2.  validazione
3.  os.listdir()
4.  os.path.join()
5.  isfile()
6.  isdir()
7.  ricorsione
8.  lettura/scrittura file
9.  while True + sleep
10. systemd service
11. systemd timer
12. sudoers
13. INPUT / FORWARD
14. DNAT / SNAT / MASQUERADE
```

E inoltre ricordare:

```
ESTABLISHED,RELATED
```

come meccanismo per il traffico di ritorno.

---

# 63\. LE 4 PROCEDURE DA MEMORIZZARE

## PYTHON

```
TRACCIA
 ↓
ARGOMENTI
 ↓
VALIDAZIONE
 ↓
PREPARAZIONE
 ↓
ELABORAZIONE
 ↓
FINE
```

Se filesystem:

```
os.listdir()
 ↓
os.path.join()
 ↓
file?
 ├── sì → elaboro
 └── no
      ↓
directory?
 └── sì → ricorsione
```

---

## DEMONE

```
PARSE
 ↓
VALIDATE
 ↓
WHILE TRUE
 ↓
ANALISI
 ↓
AZIONE
 ↓
SLEEP
 ↓
ripeti
```

---

## SYSTEMD

```
COSA DEVO ESEGUIRE?
        ↓
     SERVICE

QUANDO?
        ↓
      TIMER
```

---

## IPTABLES

```
DOVE VA IL PACCHETTO?
        │
        ├── firewall → INPUT
        │
        └── altro host → FORWARD

CAMBIO DESTINAZIONE?
        ↓
      DNAT

CAMBIO SORGENTE?
        ↓
   SNAT/MASQUERADE

RITORNO?
        ↓
ESTABLISHED,RELATED
```

---

# 64\. DECISION TREE COMPLETO

```
                    TRACCIA
                       │
          ┌────────────┼────────────┐
          │            │            │
       Python       systemd      rete/sudo
          │            │            │
          │            │       ┌────┴────┐
          │            │       │         │
      filesystem    service   sudoers  iptables
          │          timer               │
          │                              │
    ┌─────┴─────┐                 ┌──────┴──────┐
    │           │                 │             │
  singolo    ricorsivo          INPUT        FORWARD
    │           │                               │
    │           │                         ┌─────┴─────┐
    │           │                         │           │
    │        walker                     NAT       no NAT
    │           │                         │
    │           │                  ┌──────┴──────┐
    │           │                  │             │
    │           │                DNAT      SNAT/MASQ
    │           │
    │       ┌───┴────┐
    │       │        │
    │      file    directory
    │
    └──────────────┐
                   │
             deve ripetersi?
                   │
             ┌─────┴─────┐
             │           │
            sì           no
             │           │
          demone      programma
             │
       while + sleep
```

---

# 65\. PAROLE-CHIAVE → AZIONE

| Se leggi nella traccia... | Scrivi/pensa... |
| --- | --- |
| `obbligatorio` | `required=True` |
| `intero` | `type=int` |
| `positivo` | `> 0` |
| `assoluto` | `os.path.isabs()` |
| `esistente` | `os.path.exists()` |
| `directory` | `os.path.isdir()` |
| `file` | `os.path.isfile()` |
| `ricorsivamente` | funzione che richiama sé stessa |
| `sottodirectory` | `walk(fullpath)` |
| `ogni N secondi` | `while True + sleep` |
| `continuamente` | `while True` |
| `periodicamente` \+ calendario | systemd timer |
| `ogni lunedì` | `OnCalendar=Mon ...` |
| `senza password` | `NOPASSWD:` |
| `gruppo` | `%gruppo` |
| `gruppo di host` | `Host_Alias` |
| `gruppo di comandi` | `Cmnd_Alias` |
| `come root` | `(root)` |
| `come nobody` | `(nobody)` |
| `verso il firewall` | `INPUT` |
| `attraverso il firewall` | `FORWARD` |
| `destinazione modificata` | `DNAT` |
| `sorgente modificata` | `SNAT` |
| `IP dinamico in uscita` | `MASQUERADE` |
| `risposta alla connessione` | `ESTABLISHED,RELATED` |
| `porta pubblica → privata` | `PREROUTING + DNAT + FORWARD` |
| `privati → Internet` | `FORWARD + MASQUERADE` |

---

# 66\. CHECKLIST PRIMA DI CONSEGNARE PYTHON

```
[ ] argparse presente
[ ] tutti gli argomenti presenti
[ ] required=True dove necessario
[ ] type=int dove necessario
[ ] path assoluto controllato
[ ] esistenza controllata
[ ] file/directory controllati
[ ] directory create se necessario
[ ] os.listdir() usato correttamente
[ ] os.path.join() usato correttamente
[ ] file e directory distinti
[ ] ricorsione presente se richiesta
[ ] valore della ricorsione restituito/sommato se necessario
[ ] file aperti con with
[ ] modalità "r", "w", "a" corretta
[ ] sleep presente solo se serve
[ ] while True solo se serve
[ ] main() presente
[ ] if __name__ == "__main__" presente
```

---

# 67\. CHECKLIST SYSTEMD

```
[ ] .service presente
[ ] [Unit] presente
[ ] [Service] presente
[ ] ExecStart corretto
[ ] %h usato correttamente se necessario
[ ] Restart corretto se richiesto
[ ] [Install] presente se richiesto
[ ] WantedBy corretto

[ ] .timer presente
[ ] [Timer] presente
[ ] Unit=nome.service corretto
[ ] OnCalendar corretto
[ ] WantedBy=timers.target
[ ] service e timer hanno nomi coerenti
```

---

# 68\. CHECKLIST SUDOERS

```
[ ] Chi?
[ ] Utente o gruppo?
[ ] Host?
[ ] Host_Alias necessario?
[ ] Come quale utente?
[ ] Comando?
[ ] Cmnd_Alias necessario?
[ ] NOPASSWD?
[ ] Argomenti del comando specificati?
[ ] Eventuali esclusioni?
[ ] % davanti ai gruppi?
```

---

# 69\. CHECKLIST IPTABLES

```
[ ] reset?
[ ] INPUT DROP?
[ ] FORWARD DROP?
[ ] OUTPUT lasciato corretto?
[ ] INPUT o FORWARD?
[ ] interfaccia -i?
[ ] interfaccia -o?
[ ] protocollo?
[ ] porta?
[ ] ACCEPT?
[ ] ESTABLISHED,RELATED?
[ ] DNAT?
[ ] PREROUTING?
[ ] FORWARD post-DNAT?
[ ] SNAT?
[ ] MASQUERADE?
[ ] POSTROUTING?
```

---

# 70\. REGOLA D'ORO

## Non memorizzare questo:

```
"Se vedo questa traccia devo scrivere esattamente questo programma."
```

## Memorizza questo:

```
PAROLA DELLA TRACCIA
        ↓
CONCETTO
        ↓
SCHELETRO
        ↓
PARAMETRO
```

Esempi:

```
"ricorsivamente"
      ↓
ricorsione
      ↓
walk()
      ↓
walk(fullpath)
```

```
"ogni 30 secondi"
      ↓
demone
      ↓
while True
      ↓
sleep(30)
```

```
"ogni lunedì alle 03:00"
      ↓
systemd timer
      ↓
OnCalendar
      ↓
Mon *-*-* 03:00
```

```
"senza password"
      ↓
sudoers
      ↓
NOPASSWD
```

```
"verso il server interno"
      ↓
FORWARD
```

```
"porta pubblica → porta privata"
      ↓
DNAT
      ↓
PREROUTING
      ↓
FORWARD post-DNAT
```

```
"client privati → Internet"
      ↓
MASQUERADE
      ↓
POSTROUTING
```

---

# 71\. FORMULA FINALE DA ESAME

Quando ti danno una traccia, **non iniziare a scrivere codice immediatamente**.

Fai prima questo:

```
1. SOTTOLINEO LE PAROLE CHIAVE

2. IDENTIFICO LA FAMIGLIA

3. SCELGO LO SCHELETRO

4. SCRIVO GLI ARGOMENTI

5. SCRIVO LA VALIDAZIONE

6. INSERISCO LA LOGICA

7. CONTROLLO I CASI SPECIALI

8. CONTROLLO LA SINTASSI

9. RILEGGO LA TRACCIA

10. VERIFICO CHE OGNI RICHIESTA
    ABBIA UNA CORRISPONDENTE
    RIGA DI CODICE/CONFIGURAZIONE
```

---

# 72\. I 5 SCHELETRI DA SAPERE A MEMORIA

## 1\. Walker

```
def walk(path):

    for name in os.listdir(path):

        fullpath = os.path.join(path, name)

        if os.path.isfile(fullpath):

            # ...

        elif os.path.isdir(fullpath):

            walk(fullpath)
```

## 2\. Dimensione ricorsiva

```
def get_size(path):

    total = 0

    for name in os.listdir(path):

        fullpath = os.path.join(path, name)

        if os.path.isfile(fullpath):

            total += os.path.getsize(fullpath)

        elif os.path.isdir(fullpath):

            total += get_size(fullpath)

    return total
```

## 3\. Demone

```
while True:

    # analisi

    # azione

    time.sleep(interval)
```

## 4\. Sudoers

```
Host_Alias HOSTS = ...

Cmnd_Alias CMDS = ...

CHI HOSTS = (UTENTE) NOPASSWD: CMDS
```

## 5\. iptables

```
iptables -F
iptables -t nat -F

iptables -P INPUT DROP
iptables -P FORWARD DROP

iptables -A INPUT ...

iptables -A FORWARD ...

iptables -A FORWARD \
    -m conntrack \
    --ctstate ESTABLISHED,RELATED \
    -j ACCEPT

iptables -t nat -A POSTROUTING \
    -o ETH \
    -j MASQUERADE

iptables -t nat -A PREROUTING \
    -i ETH \
    -p tcp \
    --dport PUBLIC \
    -j DNAT \
    --to-destination IP:PRIVATE
```
