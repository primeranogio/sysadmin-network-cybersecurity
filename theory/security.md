## DOMANDE-RISPOSTE 
### 23. Cosa rappresenta la triade CIA nell'ambito della sicurezza informatica e qual è il significato di ciascun principio?
La triade CIA rappresenta i tre obiettivi fondamentali della sicurezza informatica: Riservatezza (Confidentiality), Integrità (Integrity) e Disponibilità (Availability).
- **Riservatezza**: l'accesso alle informazioni deve essere limitato esclusivamente a chi è autorizzato ad averlo (privacy dei dati).
- **Integrità**: l'informazione deve essere valida e non deve essere stata alterata in modo non autorizzato, garantendo autenticità e affidabilità.
- **Disponibilità**: l'informazione deve essere accessibile agli utenti autorizzati ogni volta che ne hanno bisogno.


### 24. Che cos'è l'ingegneria sociale, perché è particolarmente difficile difendersi e qual è una forma comune di questo attacco??
L'ingegneria sociale è l'uso dell'influenza psicologica per persuadere le persone a compiere azioni o rivelare informazioni, sfruttando i fattori umani anziché le vulnerabilità del software. È particolarmente difficile da difendere perché gli utenti umani e gli amministratori sono considerati gli anelli più deboli della catena di sicurezza; nessuna quantità di tecnologia può proteggere dall'elemento umano. Una forma comune di questo attacco è il **phishing**, in cui gli aggressori ingannano le persone tramite comunicazioni ingannevoli per indurre l'esecuzione di codice malevolo o la rivelazione di dati sensibili.

L'ingegneria sociale si concentra sulla manipolazione del comportamento umano per raccogliere informazioni, commettere frodi o ottenere l'accesso ai sistemi. Poiché si basa sull'inganno e non su bug tecnici, le tradizionali misure di sicurezza software spesso non sono sufficienti a prevenirla.

### 25. Che cos'è una vulnerabilità del software, qual è un esempio specifico di tale vulnerabilità e in che modo le pratiche di revisione del codice open source possono contribuire a ridurre queste vulnerabilità?
- **Definizione**: Una vulnerabilità è un difetto o una debolezza nel design, nell'implementazione o nella gestione di un sistema che può essere sfruttato da un attaccante per comprometterne la sicurezza.
- **Esempio**: Il buffer overflow (saturazione del buffer), che si verifica quando un programma scrive in un buffer di memoria più dati di quanti possa contenerne, sovrascrivendo la memoria adiacente.
- **Open-source**: La disponibilità pubblica del codice favorisce la sicurezza perché un numero maggiore di persone può esaminare il codice, aumentando la probabilità che qualcuno individui e segnali una debolezza.

### 26. Che cos'è un attacco DDoS e in che modo compromette tipicamente i sistemi presi di mira?
Un attacco **Distributed Denial-of-Service (DDoS)** mira a rendere un sistema non disponibile ai
suoi utenti intenzionali interrompendo temporaneamente o indefinitamente la sua disponibilità. Gli
attaccanti compromettono i sistemi presi di mira in due modi principali:
- **Network (D)DoS**: inondano il bersaglio con traffico di rete, esaurendo la sua larghezza di banda.
- **Endpoint (D)DoS**: esauriscono le risorse di sistema (come CPU o memoria) su cui sono ospitati i servizi o sfruttano falle per causare condizioni di crash persistente.Per condurre questi attacchi, gli aggressori tilizzano solitamente una "botnet", ovvero una rete di dispositivi infetti (come telecamere IP, stampanti o baby monitor) controllati da remoto.

### 27. Che cos'è l'insider abuse e perché è spesso più difficile da individuare rispetto agli attacchi esterni?
L'**insider abuse** (abuso interno) si verifica quando agenti fidati di un'organizzazione, come dipendenti, appaltatori o consulenti, abusano dei privilegi speciali che sono stati loro concessi. Questo tipo di attacco è spesso il più difficile da rilevare perché la maggior parte delle misure di sicurezza è progettata per difendersi da minacce esterne e risulta inefficace contro utenti a cui è già stato legittimamente concesso l'accesso al sistema.

Gli insider possono rubare dati, interrompere sistemi per guadagno finanziario o causare danni per motivi politici. Poiché agiscono dall'interno del perimetro di sicurezza, le loro attività malevole possono facilmente confondersi con le normali operazioni lavorative. Le dispense sottolineano inoltre che gli amministratori di sistema non devono mai installare "back door" (porte di servizio), poiché tali strumenti possono essere facilmente interpretati male o sfruttati da altri.

