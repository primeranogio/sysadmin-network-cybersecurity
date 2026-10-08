## 1. DEMONE

### COSA TI VIENE CHIESTO

Hai un **programma Python che deve rimanere in esecuzione indefinitamente**.

La struttura concettuale è:

```text
avvio
  ↓
leggo/configuro gli argomenti
  ↓
controllo gli argomenti
  ↓
┌───────────────────────┐
│       ANALIZZO        │
│          ↓            │
│   eventualmente agisco│
│          ↓            │
│       sleep           │
└───────────┬───────────┘
            │
            └──────→ ripeto
```

### LA COSA CHE LO CARATTERIZZA

Nel Python compare:

```python
while True:
```

e normalmente:

```python
time.sleep(...)
```

Quindi:

```python
while True:

    # analisi

    # eventuale azione

    time.sleep(interval)
```

**Questo è il cuore del demone.**

---

# DEMONE — SCHELETRO COMPLETO

```python
import argparse
import os
import sys
import time
from datetime import datetime


def main():

    # ==================================================
    # 1. ARGOMENTI
    # ==================================================

    parser = argparse.ArgumentParser()

    parser.add_argument("--target", required=True)
    parser.add_argument("--threshold", required=True, type=int)
    parser.add_argument("--interval", required=True, type=int)
    parser.add_argument("--log", required=True)

    args = parser.parse_args()


    # ==================================================
    # 2. VALIDAZIONE
    # ==================================================

    # target
    if not os.path.isabs(args.target):
        print("target must be absolute", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.target):
        print("target does not exist", file=sys.stderr)
        sys.exit(1)

    if not os.path.isdir(args.target):
        print("target is not a directory", file=sys.stderr)
        sys.exit(1)


    # threshold
    if args.threshold <= 0:
        print("threshold must be positive", file=sys.stderr)
        sys.exit(1)


    # interval
    if args.interval <= 0:
        print("interval must be positive", file=sys.stderr)
        sys.exit(1)


    # log
    if not os.path.isabs(args.log):
        print("log must be absolute", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.log):
        print("log directory does not exist", file=sys.stderr)
        sys.exit(1)

    if not os.path.isdir(args.log):
        print("log is not a directory", file=sys.stderr)
        sys.exit(1)


    # ==================================================
    # 3. PREPARAZIONE
    # ==================================================

    logfile = os.path.join(
        args.log,
        "nome-del-log.log"
    )


    # ==================================================
    # 4. DEMONE
    # ==================================================

    while True:

        # ----------------------------------------------
        # ANALISI
        # ----------------------------------------------

        result = ...


        # ----------------------------------------------
        # CONDIZIONE
        # ----------------------------------------------

        if ...:

            with open(logfile, "a") as f:

                f.write(
                    f"{datetime.now()} {result}\n"
                )


        # ----------------------------------------------
        # ATTESA
        # ----------------------------------------------

        time.sleep(args.interval)


if __name__ == "__main__":
    main()
```

---

## COSA PUÒ CAMBIARE NEL DEMONE?

Quasi sempre cambia **solo l'analisi**.

Per esempio:

### Controllare dimensione directory

```python
result = get_size(args.target)

if result >= args.threshold:
    ...
```

### Controllare file

```python
result = ...
if result:
    ...
```

### Controllare una condizione

```python
if condition:
    ...
```

### Scrivere nel log

```python
with open(logfile, "a") as f:
    f.write(...)
```

### Analizzare ricorsivamente

Usi:

```python
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

---

# DEMONE: COSA NON DEVI CONFONDERE

Il demone **non è**:

```text
systemd timer
```

Il timer non serve per rendere il Python infinito.

Nel demone:

```text
Python
 ├─ lavora
 ├─ sleep
 ├─ lavora
 ├─ sleep
 └─ ...
```

Il processo Python **rimane vivo**.

---

# 2. PROCESSO PERIODICO

Qui la distinzione deve essere nettissima.

## COSA TI VIENE CHIESTO

Hai un Python che deve:

```text
essere eseguito
     ↓
fare il lavoro
     ↓
terminare
```

e **systemd lo riavvierà secondo una periodicità**.

Nel PDF, ad esempio, `log-extractor` viene strutturato come Python + service + timer. 

---

# PROCESSO PERIODICO — SCHEMA

```text
SYSTEMD TIMER
      │
      │ arriva l'orario
      ▼
SYSTEMD SERVICE
      │
      ▼
PYTHON
      │
      ├── argparse
      ├── validazione
      ├── elaborazione
      └── termina
