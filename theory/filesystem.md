## DOMANDE-RISPOSTE 
### 9. Quali tipi di file supporta UNIX e in che modo i nove bit di permesso (rwx per utente, gruppo e altri) regolano le operazioni consentite su ciascun tipo?
UNIX supporta sette tipi di file fondamentali, ognuno identificato da un simbolo:
- **File regolari (-)**: Sequenze di byte come testi o programmi.
- **Directory (d)**: File che contengono riferimenti (nomi) ad altri file.
- **Link simbolici (l)**: Riferimenti per nome ad altri file.
- **File di dispositivo a caratteri (c) e a blocchi (b)**: Interfacce per comunicare con l'hardware.
- **Named pipe (p)**: Canali di comunicazione FIFO tra processi.
- **Socket di dominio locale (s)**: Canali di comunicazione full-duplex tra processi sullo stesso host.

I nove bit di permesso (rwx) regolano le operazioni come segue:
- **File regolari**: **r** permette di leggere il contenuto, **w** di modificarlo, **x** di eseguirlo come programma.
- **Directory**: **r** permette di elencare i file contenuti (ls); **w** permette di creare, eliminare o rinominare file (ma funziona solo se è presente anche x); **x** permette di "entrare" nella directory (cd).
- **Dispositivi/Pipe/Socket**: **r** e **w** regolano tipicamente la lettura e scrittura nel canale di comunicazione.

### 10. perché lo smontaggio differito (umount -l) è considerato non sicuro, quale comando permette di identificare i processi che mantengono ancora riferimenti al filesystem occupato e come si può eseguire invece uno smontaggio pulito?
Lo smontaggio "lazy" (**umount -l**) è considerato insicuro perché non vi è alcuna garanzia che i riferimenti esistenti (file aperti) vengano mai chiusi dai programmi; inoltre, tale modalità presenta semantiche inconsistenti, poiché i programmi possono continuare a leggere e scrivere file già aperti ma non possono aprirne di nuovi. Il comando che permette di identificare i processi che mantengono occupato un filesystem è **fuser -m**. Per eseguire uno smontaggio pulito, l'amministratore deve assicurarsi che non vi siano file aperti, processi la cui directory corrente si trovi nel filesystem o file eseguibili in esecuzione da tale risorsa.

Un filesystem viene definito "occupato" (busy) quando il kernel rileva attività che ne impediscono la rimozione sicura. L'uso di fuser -m permette di visualizzare l'utente e il PID del processo che detiene il riferimento, consentendo all'amministratore di chiudere correttamente tali processi o file prima di riprovare il comando umount senza l'opzione lazy.

### 11. Quali sono gli scopi dei bit set-UID, set-GID e sticky, a quali file o directory regolari si applicano e in che modo modificano i controlli dei permessi?
Questi tre bit di permesso speciali hanno scopi e applicazioni differenti:
- **Set-UID**: Si applica ai file regolari eseguibili; permette a un programma di essere eseguito con i permessi del proprietario del file anziché con quelli dell'utente che lo ha lanciato.
- **Set-GID**: Si applica sia ai file regolari che alle directory. Sui file eseguibili, consente l'esecuzione con i permessi del gruppo proprietario. Sulle directory, fa sì che i nuovi file creati al loro interno ereditino la proprietà del gruppo della directory stessa, invece del gruppo predefinito dell'utente che crea il file.
- **Sticky bit**: Si applica esclusivamente alle directory; garantisce che un file possa essere eliminato o rinominato solo dal proprietario del file stesso, dal proprietario della directory o dall'utente root.

### 12. Chi può modificare i bit di permesso di un file, quale comando può utilizzare e come viene invocato tale comando?
Solo il proprietario del file e l'utente root hanno il permesso di modificarne i bit di protezione. Il comando utilizzato per questa operazione è chmod. Viene invocato specificando le autorizzazioni da assegnare (tramite sintassi ottale o mnemonica) seguiti dai nomi dei file interessati. 

Esistono due modi principali per invocare chmod:
- **Sintassi ottale**: utilizza tre cifre (es. chmod 755 file) che rappresentano i tre triplette di permessi. È un metodo assoluto: ogni invocazione imposta tutti i bit di permesso, sovrascrivendo i precedenti.
- **Sintassi mnemonica**: combina destinatari (, , , ), operatori (, , ) e permessi (, , , , ). A differenza dell'ottale, questo metodo permette di modificare singoli bit preservando gli altri. u g o a + - = r w x s t Inoltre, è possibile usare l'opzione -R per applicare le modifiche in modo ricorsivo a intere directory.

### 13. Chi può modificare la proprietà di un file (proprietario e gruppo proprietario), quali regole devono essere rispettate e quale comando esegue l'operazione?
La modifica della proprietà di un file segue regole rigide:
- **Proprietario (Owner)**: Solo l'utente root può cambiare il proprietario di un file. Un utente normale non può "cedere" la proprietà di un file a un altro utente.
- **Gruppo proprietario (Group owner)**: Un utente normale può cambiare il gruppo di un file solo se è il **proprietario** del file stesso e se appartiene personalmente al **gruppo di destinazione**. L'utente **root**, invece, può cambiare il gruppo in qualsiasi momento senza restrizioni.
- **Comando**: L'operazione viene eseguita tramite il comando chown

## FLASHCARD
### 9. Quali tipi di file supporta UNIX e in che modo i nove bit di permesso (rwx per utente, gruppo e altri) regolano le operazioni consentite su ciascun tipo?
X

### 10. perché lo smontaggio differito (umount -l) è considerato non sicuro, quale comando permette di identificare i processi che mantengono ancora riferimenti al filesystem occupato e come si può eseguire invece uno smontaggio pulito?
X

### 11. Quali sono gli scopi dei bit set-UID, set-GID e sticky, a quali file o directory regolari si applicano e in che modo modificano i controlli dei permessi?
X

### 12. Chi può modificare i bit di permesso di un file, quale comando può utilizzare e come viene invocato tale comando?
X

### 13. Chi può modificare la proprietà di un file (proprietario e gruppo proprietario), quali regole devono essere rispettate e quale comando esegue l'operazione?
X