### 28. Perché mantenere i sistemi aggiornati è considerato il compito di sicurezza di maggior valore per un amministratore, quali rischi introducono le patch stesse e cosa dovrebbe includere una corretta procedura di patching?
Mantenere i sistemi aggiornati è considerato il compito di sicurezza più prezioso perché, sebbene le patch possano introdurre nuovi problemi, la stragrande maggioranza degli exploit sfrutta vulnerabilità vecchie e già note. Una corretta procedura di patching dovrebbe includere:
- Un **programma regolare** per le patch di routine (solitamente mensile).
- La capacità di applicare **patch critiche** con breve preavviso.
- Un **piano di cambiamento** che documenti l'impatto delle patch, i test post-installazione e le modalità di ripristino (back out).
- L'iscrizione a **mailing list e blog** di sicurezza specifici dei vendor per conoscere le patch pertinenti.
- Un **inventario** aggiornato delle applicazioni e dei sistemi operativi presenti nell'ambiente.

La gestione delle patch è fondamentale perché gli attaccanti contano sul fatto che molti sistemi rimangano vulnerabili a falle per le quali esiste già un rimedio. Automatizzare l'inventario e la gestione dell'infrastruttura aiuta a ridurre l'errore umano. Poiché ogni aggiornamento può potenzialmente causare instabilità è importante disporre di un piano documentato per testare le modifiche e poter tornare indietro in caso di problemi.

### 29. Che cos'è un backup nel contesto della sicurezza informatica e quali sono le raccomandazioni chiave per gestire efficacemente i backup?
Nel contesto della sicurezza, un **backup** è una copia dei dati informatici prelevata e conservata altrove, in modo da poter essere utilizzata per ripristinare l'originale dopo un evento di perdita di dati. Le raccomandazioni chiave per una gestione efficace includono:
- Assicurarsi che **tutti i filesystem** siano replicati.
- Conservare alcuni backup **off-site** (fuori sede).
- Proteggere i backup limitando e monitorando l'accesso ad essi.
- **Crittografare** i file di backup per evitare che diventino un rischio per la sicurezza.
- Effettuare backup regolari e testarne periodicamente il ripristino.

### 30. Cosa sono i virus e i worm informatici e quali sono le principali differenze tra questi due tipi di malware?
Un **virus** è un tipo di malware che, quando viene eseguito, si replica modificando altri programmi informatici e inserendo il proprio codice al loro interno. Un **worm** è invece un malware autonomo (standalone) che si replica per diffondersi ad altri computer senza la necessità di appoggiarsi a programmi ospite. La differenza fondamentale risiede nel fatto che i worm non richiedono un programma esistente per propagarsi, mentre i virus sì.

La distinzione principale riguarda il metodo di infezione: il virus deve "attaccarsi" a un programma legittimo per attivarsi e diffondersi, mentre il worm è un'entità indipendente. Sebbene i sistemi Linux siano storicamente meno colpiti da queste minacce grazie a un controllo degli accessi più rigido (senza privilegi di root la portata del malware è limitata), è talvolta consigliato l'uso di antivirus su Linux per proteggere i sistemi Windows collegati che potrebbero essere vulnerabili a malware specifici.

### 31. Che cos'è un rootkit, come funziona tipicamente e perché può essere particolarmente difficile da rilevare e rimuovere?
Un **rootkit** è un software (solitamente malevolo) progettato per consentire l'accesso a un computer o a parti del suo software che normalmente non sarebbero permesse, mascherando spesso la propria esistenza o quella di altri software. Essi funzionano a vari livelli di complessità: si va da semplici sostituzioni di applicazioni comuni (come versioni hackerate di ls e ps) fino a moduli del kernel estremamente sofisticati. Risultano difficili da gestire perché i rootkit più avanzati sono in grado di riconoscere i comuni programmi di rimozione e tentano di sovvertirli; inoltre, quelli a livello di kernel sono quasi impossibili da rilevare.

### 32. Quali sono le migliori pratiche e raccomandazioni per creare password sicure, gestire le password in modo efficace e implementare l’MFA?
Le raccomandazioni principali includono:
- **Creazione**: Ogni account deve avere una password non facilmente indovinabile. Le password più sicure sono sequenze casuali di lettere, numeri e punteggiatura, ma poiché sono difficili da memorizzare, la scelta migliore è una **passphrase** molto lunga, dato che la sicurezza aumenta esponenzialmente con la lunghezza.
- **Gestione**: Non utilizzare mai la stessa password per più di uno scopo. È consigliato l'uso di un **password vault** (gestore di password) che cripti le credenziali, accessibile tramite una singola master passphrase. Gli amministratori dovrebbero testare periodicamente la resistenza delle password degli utenti (specialmente quelli con privilegi sudo) usando strumenti di cracking offline come John the Ripper.
- **MFA**: L'autenticazione a più fattori è considerata un requisito minimo assoluto per portali esposti a Internet che forniscono privilegi amministrativi. Essa valida l'identità tramite "qualcosa che sai" (password) e "qualcosa che hai" (dispositivo fisico, impronta digitale, ecc.).