```

### DIFFERENZA FONDAMENTALE

Nel Python **NON** hai:

```python
while True:
```

---

# PROCESSO PERIODICO — SCHELETRO PYTHON

```python
import argparse
import os
import sys


def main():

    # ==================================================
    # 1. ARGOMENTI
    # ==================================================

    parser = argparse.ArgumentParser()

    parser.add_argument("--path", required=True)
    parser.add_argument("--pattern", required=True)

    args = parser.parse_args()


    # ==================================================
    # 2. VALIDAZIONE
    # ==================================================

    if not os.path.isabs(args.path):
        print("path must be absolute", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.path):
        print("path does not exist", file=sys.stderr)
        sys.exit(1)

    if not os.path.isdir(args.path):
        print("path is not a directory", file=sys.stderr)
        sys.exit(1)

    if not args.pattern:
        print("pattern must not be empty", file=sys.stderr)
        sys.exit(1)


    # ==================================================
    # 3. PREPARAZIONE
    # ==================================================

    ...


    # ==================================================
    # 4. ELABORAZIONE
    # ==================================================

    ...


    # ==================================================
    # 5. FINE
    # ==================================================


if __name__ == "__main__":
    main()
```

Il programma arriva in fondo e **termina**.

---

# PROCESSO PERIODICO — SERVICE

```ini
[Unit]
Description=Nome del processo

[Service]
ExecStart=%h/percorso/app.py ARGOMENTI

[Install]
WantedBy=default.target
```

Se richiesto un riavvio in caso di errore:

```ini
Restart=on-failure
```

---

# PROCESSO PERIODICO — TIMER

```ini
[Unit]
Description=Esecuzione periodica

[Timer]
Unit=nome.service
OnCalendar=ESPRESSIONE

[Install]
WantedBy=timers.target
```

Esempio:

```ini
OnCalendar=Mon,Fri *-*-* 02:00
```

---

# PROCESSO PERIODICO — COSA PUÒ CAMBIARE?

### Cambia il lavoro Python

Per esempio:

```text
cerca ERROR
```

oppure:

```text
sposta PDF
```

oppure:

```text
analizza directory
```

oppure:

```text
crea backup
```

### Cambia il calendario

```text
ogni lunedì
ogni lunedì e venerdì
ogni giorno
ogni mercoledì alle 14
```

### Cambiano gli argomenti del service

Ma la struttura resta:

```text
Python
+
.service
+
.timer
```

---

# DEMONE VS PROCESSO PERIODICO

Questa è la distinzione che voglio che tu abbia **istantaneamente** in testa:

|                        | DEMONE                | PROCESSO PERIODICO    |
| ---------------------- | --------------------- | --------------------- |
| Python                 | rimane vivo           | termina               |
| `while True`           | **SÌ**                | **NO**                |
| `sleep()` nel Python   | normalmente sì        | no                    |
| systemd service        | sì                    | sì                    |
| systemd timer          | **no**                | **sì**                |
| ripetizione gestita da | Python                | systemd               |
| modello                | `work → sleep → work` | `start → work → exit` |

Quindi:

> **Demone = la periodicità è dentro Python.**

> **Processo periodico = la periodicità è fuori Python, in systemd timer.**

Questa è probabilmente la distinzione più importante tra i due.

---

# 3. FILTRAGGIO DEI PACCHETTI

Qui cambia completamente il tipo di ragionamento.

Non stai scrivendo un programma.

Stai costruendo **regole firewall**.

La domanda fondamentale è:

> **Quale pacchetto voglio permettere o bloccare?**

---

# FILTRAGGIO — LE 5 DOMANDE

Per ogni regola:

```text
1. DA DOVE arriva?
2. DOVE va?
3. Attraversa il firewall o è destinato al firewall?
4. Quale protocollo/porta?
5. ACCEPT o DROP?
```

---

# INPUT VS FORWARD

Questa è la distinzione principale.

## INPUT

Il pacchetto vuole arrivare **al firewall**.

```text
PC
 │
 ▼
FIREWALL
```

→

```bash
iptables -A INPUT ...
```

Esempio:

```text
SSH verso il firewall
```

→

```bash
iptables -A INPUT -i eth1 -p tcp --dport 22 -j ACCEPT
```

---

## FORWARD

Il pacchetto attraversa il firewall.

```text
Internet
   │
   ▼
FIREWALL
   │
   ▼
SERVER
```

→

```bash
iptables -A FORWARD ...
```

Esempio:

```text
Internet → server interno
```

→ `FORWARD`.

---

# FILTRAGGIO — SCHELETRO

```bash
# RESET
iptables -F
iptables -t nat -F

