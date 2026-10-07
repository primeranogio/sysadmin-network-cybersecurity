## DOMANDE-RISPOSTE 
### 3. Cos'è un segnale, a quali processi un utente può inviare segnali e quale strategia dovrebbe adottare un amministratore per arrestare in modo affidabile un processo che si comporta in modo anomalo? 
Un segnale è una notifica inviata a un processo per informarlo che si è verificata una determinata condizione. Per quanto riguarda i permessi di invio:
- **Utente regolare**: può inviare segnali solo ai processi di cui è proprietario.
- **Root**: può inviare segnali a qualsiasi processo nel sistema.
La strategia consigliata per arrestare un processo consiste nell'utilizzare il comando kill. Di default, questo invia un segnale TERM (15), che richiede al processo di terminare l'esecuzione permettendogli di pulire il proprio stato e chiudere correttamente. Se il processo non risponde a TERM, l'amministratore può ricorrere al segnale KILL (9), che distrugge il processo a livello di kernel senza che questo possa ignorarlo o gestirlo.

I segnali possono essere inviati tra processi per comunicare, dal terminale di controllo (es. Ctrl-C invia INT), dall'amministratore o dal kernel stesso in caso di errori (es. divisione per zero). Mentre segnali come TERM o INT possono essere catturati o ignorati dal processo per permettere una chiusura pulita, i segnali KILL e STOP non possono essere né catturati, né bloccati, né ignorati, garantendo all'amministratore il controllo definitivo sul processo.

### 4. Quali sono i limiti degli strumenti indiretti come ps e i log quando si indaga su un processo sospetto, e cosa rivela strace che essi non possono mostrare?
Gli strumenti indiretti come il filesystem, i log e ps rivelano solo lo stato esterno di un processo e possono essere fuorvianti o persino falsificati deliberatamente. strace, invece, permette di visualizzare le chiamate di sistema (system calls) effettuate da un processo, insieme ai loro argomenti, ai codici di risultato e ai segnali ricevuti. Poiché un processo deve necessariamente eseguire chiamate di sistema per compiere qualsiasi azione significativa e queste vengono catturate direttamente a livello di kernel, il processo non può falsificarle.

Mentre ps legge informazioni da /proc che potrebbero non riflettere l'attività reale e i log dipendono dalla corretta segnalazione da parte del programma, strace intercetta la comunicazione tra lo spazio utente e lo spazio kernel. Questo fornisce un registro accurato e non manipolabile di ogni operazione che il processo tenta di eseguire, come l'apertura di file (openat), la lettura di dati (read) o la scrittura su terminale (write).

## FLASHCARD
### 3. Cos'è un segnale, a quali processi un utente può inviare segnali e quale strategia dovrebbe adottare un amministratore per arrestare in modo affidabile un processo che si comporta in modo anomalo? 
X

### 4. Quali sono i limiti degli strumenti indiretti come ps e i log quando si indaga su un processo sospetto, e cosa rivela strace che essi non possono mostrare?
X
