# Elaborato per Fondamenti di informatica - Università San Raffaele
# Creator: Lucas Brandolisio
# Sistema di gestione delle spese personali e del budget

#Importo librerie che andro ad usare
import os
import sqlite3

# il database viene creato nella cartella principale del progetto
# Il programma va avviato da quella cartella con: python src/main.py
FILE_DB = "spese.db"
FILE_SQL = "sql/database.sql"


def apri_database():
    # Se il file SQL non si trova, il programma è stato avviato dalla cartella sbagliata
    if not os.path.exists(FILE_SQL):
        print("Errore: file sql/database.sql non trovato.")
        print("Avviare il programma dalla cartella del progetto con: python src/main.py")
        return None
    nuovo = not os.path.exists(FILE_DB)
    con = sqlite3.connect(FILE_DB)
    # In SQLite i vincoli di chiave esterna vanno attivati a ogni connessione
    con.execute("PRAGMA foreign_keys = ON")
    if nuovo:
        file = open(FILE_SQL, encoding="utf-8")
        con.executescript(file.read())
        file.close()
        con.commit()
    return con


def mostra_menu():
    print()
    print("-------------------------")
    print(" SISTEMA SPESE PERSONALI")
    print("-------------------------")
    print("1. Gestione Categorie")
    print("2. Inserisci Spesa")
    print("3. Definisci Budget Mensile")
    print("4. Visualizza Report")
    print("5. Esci")
    print("-------------------------")


def gestione_categorie(con):
    nome = input("Nome della categoria: ").strip()
    if nome == "": # Aggiungo Controlli per evitare che vengano create eccezioni che non sto gestendo
        print("Errore: il nome della categoria non può essere vuoto.")
        return
    if cerca_categoria(con, nome) is not None:
        print("La categoria esiste già.")
    else:
        con.execute("INSERT INTO Categoria (nome) VALUES (?)", (nome,))
        con.commit()
        print("Categoria inserita correttamente.")


# Controlla il formato YYYY-MM-DD (lunghezza 10) oppure YYYY-MM (lunghezza 7)
#Sono abituato a che utenti confondano mese con anno quindi inserisco controllo, uso formattazione Americana per data per abitudine PLC.
def formato_valido(testo, lunghezza):
    if len(testo) != lunghezza:
        return False
    i = 0
    while i < lunghezza:
        if i == 4 or i == 7:
            if testo[i] != "-":
                return False
        elif testo[i] < "0" or testo[i] > "9":
            return False
        i = i + 1
    mese = int(testo[5:7])
    if mese < 1 or mese > 12:
        return False
    if lunghezza == 10:
        giorno = int(testo[8:10])
        if giorno < 1 or giorno > 31:
            return False
    return True


# Restituisce l'importo come numero, oppure None se non è un numero
# Sono ammessi solo cifre, al massimo un punto e il segno meno all'inizio
def leggi_importo(testo):
    testo = testo.replace(",", ".")
    cifre = 0
    punti = 0
    i = 0
    while i < len(testo):
        if testo[i] >= "0" and testo[i] <= "9":
            cifre = cifre + 1
        elif testo[i] == ".":
            punti = punti + 1
        elif testo[i] == "-" and i == 0:
            pass
        else:
            return None
        i = i + 1
    if cifre == 0 or punti > 1:
        return None
    return float(testo)


# Scrive un numero con due decimali, ad esempio 320.50
def due_decimali(numero):
    return format(numero, ".2f")


# Allunga il testo fino alla larghezza indicata, per allineare le colonne
def colonna(testo, larghezza, carattere):
    return testo + carattere * (larghezza - len(testo))


# Restituisce il codice della categoria, oppure None se non esiste
def cerca_categoria(con, nome):
    riga = con.execute("SELECT id FROM Categoria WHERE nome = ?", (nome,)).fetchone()
    if riga is None:
        return None
    return riga[0]


def inserisci_spesa(con):
    data = input("Data (YYYY-MM-DD): ").strip()
    testo_importo = input("Importo: ").strip()
    nome = input("Nome della categoria: ").strip()
    descrizione = input("Descrizione (facoltativa): ").strip()

    if not formato_valido(data, 10):
        print("Errore: la data deve essere nel formato YYYY-MM-DD.")
        return
    importo = leggi_importo(testo_importo)
    if importo is None:
        print("Errore: l'importo deve essere un numero.")
        return
    if importo <= 0:
        print("Errore: l'importo deve essere maggiore di zero.")
        return
    categoria = cerca_categoria(con, nome)
    if categoria is None:
        print("Errore: la categoria non esiste.")
        return
    if descrizione == "":
        descrizione = None
    con.execute("INSERT INTO Spesa (data, importo, categoria, descrizione) VALUES (?, ?, ?, ?)",
                (data, importo, categoria, descrizione))
    con.commit()
    print("Spesa inserita correttamente.")


