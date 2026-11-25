-- Sistema di gestione delle spese personali e del budget
-- Script di creazione del database e dati di esempio (SQLite)

DROP TABLE IF EXISTS Budget;
DROP TABLE IF EXISTS Spesa;
DROP TABLE IF EXISTS Categoria;

CREATE TABLE Categoria (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(30) NOT NULL UNIQUE CHECK (nome <> '')
);

CREATE TABLE Spesa (
    id INTEGER PRIMARY KEY,
    data DATE NOT NULL CHECK (data LIKE '____-__-__'),
    importo NUMERIC(8,2) NOT NULL CHECK (importo > 0),
    categoria INTEGER NOT NULL,
    descrizione VARCHAR(100),
    CONSTRAINT fk_spesa_categoria FOREIGN KEY (categoria) REFERENCES Categoria(id)
);

-- Un solo budget per ogni categoria in un mese
CREATE TABLE Budget (
    mese CHAR(7) NOT NULL CHECK (mese LIKE '____-__'),
    categoria INTEGER NOT NULL,
    importo NUMERIC(8,2) NOT NULL CHECK (importo > 0),
    PRIMARY KEY (mese, categoria),
    CONSTRAINT fk_budget_categoria FOREIGN KEY (categoria) REFERENCES Categoria(id) -- Uso fk per sintassi appresa a lavoro per definire una foreing key in caso
    -- di necessità di debug rapido se per caso sbagliando la query mi restituisce la colonna dove avviene.
);

INSERT INTO Categoria VALUES (1, 'Alimentari');
INSERT INTO Categoria VALUES (2, 'Trasporti');
INSERT INTO Categoria VALUES (3, 'Casa');
INSERT INTO Categoria VALUES (4, 'Svago');

INSERT INTO Spesa VALUES (1, '2026-01-03', 85.40, 1, 'Spesa al supermercato');
INSERT INTO Spesa VALUES (2, '2026-01-08', 40.00, 2, 'Abbonamento autobus');
INSERT INTO Spesa VALUES (3, '2026-01-10', 120.00, 3, 'Bolletta luce');
INSERT INTO Spesa VALUES (4, '2026-01-15', 25.00, 1, 'Pranzo');
INSERT INTO Spesa VALUES (5, '2026-01-18', 132.60, 1, 'Spesa al supermercato');
INSERT INTO Spesa VALUES (6, '2026-01-22', 35.00, 4, 'Cinema');
INSERT INTO Spesa VALUES (7, '2026-01-27', 77.50, 1, 'Mercato');
INSERT INTO Spesa VALUES (8, '2026-02-02', 40.00, 2, 'Abbonamento autobus');
INSERT INTO Spesa VALUES (9, '2026-02-05', 64.30, 1, 'Spesa al supermercato');
INSERT INTO Spesa VALUES (10, '2026-02-12', 18.50, 4, NULL);
INSERT INTO Spesa VALUES (11, '2026-02-14', 95.00, 3, 'Bolletta gas');
INSERT INTO Spesa VALUES (12, '2026-02-20', 40.00, 2, 'Benzina');

INSERT INTO Budget VALUES ('2026-01', 1, 300.00);
INSERT INTO Budget VALUES ('2026-01', 2, 50.00);
INSERT INTO Budget VALUES ('2026-01', 3, 150.00);
INSERT INTO Budget VALUES ('2026-02', 1, 300.00);
INSERT INTO Budget VALUES ('2026-02', 4, 15.00);