# DEFAULT DENY
iptables -P INPUT DROP
iptables -P FORWARD DROP


# TRAFFICO DESTINATO AL FIREWALL
iptables -A INPUT \
    -i INTERFACCIA \
    -p PROTOCOLLO \
    --dport PORTA \
    -j ACCEPT


# TRAFFICO ATTRAVERSO IL FIREWALL
iptables -A FORWARD \
    -i INTERFACCIA_IN \
    -o INTERFACCIA_OUT \
    -p PROTOCOLLO \
    --dport PORTA \
    -j ACCEPT


# RISPOSTE
iptables -A FORWARD \
    -m conntrack \
    --ctstate ESTABLISHED,RELATED \
    -j ACCEPT
```

Il materiale del PDF usa proprio `INPUT/FORWARD` con policy `DROP` e una regola `ESTABLISHED,RELATED` per il traffico di ritorno.  

---

# COSA PUÒ CAMBIARE NEL FILTRAGGIO?

Quasi tutto ciò che sta dentro la regola:

```text
-i
-o
-p
--dport
-j
```

Per esempio:

```text
eth0
eth1
tcp
80
ACCEPT
```

può diventare:

```text
eth1
eth0
tcp
443
ACCEPT
```

Lo **scheletro concettuale non cambia**.

---

# 4. NAT

NAT è diverso dal semplice filtraggio.

Qui non stai solamente dicendo:

> "Questo pacchetto è consentito?"

Stai dicendo:

> **"Devo modificare l'indirizzo/porta del pacchetto."**

Nel PDF vengono distinti `DNAT`, `SNAT` e `MASQUERADE`, con `DNAT` in `PREROUTING` e `SNAT/MASQUERADE` in `POSTROUTING`. 

---

# NAT — DUE DOMANDE

## 1. Sto modificando la DESTINAZIONE?

→ **DNAT**

```text
203.0.113.1:80
        ↓
10.20.30.100:8080
```

→ `PREROUTING`

---

## 2. Sto modificando la SORGENTE?

→ **SNAT/MASQUERADE**

```text
10.20.30.50
     ↓
203.0.113.1
```

→ `POSTROUTING`

---

# DNAT — SCHELETRO

```bash
iptables -t nat -A PREROUTING \
    -i INTERFACCIA_PUBBLICA \
    -p tcp \
    --dport PORTA_PUBBLICA \
    -j DNAT \
    --to-destination IP_PRIVATO:PORTA_PRIVATA
```

**MA ATTENZIONE:**

Il DNAT da solo non basta.

Devi pensare:

```text
DNAT
 ↓
FORWARD
 ↓
ESTABLISHED,RELATED
```

Quindi:

```bash
iptables -A FORWARD \
    -i ETH_PUBLIC \
    -o ETH_PRIVATE \
    -p tcp \
    --dport PORTA_PRIVATA \
    -j ACCEPT
```

Il punto fondamentale è che il `FORWARD` deve usare la **porta post-DNAT**. Il PDF lo evidenzia esplicitamente. 

---

# MASQUERADE — SCHELETRO

Quando la traccia dice:

> permettere ai computer della rete privata di accedere a Internet

pensa:

```text
rete privata
     ↓
firewall
     ↓
Internet
```

→

```bash
iptables -t nat -A POSTROUTING \
    -o ETH_PUBLIC \
    -j MASQUERADE
```

---

# SNAT — SCHELETRO

Se invece la traccia specifica l'IP pubblico:

```bash
iptables -t nat -A POSTROUTING \
    -o ETH_PUBLIC \
    -j SNAT \
    --to-source IP_PUBBLICO
```

---

# FILTRAGGIO VS NAT

Questa distinzione deve essere chiarissima:

|                   | FILTRAGGIO           | NAT                        |
| ----------------- | -------------------- | -------------------------- |
| Scopo             | permettere/bloccare  | modificare indirizzi/porte |
| tabella           | `filter`             | `nat`                      |
| catene principali | INPUT/FORWARD        | PREROUTING/POSTROUTING     |
| azione tipica     | ACCEPT               | DNAT/SNAT/MASQUERADE       |
| domanda           | "Lo lascio passare?" | "Devo modificarlo?"        |

E soprattutto:

> **NAT e filtraggio possono comparire nello stesso esercizio.**

Per esempio:

```text
Internet
   │
   │ 203.0.113.1:80
   ▼
DNAT
   │
   │ 10.20.30.100:8080
   ▼
FORWARD
   │
   ▼
