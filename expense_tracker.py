import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path

FILE_NAME = Path("spese.csv")
FIELDNAMES = ["data", "tipo", "categoria", "descrizione", "importo"]


def inizializza_file() -> None:
    if not FILE_NAME.exists():
        with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()


def aggiungi_movimento() -> None:
    print("\n--- Aggiungi movimento ---")
    tipo = input("Tipo (entrata/uscita): ").strip().lower()
    while tipo not in ["entrata", "uscita"]:
        tipo = input("Valore non valido. Scrivi 'entrata' o 'uscita': ").strip().lower()

    categoria = input("Categoria (es. affitto, cibo, stipendio): ").strip()
    descrizione = input("Descrizione: ").strip()

    data = input("Data (GG/MM/AAAA, lascia vuoto per oggi): ").strip()
    if not data:
        data = datetime.today().strftime("%d/%m/%Y")
    else:
        try:
            datetime.strptime(data, "%d/%m/%Y")
        except ValueError:
            print("Data non valida. Uso la data di oggi.")
            data = datetime.today().strftime("%d/%m/%Y")

    while True:
        try:
            importo = float(input("Importo: ").replace(",", "."))
            if importo <= 0:
                print("L'importo deve essere maggiore di 0.")
                continue
            break
        except ValueError:
            print("Inserisci un numero valido.")

    with open(FILE_NAME, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow(
            {
                "data": data,
                "tipo": tipo,
                "categoria": categoria,
                "descrizione": descrizione,
                "importo": f"{importo:.2f}",
            }
        )

    print("Movimento salvato con successo.\n")


def leggi_movimenti() -> list[dict]:
    with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def mostra_movimenti() -> None:
    print("\n--- Elenco movimenti ---")
    movimenti = leggi_movimenti()

    if not movimenti:
        print("Nessun movimento registrato.\n")
        return

    for i, movimento in enumerate(movimenti, start=1):
        print(
            f"{i}. {movimento['data']} | {movimento['tipo'].upper()} | "
            f"{movimento['categoria']} | {movimento['descrizione']} | € {movimento['importo']}"
        )
    print()


def calcola_totali(movimenti: list[dict] | None = None) -> tuple[float, float, float]:
    if movimenti is None:
        movimenti = leggi_movimenti()

    totale_entrate = 0.0
    totale_uscite = 0.0

    for movimento in movimenti:
        importo = float(movimento["importo"])
        if movimento["tipo"] == "entrata":
            totale_entrate += importo
        elif movimento["tipo"] == "uscita":
            totale_uscite += importo

    saldo = totale_entrate - totale_uscite
    return totale_entrate, totale_uscite, saldo


def mostra_riepilogo() -> None:
    print("
--- Riepilogo ---")
    movimenti = leggi_movimenti()
    totale_entrate, totale_uscite, saldo = calcola_totali(movimenti)

    print(f"Totale entrate: € {totale_entrate:.2f}")
    print(f"Totale uscite:  € {totale_uscite:.2f}")
    print(f"Saldo attuale:  € {saldo:.2f}
")


def filtra_per_mese() -> None:
    print("
--- Report mensile ---")
    mese = input("Inserisci mese e anno (MM/AAAA): ").strip()

    try:
        datetime.strptime(mese, "%m/%Y")
    except ValueError:
        print("Formato non valido. Usa MM/AAAA.
")
        return

    movimenti = leggi_movimenti()
    filtrati = []

    for movimento in movimenti:
        try:
            data_movimento = datetime.strptime(movimento["data"], "%d/%m/%Y")
            if data_movimento.strftime("%m/%Y") == mese:
                filtrati.append(movimento)
        except ValueError:
            continue

    if not filtrati:
        print("Nessun movimento trovato per questo mese.
")
        return

    for i, movimento in enumerate(filtrati, start=1):
        print(
            f"{i}. {movimento['data']} | {movimento['tipo'].upper()} | "
            f"{movimento['categoria']} | {movimento['descrizione']} | € {movimento['importo']}"
        )

    totale_entrate, totale_uscite, saldo = calcola_totali(filtrati)
    print(f"
Totale entrate del mese: € {totale_entrate:.2f}")
    print(f"Totale uscite del mese:  € {totale_uscite:.2f}")
    print(f"Saldo del mese:          € {saldo:.2f}
")


def riepilogo_per_categoria() -> None:
    print("
--- Riepilogo per categoria ---")
    movimenti = leggi_movimenti()

    if not movimenti:
        print("Nessun movimento registrato.
")
        return

    categorie = defaultdict(float)

    for movimento in movimenti:
        if movimento["tipo"] == "uscita":
            categorie[movimento["categoria"]] += float(movimento["importo"])

    if not categorie:
        print("Non ci sono uscite da raggruppare.
")
        return

    for categoria, totale in sorted(categorie.items(), key=lambda item: item[1], reverse=True):
        print(f"{categoria}: € {totale:.2f}")
    print()


def cerca_movimenti() -> None:
    print("
--- Cerca movimenti ---")
    parola = input("Inserisci una parola chiave: ").strip().lower()

    if not parola:
        print("Ricerca vuota.
")
        return

    movimenti = leggi_movimenti()
    risultati = []

    for movimento in movimenti:
        testo = " ".join([
            movimento["data"],
            movimento["tipo"],
            movimento["categoria"],
            movimento["descrizione"],
            movimento["importo"],
        ]).lower()
        if parola in testo:
            risultati.append(movimento)

    if not risultati:
        print("Nessun movimento trovato.
")
        return

    for i, movimento in enumerate(risultati, start=1):
        print(
            f"{i}. {movimento['data']} | {movimento['tipo'].upper()} | "
            f"{movimento['categoria']} | {movimento['descrizione']} | € {movimento['importo']}"
        )
    print()


def mostra_menu() -> None:
    while True:
        print("=" * 35)
        print("GESTORE SPESE PERSONALI")
        print("=" * 35)
        print("1. Aggiungi movimento")
        print("2. Mostra movimenti")
        print("3. Mostra riepilogo")
        print("4. Report mensile")
        print("5. Riepilogo per categoria")
        print("6. Cerca movimenti")
        print("7. Esci")

        scelta = input("Scegli un'opzione: ").strip()

        if scelta == "1":
            aggiungi_movimento()
        elif scelta == "2":
            mostra_movimenti()
        elif scelta == "3":
            mostra_riepilogo()
        elif scelta == "4":
            filtra_per_mese()
        elif scelta == "5":
            riepilogo_per_categoria()
        elif scelta == "6":
            cerca_movimenti()
        elif scelta == "7":
            print("Chiusura programma. A presto!")
            break
        else:
            print("Opzione non valida. Riprova.\n")


if __name__ == "__main__":
    inizializza_file()
    mostra_menu()
