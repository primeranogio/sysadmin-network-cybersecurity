## DOMANDE-RISPOSTE 
### 16. Cos'è un firewall, come funziona uno schema di filtraggio a due fasi e che ruolo svolge una DMZ?
- Un firewall a filtraggio di pacchetti è un sistema che limita il tipo di traffico che può passare attraverso un gateway basandosi sulle informazioni contenute nell'intestazione (header) del pacchetto.
- Un schema di filtraggio a due stadi prevede l'uso di due filtri distinti: il primo funge da gateway verso Internet, mentre il secondo è posizionato tra il gateway esterno e il resto della rete locale.
- La DMZ (Demilitarized Zone) è il segmento di rete che si trova tra questi due filtri. Il suo ruolo è quello di ospitare i sistemi che devono ricevere connessioni dall'esterno (come i server web), mantenendoli separati dal resto della rete locale per motivi di sicurezza.


### 17. Cos'è lo spoofing ARP, quali vulnerabilità del protocollo ARP sfrutta e che tipo di attacchi consente?
L'ARP spoofing è un attacco in cui un malintenzionato invia messaggi ARP (Address Resolution Protocol) falsificati all'interno di una rete locale. Questo attacco sfrutta due debolezze intrinseche del protocollo ARP:
- Mancanza di autenticazione: Non esiste un meccanismo per verificare l'identità del mittente di una risposta ARP.
- Natura stateless: Le risposte ARP vengono automaticamente salvate nella cache dei computer riceventi, indipendentemente dal fatto che abbiano effettivamente inviato una richiesta corrispondente.

Tale tecnica abilita principalmente attacchi di tipo Man-in-the-middle (MITM), permettendo all'aggressore di intercettare o alterare le comunicazioni tra una vittima e un altro host (spesso il gateway predefinito).

### 18. Come può un aggressore sfruttare i messaggi di reindirizzamento ICMP, quali debolezze del protocollo ICMP lo rendono possibile e che tipo di attacchi permette?
Un attaccante può abusare dei messaggi ICMP redirect inviando pacchetti falsificati che istruiscono una vittima a utilizzare l'indirizzo IP dell'attaccante come gateway per una specifica destinazione (ad esempio, un DNS pubblico). Questa vulnerabilità è possibile perché i messaggi ICMP redirect non contengono informazioni di autenticazione. Tale abuso abilita attacchi di tipo Man-in-the-middle (MITM), permettendo all'attaccante di intercettare o alterare le comunicazioni tra la vittima e la sua destinazione reale.

I messaggi ICMP redirect sono nati originariamente per ottimizzare il routing: un router informa un host che esiste un percorso più efficiente per una certa destinazione sulla stessa rete locale. Poiché il protocollo si fida della notifica senza verificarne l'origine, il sistema operativo della vittima aggiorna automaticamente la propria tabella di routing, deviando il traffico verso l'host indicato dall'attaccante.

### 19. Cos'è l'inoltro IP e perché di solito è sconsigliabile lasciarlo attivo su host che non sono progettati per fungere da router?
L'IP forwarding è una funzionalità del kernel che permette a un host di agire come un router. In questa modalità, l'host può accettare pacchetti di terze parti su un'interfaccia di rete, individuare il gateway o l'host di destinazione su un'altra interfaccia e ritrasmettere i pacchetti. È generalmente considerato non sicuro lasciarlo abilitato su host che non devono fungere da router perché questi sistemi possono essere costretti a compromettere la sicurezza facendo apparire i pacchetti esterni come se provenissero dall'interno della rete, eludendo così scanner di rete e filtri di pacchetti.

Se l'IP forwarding è attivo, un attaccante può sfruttare tecniche come l'ARP spoofing o gli ICMP redirect per deviare il traffico verso l'host compromesso invece che verso il gateway legittimo. Di default, questa funzione è disabilitata in Linux (valore 0 in /proc/sys/net/ipv4/ip_forward) e la raccomandazione è di mantenerla spenta a meno che il sistema non debba effettivamente operare come router.

