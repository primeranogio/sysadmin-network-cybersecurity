## DOMANDE-RISPOSTE 
1) **Perché gli aggressori manomettono i file di log, cos'è FSS e come consente agli
amministratori di rilevare tali manomissioni?** \
Gli aggressori manomettono i file di log principalmente per coprire le proprie tracce dopo
un'intrusione. Il Forward Secure Sealing (FSS) è una funzionalità del journal di systemd che
permette di rilevare se i log passati sono stati alterati. Il sistema utilizza due chiavi:
    - Chiave di sigillatura (sealing key): mantenuta sul sistema e usata per firmare le voci a intervalli regolari.
    - Chiave di verifica (verification key): conservata in modo sicuro dall'amministratore (non sul sistema locale) per verificare l'integrità dei sigilli passati.
firma periodicamente gruppi di voci recenti con la chiave di sigillatura, genera una nuova chiave e
scarta immediatamente quella vecchia systemd-journald. Poiché le chiavi passate vengono
eliminate, un attaccante che ottiene l'accesso al sistema può vedere solo la chiave di sigillatura
corrente; di conseguenza, non può modificare i log già sigillati senza che la manomissione sia
rilevata durante un controllo con la chiave di verifica esterna.

2) **Perché oggi gli amministratori sono tenuti a mantenere un repository di log centralizzato
e protetto, che ruolo svolgono i timestamp convalidati da NTP e quali daemon di logging
gestiscono la raccolta locale rispetto all'inoltro al repository centrale?** \
Gli amministratori oggi sono tenuti a mantenere repository di log centralizzati e protetti
("hardened") per conformarsi agli standard IT formali (come ISO/IEC 27001) e alle normative di
settore. I timestamp convalidati tramite il protocollo NTP (Network Time Protocol) sono
fondamentali per garantire la validità temporale dei log in tutta l'infrastruttura. Per quanto riguarda
i daemon:
    - systemd-journald: gestisce la raccolta e l'archiviazione locale dei messaggi di log in formato binario.
    - rsyslog (rsyslogd): si occupa di inoltrare i messaggi di log a una postazione centralizzata attraverso la rete.
La centralizzazione è necessaria perché il sistema di logging tradizionale di UNIX (syslog) era
rudimentale e non copriva tutte le esigenze di gestione dei log su larga scala. Inoltre, l'inoltro dei
log a un server remoto sicuro impedisce agli aggressori di cancellare le proprie tracce
manomettendo i file locali su un sistema compromesso. L'uso di NTP assicura che i messaggi
provenienti da centinaia o migliaia di server diversi abbiano riferimenti temporali coerenti e
sincronizzati, facilitando l'analisi e il monitoraggio.

## FLASHCARD
1) **Perché gli aggressori manomettono i file di log, cos'è FSS e come consente agli
amministratori di rilevare tali manomissioni?** \
Writing ...

3) **Perché oggi gli amministratori sono tenuti a mantenere un repository di log centralizzato
e protetto, che ruolo svolgono i timestamp convalidati da NTP e quali daemon di logging
gestiscono la raccolta locale rispetto all'inoltro al repository centrale?** \
Writing ...
