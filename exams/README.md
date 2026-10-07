# Demone 
## S

# Processo periodico
## S

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