SERVER
```

Quindi:

```text
NAT = modifica
FILTER = autorizzazione
```

---

# 5. AMMINISTRAZIONE DEGLI ACCOUNT

Qui ancora una volta **non stai scrivendo Python e non stai filtrando pacchetti**.

Stai traducendo una descrizione di permessi in **regole sudoers**.

---

# LE 5 DOMANDE SUDOERS

Per ogni regola chiediti:

```text
CHI?
 ↓
SU QUALI HOST?
 ↓
COME QUALE UTENTE?
 ↓
QUALI COMANDI?
 ↓
CON PASSWORD O SENZA?
```

---

# SUDOERS — SCHELETRO

```sudoers
# ==================================================
# HOST
# ==================================================

Host_Alias WEB = ...
Host_Alias DB = ...


# ==================================================
# COMANDI
# ==================================================

Cmnd_Alias CMD1 = ...
Cmnd_Alias CMD2 = ...


# ==================================================
# PERMESSI
# ==================================================

CHI HOST = (COME_CHI) [NOPASSWD:] COMANDI
```

---

# ESEMPIO DI TRADUZIONE

Traccia:

> Il gruppo `acct` può usare `useradd` e `usermod` come root sui server web.

Prima costruisci mentalmente:

```text
CHI       → %acct
HOST      → WEB
COME CHI  → root
COMANDI   → ACCTMGM
PASSWORD  → normale
```

Poi:

```sudoers
%acct WEB = (root) ACCTMGM
```

---

# SUDOERS — TIPI DI ELEMENTI

### Tutti gli host

```sudoers
ALL
```

### Tutti gli utenti

```sudoers
(ALL)
```

### Root

```sudoers
(root)
```

### Gruppo

```sudoers
%nomegruppo
```

### Host raggruppati

```sudoers
Host_Alias WEB = web01, web02
```

### Comandi raggruppati

```sudoers
Cmnd_Alias PKG = /usr/bin/apt, /usr/bin/dpkg
```

### Nessuna password

```sudoers
NOPASSWD:
```

---

# AMMINISTRAZIONE ACCOUNT — COSA PUÒ CAMBIARE?

La struttura non cambia.

Può cambiare:

```text
CHI
HOST
UTENTE TARGET
COMANDO
GRUPPO
PASSWORD
ECCEZIONE
```

Per esempio:

```sudoers
alice ALL = (ALL) ALL
```

oppure:

```sudoers
%ops WEB = (root) USERMGM
```

oppure:

```sudoers
dave DB = (nobody) /usr/bin/id
```

oppure:

```sudoers
carol ALL = NOPASSWD: /usr/bin/cat /etc/shadow
```

Sono tutte variazioni dello **stesso schema**. Il PDF presenta proprio queste forme: utenti, gruppi, host alias, command alias, `NOPASSWD`, utenti target ed esclusioni. 

---

# 6. I QUATTRO ESERCIZI — CONFRONTO DEFINITIVO

Questa è la tabella che terrei davanti mentre studi.

|                   | DEMONE            | PROCESSO PERIODICO               | FILTRAGGIO      | NAT                  | ACCOUNT                 |
| ----------------- | ----------------- | -------------------------------- | --------------- | -------------------- | ----------------------- |
| Linguaggio        | Python            | Python + systemd                 | Bash/iptables   | Bash/iptables        | sudoers                 |
| Cosa costruisci   | processo infinito | processo lanciato periodicamente | regole firewall | traduzione indirizzi | permessi sudo           |
| Concetto centrale | `while True`      | `.timer`                         | `INPUT/FORWARD` | `DNAT/SNAT`          | `CHI HOST = (USER) CMD` |
| Ripetizione       | Python            | systemd                          | —               | —                    | —                       |
| File ricorsivi    | possibile         | possibile                        | no              | no                   | no                      |
| `sleep()`         | sì                | no                               | no              | no                   | no                      |
| `service`         | sì                | sì                               | no              | no                   | no                      |
| `timer`           | no                | sì                               | no              | no                   | no                      |
| `INPUT`           | no                | no                               | sì              | eventualmente        | no                      |
| `FORWARD`         | no                | no                               | sì              | spesso               | no                      |
| `PREROUTING`      | no                | no                               | no              | DNAT                 | no                      |
| `POSTROUTING`     | no                | no                               | no              | SNAT/MASQUERADE      | no                      |
| `sudoers`         | no                | no                               | no              | no                   | sì                      |

---

# 7. MA SOPRATTUTTO: COSA DEVI FARE QUANDO TI DANNO LA TRACCIA

Dato che **all'esame sai già la categoria**, non devi fare:

```text
"È un demone?"
"È un processo periodico?"
"È NAT?"
```

Quello lo sai già.

Devi invece fare:

---

## SE È UN DEMONE

```text
1. Quali argomenti?
2. Come li valido?
3. Cosa devo analizzare?
4. Devo attraversare directory?
5. Cosa succede quando trovo la condizione?
6. Cosa devo scrivere/spostare?
7. Quanto devo aspettare?
```

Poi:

```python
while True:
    ANALISI
    AZIONE
    sleep