def definisci_budget(con):
    mese = input("Mese (YYYY-MM): ").strip()
    nome = input("Nome della categoria: ").strip()
    testo_importo = input("Importo del budget: ").strip()

    if not formato_valido(mese, 7):
        print("Errore: il mese deve essere nel formato YYYY-MM.")
        return
    importo = leggi_importo(testo_importo)
    if importo is None:
        print("Errore: l'importo deve essere un numero.")
        return
    if importo <= 0:
        print("Errore: il budget deve essere maggiore di zero.")
        return
    categoria = cerca_categoria(con, nome)
    if categoria is None:
        print("Errore: la categoria non esiste.")
        return
    riga = con.execute("SELECT importo FROM Budget WHERE mese = ? AND categoria = ?",
                       (mese, categoria)).fetchone()
    if riga is None:
        con.execute("INSERT INTO Budget (mese, categoria, importo) VALUES (?, ?, ?)",
                    (mese, categoria, importo))
    else:
        con.execute("UPDATE Budget SET importo = ? WHERE mese = ? AND categoria = ?",
                    (importo, mese, categoria))
    con.commit()
    print("Budget mensile salvato correttamente.")


def report_totale_categorie(con):
    righe = con.execute("""SELECT C.nome, SUM(S.importo) AS totale
                           FROM Categoria C, Spesa S
                           WHERE S.categoria = C.id
                           GROUP BY C.nome
                           ORDER BY C.nome""").fetchall()
    if len(righe) == 0:
        print("Nessuna spesa registrata.")
        return
    print(colonna("Categoria", 17, ".") + "Totale Speso")
    for riga in righe:
        print(colonna(riga[0], 17, ".") + due_decimali(riga[1]))


def report_budget(con):
    budget = con.execute("""SELECT B.mese, C.nome, B.importo, B.categoria
                            FROM Budget B, Categoria C
                            WHERE B.categoria = C.id
                            ORDER BY B.mese, C.nome""").fetchall()
    if len(budget) == 0:
        print("Nessun budget definito.")
        return
    mese_precedente = ""
    for riga in budget:
        mese = riga[0]
        # Totale speso nella categoria in quel mese 
        speso = con.execute("""SELECT SUM(importo) FROM Spesa
                               WHERE categoria = ? AND data LIKE ?""",
                            (riga[3], mese + "%")).fetchone()[0]
        if speso is None:
            speso = 0
        speso = round(speso, 2)
        if mese != mese_precedente:
            print()
            print("Mese:", mese)
            mese_precedente = mese
        print()
        print("Categoria:", riga[1])
        print("Budget: " + due_decimali(riga[2]))
        print("Speso: " + due_decimali(speso))
        if speso > riga[2]:
            print("Stato: SUPERAMENTO BUDGET")
        else:
            print("Stato: BUDGET RISPETTATO")


def report_elenco_spese(con):
    righe = con.execute("""SELECT S.data, C.nome, S.importo, S.descrizione
                           FROM Spesa S, Categoria C
                           WHERE S.categoria = C.id
                           ORDER BY S.data""").fetchall()
    if len(righe) == 0:
        print("Nessuna spesa registrata.")
        return
    print(colonna("Data", 12, " ") + colonna("Categoria", 14, " ") + colonna("Importo", 9, " ") + "Descrizione")
    print("-" * 62)
    for riga in righe:
        descrizione = riga[3]
        if descrizione is None:
            descrizione = ""
        print(colonna(riga[0], 12, " ") + colonna(riga[1], 14, " ")
              + colonna(due_decimali(riga[2]), 9, " ") + descrizione)


def visualizza_report(con):
    scelta = ""
    while scelta != "4":
        print()
        print("-------------------------")
        print(" MENU REPORT")
        print("-------------------------")
        print("1. Totale spese per categoria")
        print("2. Spese mensili vs budget")
        print("3. Elenco completo delle spese ordinate per data")
        print("4. Ritorna al menu principale")
        print("-------------------------")
        scelta = input("Inserisci la tua scelta: ").strip()
        print()
        match scelta:
            case "1":
                report_totale_categorie(con)
            case "2":
                report_budget(con)
            case "3":
                report_elenco_spese(con)
            case "4":
                pass
            case _:
                print("Scelta non valida. Riprovare.")


def main():
    con = apri_database() #Qua lo uso per aprire la connessione al database.
    if con is None:
        return
    print("Benvenuto nel Sistema di Gestione delle Spese Personali e del Budget.")
    scelta = ""
    while scelta != "5":
        mostra_menu()
        scelta = input("Inserisci la tua scelta: ").strip()
        match scelta:
            case "1":
                gestione_categorie(con)
            case "2":
                inserisci_spesa(con)
            case "3":
                definisci_budget(con)
            case "4":
                visualizza_report(con)
            case "5":
                print("Arrivederci.")
            case _:
                print("Scelta non valida. Riprovare.")
    con.close()


main()