### 20. Che cos'è lo spoofing IP e quali difese si possono adottare per contrastarlo?
L'IP spoofing consiste nel falsificare l'indirizzo IP sorgente di un pacchetto. Mentre normalmente l'indirizzo viene inserito dal kernel, un software che utilizza un "raw socket" (SOCK_RAW) può inserire qualsiasi indirizzo desideri. Le principali difese includono:
- Filtraggio in uscita: Bloccare i pacchetti in uscita il cui indirizzo sorgente non appartiene al proprio spazio di indirizzi, per evitare che attacchi esterni sembrino originati dalla rete interna.
- Unicast Reverse Path Forwarding (uRPF): Una tecnica che istruisce il gateway a scartare un pacchetto se il suo indirizzo IP sorgente non è raggiungibile attraverso l'interfaccia da cui il pacchetto è arrivato (modalità strict). Di default, Linux utilizza la modalità loose, che accetta il pacchetto se l'indirizzo sorgente è raggiungibile tramite una qualsiasi interfaccia nella tabella di routing.

### 21. Cos'è il routing di origine IPv4 e come può un attaccante sfruttarlo?
Il source routing IPv4 è un meccanismo che permette di specificare una serie esplicita di gateway che un pacchetto deve attraversare nel suo percorso verso la destinazione. Un attaccante può sfruttarlo per instradare i pacchetti in modo che sembrino originati dall'interno della rete locale anziché da Internet, riuscendo così a eludere i filtri del firewall. 

Originariamente concepito per agevolare i test di rete, il source routing scavalca i normali algoritmi di instradamento dei gateway. Se un firewall è configurato per fidarsi del traffico proveniente da determinati indirizzi interni, un pacchetto esterno con source routing attivo può "fingere" tale provenienza e scivolare attraverso le protezioni. Per questo motivo, la raccomandazione è di configurare il sistema affinché non accetti né inoltri pacchetti con source routing (utilizzando parametri sysctlVenire ).accept_source_route=0

### 22. Come funziona un attacco broadcast ping come l'attacco Smurf? Dove entra in gioco lo spoofing IP? E come si difende Linux da esso di default?
Un attacco di tipo "broadcast ping", come lo smurf attack, funziona inviando richieste ICMP echo (ping) all'indirizzo di broadcast di una rete, il che causa la consegna del pacchetto a ogni host presente su quella rete. Lo **spoofing dell'IP** entra in gioco perché l'aggressore falsifica l'indirizzo sorgente del pacchetto ping, inserendo l'indirizzo IP della vittima. Di conseguenza, tutti gli host della rete rispondono contemporaneamente all'indirizzo della vittima, scatenando un attacco Distributed Denial-of-Service (DDoS). Linux si difende da questo attacco ignorando i ping di broadcast per impostazione predefinita.

L'attacco sfrutta la moltiplicazione del traffico: un singolo pacchetto inviato dall'attaccante genera centinaia o migliaia di risposte dirette verso la vittima. La difesa di Linux è implementata tramite il parametro del kernel net.ipv4.icmp_echo_ignore_broadcasts, che ha valore 1 di default, istruendo lo stack di rete a non rispondere a messaggi ICMP inviati a indirizzi broadcast o multicast.

## FLASHCARD
### 16. Cos'è un firewall, come funziona uno schema di filtraggio a due fasi e che ruolo svolge una DMZ?
X

### 17. Cos'è lo spoofing ARP, quali vulnerabilità del protocollo ARP sfrutta e che tipo di attacchi consente?
X

### 18. Come può un aggressore sfruttare i messaggi di reindirizzamento ICMP, quali debolezze del protocollo ICMP lo rendono possibile e che tipo di attacchi permette?
X

### 19. Cos'è l'inoltro IP e perché di solito è sconsigliabile lasciarlo attivo su host che non sono progettati per fungere da router?
X

### 20. Che cos'è lo spoofing IP e quali difese si possono adottare per contrastarlo?
X

### 21. Cos'è il routing di origine IPv4 e come può un attaccante sfruttarlo?
X

### 22. Come funziona un attacco broadcast ping come l'attacco Smurf? Dove entra in gioco lo spoofing IP? E come si difende Linux da esso di default?
X

