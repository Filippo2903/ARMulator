# Tesina - Emulatore ARMv4
###### _Università degli studi di Roma Tor Vergata<br>CdL Informatica<br>A.A. 2024/2025 - Architettura dei Sistemi di Elaborazione - Prof. A. Simonetta, Ing. E. Iannaccone<br>Filippo Gentili, Thomas Infascelli, Matteo Sorvillo, Alessandro Stella_
## Introduzione

Questo progetto nasce dall'esigenza didattica di disporre di un'alternativa nativa e mantenibile a [**CPUlator**](https://cpulator.01xz.net/), simulatore e debugger di sistemi informatici.<br>
Il progetto è basato su [**epater**](https://github.com/mgard/epater), un assemblatore ed emulatore ARMv4.<br>
Il codice originale è stato aggiornato, ottimizzato e reso compatibile con Windows e Linux.


## Requisiti
- Fornire un'alternativa nativa a CPUlator
- Utilizzare [epater](https://github.com/mgard/epater) come punto di partenza
   * Rendere il progetto iniziale utilizzabile
   * Comprenderne potenzialità e limiti
   * Rendere l'installazione del software chiara e semplice



## Il Progetto

Si tratta di un emulatore ARM, scritto in python, a scopi didattici con interfaccia grafica interattiva. Anziché _**interpretare**_ il codice ARM, questo software è in grado di _**emulare**_ direttamente una CPU ARM.<br>In particolare, è un assemblatore e simulatore composto in tre parti:

1. Assemblatore che traduce codice ARM in bytecode ARMv4
2. Emulatore ARMv4
3. Interfaccia grafica composta da editor di testo, tabella dei registri, tabella degli indirizzi di memoria e varie funzioni utili al debug e allo studio

## Funzionalità supportate

- Tutte le istruzioni dell'architettura ARMv4 
- Interrupt (software tramite SWI o hardware di tipo timer con IRQ o FIQ)
- Esecuzione step-by-step e continua
- Debugger integrato, incluso reverse-debugging
- Interfaccia grafica moderna e interattiva
- Salvataggio e caricamento fino ad un massimo di 10 sessioni


## Modifiche principali

- **Aggiornamento dipendenze** nel file `requirements.txt`
- **Parallelizzazione dei server** HTTP e WebSocket
- **Ottimizzazione aggiornamento GUI**
  - **Editor di testo velocizzato**
- **Compilazione in eseguibile** tramite [py-to-exe](https://pypi.org/project/auto-py-to-exe) 
- **Distribuzione con Installer** 
- **Modernizzazione GUI** e miglioramenti all'usabilità
- **Supporto multilingua integrato**
   - **Aggiunta lingua italiana ed inglese**
- Accesso all'emulatore su server privato

## Installazione

Per installare l'emulatore è sufficiente scaricare l'installer corrispondente al vostro sistema operativo.<br>
[Windows]() [Linux]()<br> 

### Requisiti di sistema

- Windows 11 o qualsiasi distribuzione Linux
- Python ver 3.12 (per sviluppatori)

### Installazione per Sviluppatori

```bash
git clone https://github.com/NOME_UTENTE/NOME_REPO
pip install -r requirements.txt

```

## Accesso Server
Per accedere all'emulatore sul server privato, utilizzare il seguente indirizzo:<br>
147.93.63.174:8888

## Utilizzo

1. Aprire l'applicazione
2. Caricare un file `.txt` con codice assembly ARM oppure utilizzare direttamente l'editor di testo
3. Usare la GUI per:
   - Modificare il codice
   - Modificare manualmente memoria e registri
   - Impostare breakpoint
   - Eseguire il programma (step/continuo)
4. Visualizzare: registri, memoria, flags, output ed errori


## Differenze rispetto al progetto originale

| Aspetto                | Epater Originale           | Versione tesina             |
|------------------------|----------------------------|-----------------------------|
| Esecuzione             | Web-based                  | Applicazione nativa         |
| GUI                    | Obsoleta                   | Modernizzata                |
| Server                 | Non funzionante            | Doppio, asincrono           |
| Build                  | Assente                    | Eseguibile + installer      |
| Dipendenze             | Obsolete                   | Gestite via `requirements`  |

## Come funziona e manuale utente

Il file [`howItWorks.pdf`]() presenta uno schema visivo del funzionamento generale dell'emulatore.<br>
Per una documentazione approfondita delle API, si consulti la documentazione in [`pdoc-docs`](https://github.com/Filippo2903/ARMulator/tree/master/pdoc-docs).<br>
Il manuale originale del progetto (_da tradurre_) è incluso: [`manuale`](). Descrive le funzionalità della GUI, i registri, la memoria, e il set di istruzioni ARMv4 supportate.

# Sviluppi Futuri

1. Implementare le funzionalità di ARMv7
   * ##### in `simulator.py` la funzione _`bytecodeToInstr`_ sembra un buon punto di partenza
   * ##### si potrebbe usare [unicorn](https://www.unicorn-engine.org) ma richiede una revisione totale del codice
2. Completare la traduzione, rimuovendo le stringhe 'hard-coded'
3. Ottimizzare l'interazione tra client e server
4. Aggiungere modalità Thumb
5. Aggiungere istruzioni verso i coprocessori
6. Simulazione accurata dei cicli del processore
7. Compatibilità con MacOS (Silicon/Intel)
8. Ottimizzare ulteriormente aggiornamento GUI ed evitare che funzioni "passivamente"
   * ##### al momento utilizza del codice jQuery per reagire a messaggi provenienti dal websocket
9. Tradurre `manuale`
10. Comprendere inizializzazione memoria ed errori riguardanti celle non inizializzate da compiler

## Licenza e Ringraziamenti

Progetto prodotto come tesina per il corso di laurea di [Informatica](http://www.informatica.uniroma2.it/) dell'Università degli studi di Roma Tor Vergata<br>.
Basato su [epater](https://github.com/mgard/epater), sviluppato originariamente da Marc-André Gardner, Yannick Hold-Geoffroy e Jean-François Lalonde.<br>
Il progetto è distribuito sotto licenza GPLv3 (vedi `LICENSE`).
