## DOMANDE-RISPOSTE 
### 5. Quali sono le regole fondamentali che governano il modello di permessi tradizionale di UNIX?
Il modello di controllo degli accessi standard di UNIX segue queste regole fondamentali:
- Le decisioni di controllo dipendono dall'utente (o dalla sua appartenenza a un gruppo) che tenta di eseguire un'operazione.
- Gli oggetti, come file e processi, hanno dei proprietari che esercitano un controllo ampio su di essi.
- Un utente è il proprietario degli oggetti che crea.
- L'account speciale **root** può agire come proprietario di qualsiasi oggetto nel sistema.
- Solo l'utente **root** può eseguire determinate operazioni amministrative sensibili.

Il sistema gestisce queste identità tramite numeri chiamati UID (User Identifier) e GID (Group Identifier). Ogni file ha bit di permesso che definiscono le azioni di lettura, scrittura ed esecuzione per tre categorie: il proprietario, il gruppo e tutti gli altri utenti. L'utente root, avendo UID 0, ha il privilegio di superare i normali controlli di permesso su quasi ogni risorsa.

### 6. Quali identità sono associate a un processo e quale ruolo svolge ciascuna?
Un processo è associato a tre set principali di identificativi (ID):
- **UID e GID reali (Real UID/GID)**: Rappresentano "chi siamo veramente". Vengono presi dal file /etc/passwd al momento del login e solitamente non cambiano durante la sessione.
- **UID e GID effettivi (Effective UID/GID)**: Insieme ai GID supplementari, sono le identità utilizzate dal kernel per i controlli dei permessi di accesso ai file.
- **ID salvati (Saved set-UID/GID)**: Contengono una copia dell'UID/GID effettivo nel momento in cui il processo inizia l'esecuzione. Vengono utilizzati per consentire al processo di passare dalla modalità privilegiata a quella non privilegiata e viceversa.

Normalmente, l'identità reale e quella effettiva coincidono. Tuttavia, l'identità effettiva può essere "elevata" (ad esempio tramite il bit set-UID) per consentire a un processo di eseguire operazioni che richiedono privilegi superiori a quelli dell'utente che ha lanciato il comando (come cambiare la propria password scrivendo in /etc/shadow). Gli ID salvati servono proprio a gestire questi passaggi di stato, memorizzando l'identità privilegiata in modo da potervi tornare dopo averla temporaneamente abbandonata.

### 7. Cos'è l'esecuzione set-UID, perché il comando passwd ne ha bisogno e cosa succede quando un utente normale esegue passwd?
L'esecuzione **set-UID** è un meccanismo che permette a un programma di essere eseguito con i privilegi del proprietario del file eseguibile, invece che con quelli dell'utente che lo ha lanciato. Il comando passwd ne ha bisogno perché le password degli utenti sono memorizzate nel file /etc/shadow, che per motivi di sicurezza è leggibile e scrivibile solo dall'utente root. Quando un utente normale esegue passwd, il kernel nota il bit set-UID sul file e imposta l'UID effettivo del processo a 0 (root), consentendo al programma di scrivere la nuova password in /etc/shadow.

Senza il bit set-UID, un utente normale non avrebbe i permessi necessari per modificare i file di sistema protetti e non potrebbe quindi cambiare la propria password. Grazie a questo bit (visibile come una "s" nei permessi del file, ad esempio -rwsr-xr-x), il kernel eleva temporaneamente i privilegi del processo alla sola identità del proprietario del file (root) per tutta la durata dell'operazione, mentre l'identità reale rimane quella dell'utente originale.

### 8. Perché sudo è generalmente preferito al login diretto come root o a su per ottenere i privilegi di root, e quali sono i suoi principali vantaggi e svantaggi?
**sudo** è preferito perché offre un controllo più granulare e una migliore tracciabilità rispetto agli altri metodi. Mentre il login diretto come root non lascia traccia di chi ha eseguito le operazioni e **su** registra solo chi è diventato root (ma non i comandi impartiti), **sudo** registra ogni singolo comando eseguito.
1. Vantaggi principali:
    - **Logging dei comandi**: ogni azione è registrata.
    - **Privilegi limitati**: gli utenti possono eseguire solo compiti specifici senza avere poteri illimitati.
    - **Sicurezza delle password**: gli utenti usano la propria password e non devono conoscere quella di root.
    - **Gestione centralizzata**: i permessi sono gestiti in un unico file (/etc/sudoers).
2. Svantaggi principali:
    - Il logging può essere aggirato (ad esempio eseguendo sudo su, che apre una shell di root i cui comandi successivi non vengono loggati).
    - La compromissione dell'account di un "sudoer" equivale a compromettere l'account root.

## FLASHCARD
### 5. Quali sono le regole fondamentali che governano il modello di permessi tradizionale di UNIX?
X

### 6. Quali identità sono associate a un processo e quale ruolo svolge ciascuna?
X

### 7. Cos'è l'esecuzione set-UID, perché il comando passwd ne ha bisogno e cosa succede quando un utente normale esegue passwd?
X

### 8. Perché sudo è generalmente preferito al login diretto come root o a su per ottenere i privilegi di root, e quali sono i suoi principali vantaggi e svantaggi?
X