```

---

# SE È UN PROCESSO PERIODICO

```text
1. Quali argomenti?
2. Come li valido?
3. Cosa devo analizzare?
4. Come elaboro i dati?
5. Qual è il service?
6. Qual è il calendario?
```

Poi:

```text
Python
+
.service
+
.timer
```

**Niente `while True`.**

---

# SE È FILTRAGGIO PACCHETTI

```text
1. Il traffico arriva al firewall?
       ↓
      INPUT

2. Oppure attraversa il firewall?
       ↓
      FORWARD

3. Interfaccia ingresso?
4. Interfaccia uscita?
5. Protocollo?
6. Porta?
7. ACCEPT?
8. Serve traffico di ritorno?
       ↓
ESTABLISHED,RELATED
```

---

# SE È NAT

```text
1. Cambio DESTINAZIONE?
       ↓
      DNAT
       ↓
 PREROUTING

2. Cambio SORGENTE?
       ↓
 SNAT/MASQUERADE
       ↓
 POSTROUTING
```

E se c'è DNAT:

```text
DNAT
 ↓
FORWARD sulla porta interna
 ↓
ESTABLISHED,RELATED
```

---

# SE È AMMINISTRAZIONE ACCOUNT

Per **ogni frase** della traccia:

```text
CHI?
 ↓
DOVE?
 ↓
COME CHI?
 ↓
COSA?
 ↓
PASSWORD?
```

Poi costruisci:

```sudoers
CHI HOST = (COME_CHI) [NOPASSWD:] COMANDI
```

---

# 8. LA MINI-SCHEDA DA MEMORIZZARE

Se dovessi ridurre tutto a pochissime righe, imparerei questa:

```text
══════════════════════════════════════════════════
DEMONE
══════════════════════════════════════════════════

Python:
while True:
    lavoro()
    time.sleep(interval)

→ Python rimane vivo
→ periodicità dentro Python
```

```text
══════════════════════════════════════════════════
PROCESSO PERIODICO
══════════════════════════════════════════════════

Python:
    lavoro()
    exit

systemd:
    service
       ↑
    timer

→ Python termina
→ periodicità gestita da systemd
```

```text
══════════════════════════════════════════════════
FILTRAGGIO
══════════════════════════════════════════════════

destinazione = FIREWALL
        ↓
      INPUT

attraversa FIREWALL
        ↓
     FORWARD

default:
INPUT DROP
FORWARD DROP

risposte:
ESTABLISHED,RELATED
```

```text
══════════════════════════════════════════════════
NAT
══════════════════════════════════════════════════

DESTINAZIONE
    ↓
   DNAT
    ↓
PREROUTING

SORGENTE
    ↓
SNAT / MASQUERADE
    ↓
POSTROUTING
```

```text
══════════════════════════════════════════════════
ACCOUNT
══════════════════════════════════════════════════

CHI
 ↓
HOST
 ↓
COME CHI
 ↓
COMANDO
 ↓
PASSWORD?

CHI HOST = (USER) [NOPASSWD:] CMD
```

---

# 9. E LA DISTINZIONE PIÙ IMPORTANTE DI TUTTE

Vorrei che questi quattro concetti diventassero quasi automatici:

### DEMONE

> **"Devo far continuare a vivere il programma."**

```python
while True
```

### PROCESSO PERIODICO

> **"Devo far ripartire il programma a determinati orari."**

```text
systemd timer
```

### FILTRAGGIO

> **"Devo decidere se un pacchetto può attraversare/arrivare al firewall."**

```text
INPUT / FORWARD
```

### NAT

> **"Devo cambiare sorgente o destinazione del pacchetto."**

```text
DNAT / SNAT / MASQUERADE
```

### AMMINISTRAZIONE ACCOUNT

> **"Devo decidere chi può eseguire quale comando, su quale host e come quale utente."**

```text
sudoers
```

La parte davvero variabile, e quindi quella su cui conviene allenarsi, è **riempire correttamente gli spazi vuoti dello scheletro**.