### 33. Che cos'è la crittografia a chiave simmetrica, come funziona e quali sono i suoi principali vantaggi e svantaggi?
**Definizione e Funzionamento**: Nella crittografia a chiave simmetrica, il mittente e il destinatario condividono un'unica chiave segreta (KAB) utilizzata sia per cifrare che per decifrare i messaggi. Le parti devono trovare un modo per scambiarsi privatamente questo segreto prima di iniziare la comunicazione.
- **Vantaggi**: Queste chiavi sono relativamente efficienti in termini di utilizzo della CPU e dimensioni dei dati crittografati (payload).
- **Svantaggi**: Il limite principale è la necessità di scambiarsi la chiave segreta in anticipo in modo sicuro; l'unico modo per farlo con sicurezza totale è incontrarsi di persona.

### 34. Che cos'è la crittografia a chiave pubblica, come funziona e quali sono i suoi principali vantaggi e svantaggi?
**Cos'è e come funziona**: Si basa su una coppia di chiavi generate da ogni utente: una **chiave privata** (K-1) che deve rimanere segreta, e una **chiave pubblica** (K), che può essere conosciuta da tutti. Per inviare un messaggio privato a Bob, Alice lo cifra con la chiave pubblica di Bob (KB); solo Bob, possedendo la relativa chiave privata (KB-1) potrà decifrarlo. Può essere usata anche per le **firme digitali**, cifrando un messaggio con la propria chiave privata affinché altri possano verificarne l'autenticità con la chiave pubblica corrispondente.
- **Vantaggi**: Elimina la necessità di scambiarsi segretamente e in anticipo una chiave condivisa, superando il limite principale della crittografia simmetrica.
- **Svantaggi**: Le prestazioni sono inferiori rispetto ai sistemi simmetrici; i cifrari asimmetrici sono computazionalmente pesanti e quindi poco pratici per cifrare grandi quantità di dati.

### 35. Che cos'è una CA, perché è necessaria in un'infrastruttura a chiave pubblica e perché è un bersaglio di alto valore?
Una **CA (Certificate Authority)** è una terza parte fidata che emette, firma e gestisce certificati digitali.

È necessaria per risolvere il problema della fiducia: un utente deve poter verificare che una chiave pubblica appartenga effettivamente al soggetto dichiarato e non a un malintenzionato. La CA valida questa associazione su scala globale.

È un **bersaglio di alto valore** per gli hacker perché l'intero modello si basa sulla fiducia implicita verso le CA; i sistemi operativi moderni ne considerano affidabili a centinaia per impostazione predefinita. Se una CA viene compromessa, l'intero sistema di fiducia globale viene interrotto.

## FLASHCARD
### 23. Cosa rappresenta la triade CIA nell'ambito della sicurezza informatica e qual è il significato di ciascun principio?
X

### 24. Che cos'è l'ingegneria sociale, perché è particolarmente difficile difendersi e qual è una forma comune di questo attacco??
X

### 25. Che cos'è una vulnerabilità del software, qual è un esempio specifico di tale vulnerabilità e in che modo le pratiche di revisione del codice open source possono contribuire a ridurre queste vulnerabilità?
X

### 26. Che cos'è un attacco DDoS e in che modo compromette tipicamente i sistemi presi di mira?
X

### 27. Che cos'è l'insider abuse e perché è spesso più difficile da individuare rispetto agli attacchi esterni?
X

### 28. Perché mantenere i sistemi aggiornati è considerato il compito di sicurezza di maggior valore per un amministratore, quali rischi introducono le patch stesse e cosa dovrebbe includere una corretta procedura di patching?
X

### 29. Che cos'è un backup nel contesto della sicurezza informatica e quali sono le raccomandazioni chiave per gestire efficacemente i backup?
X

### 30. Cosa sono i virus e i worm informatici e quali sono le principali differenze tra questi due tipi di malware?
X

### 31. Che cos'è un rootkit, come funziona tipicamente e perché può essere particolarmente difficile da rilevare e rimuovere?
X

### 33. Che cos'è la crittografia a chiave simmetrica, come funziona e quali sono i suoi principali vantaggi e svantaggi?
X

### 32. Quali sono le migliori pratiche e raccomandazioni per creare password sicure, gestire le password in modo efficace e implementare l’MFA?
X

### 33. Che cos'è la crittografia a chiave simmetrica, come funziona e quali sono i suoi principali vantaggi e svantaggi?
X

### 34. Che cos'è la crittografia a chiave pubblica, come funziona e quali sono i suoi principali vantaggi e svantaggi?
X

### 35. Che cos'è una CA, perché è necessaria in un'infrastruttura a chiave pubblica e perché è un bersaglio di alto valore?
X
