# PersonalExpenseSystem

Progetto finale di Fondamenti di Informatica: sistema di gestione delle spese personali e del budget.

Il programma gira su console. Permette di inserire le categorie, registrare le spese, fissare un budget mensile per ogni categoria e vedere tre report. L'ho scritto in Python e i dati sono salvati in un database SQLite.

## File del progetto

- src/main.py: il programma
- sql/database.sql: script che crea le tabelle e inserisce i dati di esempio
- demo/demo_video.mp4: video in cui faccio vedere il programma
- README.md: questo file

## Cosa serve

Serve Python 3.10 o una versione più recente, perché per i menu ho usato match. Io l'ho provato con Python 3.14.

Le librerie che uso sono solo due e sono già incluse in Python: sqlite3 per il database e os per controllare se il file del database esiste già. Quindi non bisogna installare niente.

Il programma non si compila.

## Come avviarlo

Scaricare il repository (Code, poi Download ZIP) ed estrarlo. Poi aprire il terminale nella cartella principale del progetto, quella dove ci sono src e sql. Il programma va avviato da questa cartella, altrimenti non trova lo script SQL.

Il comando è:

```
python src/main.py
```



La prima volta il programma crea il file spese.db usando sql/database.sql, quindi ci sono già alcune categorie, spese e budget di prova. Le volte dopo riapre lo stesso file e i dati inseriti restano. Se si vuole ripartire dai dati di esempio basta cancellare spese.db.

## Menu

Dal menu principale si sceglie scrivendo il numero e premendo Invio:

1. Gestione Categorie: aggiunge una categoria nuova
2. Inserisci Spesa: chiede data (YYYY-MM-DD), importo, categoria e una descrizione, che si può lasciare vuota
3. Definisci Budget Mensile: chiede mese (YYYY-MM), categoria e importo; se per quel mese il budget c'è già, lo aggiorna
4. Visualizza Report: totale per categoria, spese del mese confrontate con il budget, elenco delle spese in ordine di data
5. Esci
