## DOMANDE-RISPOSTE 
### 14. Come può un amministratore impostare una password iniziale per un nuovo account, perché è rischioso rimandare questa operazione al primo login dell'utente e quale approccio è raccomandato?
Un amministratore può impostare una password iniziale per un nuovo account utilizzando il comando passwd (ad esempio, sudo passwd hilbert). È rischioso rimandare l'impostazione della password al primo login dell'utente perché alcuni sistemi automatizzati creano account senza password iniziale, permettendo a chiunque riesca a indovinare il nome dell'account di "dirottarlo" (hijack) prima che l'utente previsto abbia la possibilità di accedere. L'approccio raccomandato è impostare una password iniziale e poi utilizzare il comando chage -d 0 <utente> per forzare l'utente a cambiarla immediatamente al primo accesso.

### 15. Come può un amministratore bloccare e sbloccare l'account di un utente, come funziona il meccanismo sottostante a livello di /etc/shadow e quali sono i limiti di questo approccio?
Un amministratore può bloccare temporaneamente l'accesso di un utente utilizzando il comando usermod -L (lock) e sbloccarlo con usermod -U (unlock). A livello di sistema, questo comando inserisce un punto esclamativo (!) all'inizio della password cifrata (hash) dell'utente all'interno del file /etc/shadow.

L'aggiunta del carattere ! rende l'hash della password non valido, facendo fallire ogni tentativo di login basato su password. Tuttavia, questo approccio presenta dei limiti significativi:
- Mancanza di feedback: L'utente non riceve alcuna notifica del blocco né una spiegazione del motivo per cui l'account non funziona più.
- Accessi alternativi: Il blocco della password non impedisce l'accesso tramite metodi che non la richiedono esplicitamente, come ad esempio le connessioni SSH basate su chiavi pubbliche, che potrebbero continuare a funzionare nonostante il blocco in /etc/shadow.

## FLASHCARD
### 14. Come può un amministratore impostare una password iniziale per un nuovo account, perché è rischioso rimandare questa operazione al primo login dell'utente e quale approccio è raccomandato?
X

### 15. Come può un amministratore bloccare e sbloccare l'account di un utente, come funziona il meccanismo sottostante a livello di /etc/shadow e quali sono i limiti di questo approccio?
X
