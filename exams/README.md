# Demone 
## S

# Processo periodico
## S

# Filtraggio dei pacchetti e NAT
## S

# Amministrazione degli account
## Sintassi standard di una regola in **sudo**:
**Chi** (Utente/Gruppo) **Dove** (Host) = (*Come chi* (Utente RunAs)) [Opzioni] **Cosa** (Comandi)

```%```: Un prefisso ```%``` indica un gruppo del sistema operativo (es. ```%acct```).

```NOPASSWD:```: Consente di eseguire il comando senza inserire la password.

```(ALL)``` o ```(utente)```: Definisce l'utente target sotto le cui spoglie eseguire il comando. Se omesso, di default ```sudo``` assume ```(root)```.

ESEMPIO:
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
