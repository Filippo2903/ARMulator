# Dizionario in italiano
"""
The Italian dictionary for translation
"""
dict = {
    "abstractOp": [
        "Errore interno: ",
        "<li>Verifica se la condizione {} è soddisfatta</li>\n",
        "L'istruzione è invalida (la condizione richiesta non esiste)"
    ],

    "branchOp": [
        "Il bytecode a questo indirizzo non corrisponde a nessuna istruzione valida (1)",
        "<li>Copia il valore di {}-4 (l'indirizzo della prossima istruzione) in {}</li>\n",
        "<li>Sottrae il valore {} da {}</li>\n",
        "<li>Aggiunge il valore {} a {}</li>\n",
        "<li>Copia il valore da {} in {}</li>\n"
    ],

    "dataOp": [
        "Il bytecode a questo indirizzo non corrisponde a nessuna istruzione valida (2)",
        "La costante {}",
        "Il registro {} {}",
        "<li>Esegue un'operazione AND tra:</li>\n",
        "<li>Esegue un'operazione OR esclusivo (XOR) tra:</li>\n",
        "<li>Esegue una sottrazione (A-B) tra:</li>\n",
        "<li>Esegue una sottrazione inversa (B-A) tra:</li>\n",
        "<li>Esegue un'addizione (A+B) tra:</li>\n",
        "<li>Esegue un'addizione con riporto (A+B+carry) tra:</li>\n",
        "<li>Esegue una sottrazione con prestito (A-B+carry) tra:</li>\n",
        "<li>Esegue una sottrazione inversa con prestito (B-A+carry) tra:</li>\n",
        "<li>Esegue un'operazione OR tra:</li>\n",
        "<li>Legge il valore di:</li>\n",
        "<li>Esegue un'operazione AND NOT tra:</li>\n",
        "<li>Esegue un'operazione NOT su:</li>\n",
        "Mnemotecnico non valido: {}",
        "<ol type=\"A\"><li>Registro {}</li><li>{}</li></ol>\n",
        "<ol type=\"A\"><li>Registro {}</li>\n",
        "<li>Copia il valore attuale di SPSR in CPSR</li>\n",
        "<li>Aggiorna i flag dell'ALU in base al risultato dell'operazione</li>\n",
        "<li>Scrive il risultato in {}</li>",
        "Mnemotecnico non valido: {}",
        "L'uso del registro PC come destinazione con aggiornamento dei flag è vietato in modalità User!",
        "SPSR dovrebbe essere copiato in CPSR, ma la modalità contenuta in SPSR è invalida!"
    ],

    "halfSignedMemOp": [
        "Il bytecode a questo indirizzo non corrisponde a nessuna istruzione valida",
        "<li>Usa il valore del registro {} come indirizzo base</li>\n",
        "<li>Aggiunge la costante {} all'indirizzo base</li>\n",
        "<li>Sottrae la costante {} dall'indirizzo base</li>\n",
        "<li>Aggiunge il registro {} all'indirizzo base</li>\n",
        "<li>Sottrae il registro {} dall'indirizzo base</li>\n",
        "<li>Legge {} dall'indirizzo ottenuto (pre-incremento) e memorizza il risultato in {} (LDR)</li>\n",
        "<li>Legge {} dall'indirizzo base e memorizza il risultato in {} (LDR)</li>\n",
        "<li>Copia il valore del bit {} nei bit da {} a 31 del registro di destinazione</li>\n",
        " del byte meno significativo",
        " dei due byte meno significativi",
        "<li>Copia il valore",
        " del registro {} in memoria, all'indirizzo ottenuto nel passo precedente (pre-incremento), su {} (STR)</li>\n",
        "<li>Copia il valore",
        " del registro {} in memoria, all'indirizzo base, su {} (STR)</li>\n",
        "<li>Scrive l'indirizzo effettivo nel registro base {} (modalità writeback)</li>\n",
        "Tentativo di lettura di {} byte da un indirizzo non valido {}: memoria non inizializzata"
    ],

    "memOp": [
        "Il bytecode a questo indirizzo non corrisponde a nessuna istruzione valida",
        "<li>Usa il valore del registro {} come indirizzo base</li>\n",
        "<li>Aggiunge la costante {} all'indirizzo base</li>\n",
        "<li>Sottrae la costante {} dall'indirizzo base</li>\n",
        "<li>Aggiunge il registro {} {} all'indirizzo base</li>\n",
        "<li>Sottrae il registro {} {} dall'indirizzo base</li>\n",
        "1 byte",
        "{} byte",
        "<li>Legge {} dall'indirizzo ottenuto (pre-incremento) e memorizza il risultato in {} (LDR)</li>\n",
        "<li>Legge {} dall'indirizzo base e memorizza il risultato in {} (LDR)</li>\n",
        "<li>Copia il valore del registro {} in memoria, all'indirizzo ottenuto nel passo precedente (pre-incremento), su {} (STR)</li>\n",
        "<li>Copia il valore del registro {} in memoria, all'indirizzo base, su {} (STR)</li>\n",
        "<li>Scrive l'indirizzo effettivo nel registro base {} (modalità writeback)</li>\n",
        "Tentativo di lettura di {} byte da un indirizzo {} non valido: memoria non inizializzata"
    ],

    "mulLongOp": [
        "Il bytecode a questo indirizzo non corrisponde a nessuna istruzione valida",
        "<li>Esegue una moltiplicazione e un'addizione {} su 64 bit (A*B+[C,D]) tra:</li>\n",
        "<ol type=\"A\"><li>Registro {}</li>\n",
        "<li>Registro {}</li>\n",
        "<li>Registro {}</li>\n",
        "<li>Registro {}</li></ol>\n",
        "<li>Esegue una moltiplicazione {} (A*B) tra:</li>\n",
        "<ol type=\"A\"><li>Registro {}</li>\n",
        "<li>Registro {}</li></ol>\n",
        "<li>Aggiorna i flag dell'ALU in base al risultato dell'operazione</li>\n",
        "<li>Scrive i 32 bit più significativi del risultato in R{} e i 32 meno significativi in R{}</li>"
    ],

    "mulOp": [
        "Il bytecode a questo indirizzo non corrisponde a nessuna istruzione valida",
        "<li>Esegue una moltiplicazione seguita da un'addizione (A*B+C) tra:</li>\n",
        "<ol type=\"A\"><li>Registro {}</li>\n",
        "<li>Registro {}</li>\n",
        "<li>Registro {}</li></ol>\n",
        "<li>Aggiorna i flag dell'ALU in base al risultato dell'operazione</li>\n",
        "<li>Esegue una moltiplicazione (A*B) tra:</li>\n",
        "<ol type=\"A\"><li>Registro {}</li>\n",
        "<li>Registro {}</li></ol>\n",
        "<li>Aggiorna i flag dell'ALU in base al risultato dell'operazione</li>\n",
        "<li>Scrive il risultato in R{}</li>"
    ],

    "multipleMemOp": [
        "Il bytecode a questo indirizzo non corrisponde a nessuna istruzione valida",
        "<li>Legge il valore di SP</li>\n",
        "<li>Per ogni registro nella lista seguente, memorizza il valore contenuto all'indirizzo puntato da SP nel registro, poi incrementa SP di 4.</li>\n",
        "<li>Legge il valore di SP</li>\n",
        "<li>Per ogni registro nella lista seguente, decrementa SP di 4, poi memorizza il valore del registro all'indirizzo puntato da SP.</li>\n",
        "<li>Legge il valore di {}</li>\n",
        "<li>Per ogni registro nella lista seguente, memorizza il valore contenuto all'indirizzo puntato da {reg} nel registro, poi {incmode} {reg} di 4.</li>\n",
        "<li>Legge il valore di {}</li>\n",
        "<li>Per ogni registro nella lista seguente, {incmode} {reg} di 4, poi memorizza il valore del registro all'indirizzo puntato da {reg}.</li>\n",
        "<li>Copia l’SPSR corrente nel CPSR</li>\n"
    ],

    "nopOp": [
        "Il bytecode a questo indirizzo non corrisponde a nessuna istruzione valida",
        "<li>Non fa nulla</li><li>Davvero, assolutamente nulla</li>"
    ],

    "psrOp": [
        "Il bytecode a questo indirizzo non corrisponde a nessuna istruzione valida",
        "<li>Scrive la costante {} in {}</li>\n",
        "<li>Legge il valore di {}</li>\n",
        "<li>Scrive i 4 bit più significativi di questo valore (che corrispondono ai flag) in {}</li>\n",
        "<li>Legge il valore di {}</li>\n",
        "<li>Scrive questo valore in {}</li>\n",
        "<li>Legge il valore di {}</li>\n",
        "<li>Scrive il risultato in {}</li>\n",
        "Errore: scrittura dello SPSR in modalità 'User' (questa modalità non ha un registro SPSR)",
        "Errore: i bit ({:05b}) della modalità di {} non corrispondono a nessuna modalità valida!",
        "Errore: tentativo di cambiare la modalità del processore da una modalità non privilegiata!",
        "Errore: lettura dello SPSR in modalità 'User' (questa modalità non ha un registro SPSR)"
    ],

    "softInterruptOp": [
        "Il bytecode a questo indirizzo non corrisponde a nessuna istruzione valida",
        "<li>Cambia banca di registri in SVC</li>\n",
        "<li>Copia il CPSR in SPSR_svc</li>\n",
        "<li>Copia il PC in LR_svc</li>\n",
        "<li>Assegna 0x08 al PC</li>\n"
    ],

    "swapOp": [
        "Il bytecode a questo indirizzo non corrisponde a nessuna istruzione valida",
        "<li>Legge {} dall'indirizzo contenuto in {}</li>\n",
        "<li>Scrive il byte meno significativo del registro {} all'indirizzo contenuto in {}</li>\n",
        "<li>Scrive il byte meno significativo del valore originale in memoria in {}</li>\n",
        "<li>Scrive il valore del registro {} all'indirizzo contenuto in {}</li>\n",
        "<li>Scrive in {} il valore originale dell'indirizzo contenuto in {}</li>\n",
        "Tentativo di lettura di {} byte da un indirizzo {} non valido: memoria non inizializzata"
    ],

    "utils": [
        "spostato a sinistra (modalità LSL)",
        "spostato a destra (modalità LSR)",
        "spostato a destra (modalità ASR)",
        "ruotato a destra con riporto (modalità RRX)",
        "ruotato a destra (modalità ROR)",
        " di {} {}",
        " del numero di posizioni contenuto in {}"
    ],

    "assembler": [
        "Errore di sintassi",
        "Errore di intervallo",
        "Istruzione non valida",
        "Il comportamento attuale del PC non è ancora implementato",
        "Formato dell'istruzione non valido",
        "Impossibile interpretare l'istruzione",
        "Istruzione non valida",
        "Non puoi scrivere istruzioni prima della prima parola chiave SECTION; se vuoi testare un frammento di codice, non dichiarare alcuna sezione.",
        "La sezione INTVEC deve essere definita prima delle sezioni CODE e DATA!",
        "La sezione CODE deve essere definita prima della sezione DATA!",
        "La sezione '{}' è definita due volte!",
        "L'etichetta '{}' è definita due volte (prima definizione alla riga {})",
        "La dichiarazione su questa riga fa traboccare la sezione INTVEC nella sezione CODE. Verifica di allocare il numero corretto di byte (massimo 128 byte per tutta la sezione INTVEC).",
        "Il codice richiede un'allocazione totale superiore a {} byte di memoria, il che non è valido.",
        "La sezione INTVEC non è dichiarata da nessuna parte (usa 'SECTION INTVEC' all'inizio del codice)!",
        "La sezione CODE non è dichiarata da nessuna parte (usa 'SECTION CODE')!",
        "La sezione DATA non è dichiarata da nessuna parte (usa 'SECTION DATA' alla fine del codice)!",
        "Questa riga richiede l'indirizzo dell'etichetta {}, ma non è dichiarata da nessuna parte",
        "L'etichetta {} non è dichiarata da nessuna parte",
        "Accesso all'indirizzo identificato dall'etichetta {} troppo distante (scostamento di {} byte) per poter essere codificato",
        "L'etichetta {} non è dichiarata da nessuna parte",
        "L'etichetta {} corrisponde a uno scostamento di {} byte, che non è un multiplo di 4, come richiesto da ARM"
    ],

    "components": [
        "Modalità non valida '{}'",
        "Il registro SPSR non esiste in modalità 'User'!",
        "Il registro SPSR non esiste in modalità 'User'!",
        "Tentativo di lettura di un'istruzione da un indirizzo non inizializzato: {}",
        "Accesso di lettura alla memoria fallito all'indirizzo {}",
        "Accesso non valido per una scrittura di dimensione {} all'indirizzo {}"
    ],

    "history": [
        "Fine della cronologia raggiunta, impossibile risalire più in alto!"
    ],

    "mainweb": [
        "Informazioni non disponibili",
        "Si prega di assemblare il codice prima di eseguire questa operazione.",
        "Indirizzo di memoria non valido",
        "Valore non valido: {}",
        "Registro non valido: {}",
        "Valore non valido: {}"
    ],

    "simulator": [
        "Errore: il valore di PC ({}) non è valido (deve essere un multiplo di 4)!",
        "Informazioni non disponibili",
        "Indirizzo dell'istruzione",
        "Errore: {} dovrebbe valere {} (il valore del registro R{}), ma vale {}\n",
        "Errore: {} dovrebbe valere {}, ma vale {}\n",
        "Errore: l'indirizzo di memoria {} dovrebbe contenere {} (il valore del registro R{}), ma contiene {}\n",
        "Errore: l'indirizzo di memoria {} dovrebbe contenere {}, ma contiene {}\n",
        "Errore: il flag {} dovrebbe indicare {}, ma indica {}\n",
        "Aserzione sconosciuta o impossibile da interpretare: ({}, {})!"
    ],

    "tokenizer": [
        "(01) Carattere non valido (riga {}, colonna {}) : {}",
        "(02) Carattere non valido (riga {}, colonna {}) : {}",
        "(03) Carattere non valido (riga {}, colonna {}) : {}",
        "(04) Carattere non valido (riga {}, colonna {}) : {}",
        "(05) Carattere non valido (riga {}, colonna {}) : {}",
        "(06) Carattere non valido (riga {}, colonna {}) : {}",
        "(07) Carattere non valido (riga {}, colonna {}) : {}",
        "(08) Carattere non valido (riga {}, colonna {}) : {}",
        "(09) Carattere non valido (riga {}, colonna {}) : {}",
        "(10) Carattere non valido (riga {}, colonna {}) : {}",
        "(11) Carattere non valido (riga {}, colonna {}) : {}",
        "(12) Carattere non valido (riga {}, colonna {}) : {}",
        "(12b) Carattere non valido (riga {}, colonna {}) : {}",
        "(13) Carattere non valido (riga {}, colonna {}) : {}",
        "(07b) Carattere non valido (riga {}, colonna {}) : {}",
        "(14) Carattere non valido (riga {}, colonna {}) : {}",
        "(15) Carattere non valido (riga {}, colonna {}) : {}",
        "(16) Carattere non valido (riga {}, colonna {}) : {}",
        "(17) Carattere non valido (riga {}, colonna {}) : {}",
        "(18) Carattere non valido (riga {}, colonna {}) : {}",
        "(19) Carattere non valido (riga {}, colonna {}) : {}",
        "(20) Carattere non valido (riga {}, colonna {}) : {}",
        "(21) Carattere non valido (riga {}, colonna {}) : {}",
        "(22) Carattere non valido (riga {}, colonna {}) : {}",
        "(23) Carattere non valido (riga {}, colonna {}) : {}",
        "(24) Carattere non valido (riga {}, colonna {}) : {}",
        "(25) Carattere non valido (riga {}, colonna {}) : {}",
        "(26) Carattere non valido (riga {}, colonna {}) : {}",
        "(G) Carattere non valido (riga {}, colonna {}) : {}"
    ],

    "yaccparser": [
        "Un'etichetta deve iniziare con una lettera maiuscola o minuscola (e non con un numero)",
        "Istruzione invalida: \"{}\". Si prega di fare riferimento al manuale del simulatore per la lista delle istruzioni accettate.",
        "Il registro R{}{} non esiste",
        "L'istruzione {} richiede un registro come primo argomento",
        "I registri e/o le costanti usati in un'operazione devono essere separati da una virgola",
        "I registri e/o le costanti usati in un'operazione devono essere separati da una virgola",
        "L'istruzione {} richiede 3 argomenti",
        "Il registro R{}{} non esiste",
        "Il registro R{}{} non esiste",
        "TEST",
        "Impossibile codificare la seguente costante o il suo inverso in un'istruzione {}: {}",
        "Impossibile codificare la seguente costante in un'istruzione {}: {}",
        "Il registro R{}{} non esiste",
        "È richiesta una virgola prima dell'operazione di spostamento",
        "Spostamento {} invalido senza un parametro (registro o costante) che indichi lo spostamento",
        "Impossibile codificare uno spostamento negativo ({}) in un'istruzione (usa un altro operatore di spostamento per ottenere lo stesso effetto)",
        "Impossibile codificare lo spostamento {} in un'istruzione (deve essere inferiore a 32)",
        "Un'istruzione {} non accetta uno spostamento sul suo registro di offset",
        "Lo spostamento richiesto di {} nell'istruzione è troppo grande per essere codificato (deve essere inferiore a 256)",
        "È vietato usare STR con un indirizzo di etichetta come destinazione. Ad esempio, 'STR R0, a' è valido, ma non 'STR R0, =a'.",
        "È vietato usare PC come registro di base quando il writeback è abilitato.",
        "In modalità writeback, è vietato usare lo stesso registro come destinazione e indirizzo di base.",
        "Lo spostamento richiesto di {} nell'istruzione è troppo grande per essere codificato (deve essere inferiore a 4096)",
        "Un'operazione di spostamento deve essere preceduta da una virgola.",
        "PC non può essere usato come registro di spostamento!",
        "È vietato usare PC come registro di base in modalità post-incremento!",
        "Lo spostamento richiesto di {} nell'istruzione è troppo grande per essere codificato (deve essere inferiore a 4096)",
        "La destinazione di un salto deve essere un'etichetta (o, per BX, un registro). Un'etichetta non può iniziare con un numero.",
        "Un'istruzione {} deve specificare almeno un registro nella sua lista.",
        "È vietato usare PC come registro di base in un'operazione di memoria multipla!",
        "Impossibile assegnare direttamente una costante a un registro di stato. Solo i flag possono essere modificati direttamente, aggiungendo il suffisso _flg al registro di stato.",
        "Impossibile codificare la seguente costante in un'istruzione {}: {}",
        "Un'istruzione {} non può ricevere una costante come ultimo argomento, solo un registro.",
        "Un'istruzione {} non può ricevere più di 3 registri come argomenti.",
        "Un'istruzione {} non può ricevere una costante come ultimo argomento, solo un registro.",
        "Il registro PC non può essere usato.",
        "Il registro R{} non può essere usato più di una volta.",
        "Una variabile può avere le seguenti dimensioni (in bit): 8, 16 o 32. {} non è una dimensione valida",
        "Un'assegnazione di variabile deve essere seguita da una dimensione in bit (ad esempio ASSIGN32 o ASSIGN8)",
        "Una variabile può avere le seguenti dimensioni (in bit): 8, 16 o 32. {} non è una dimensione valida",
        "Un'allocazione di variabile può essere seguita solo dal numero di elementi. Usa ASSIGN se vuoi assegnare valori specifici.",
        "Richiesta di allocazione di memoria troppo grande. Il massimo consentito è 8 KB (8192 byte), ma la dichiarazione richiede {} byte.",
        "Un'allocazione di variabile deve essere seguita da una dimensione in bit (ad esempio ALLOC32 o ALLOC8)"
    ]
}
