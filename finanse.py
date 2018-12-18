import sqlite3

con = sqlite3.connect('FinanseBD.db')               #polaczenie z baza danych
con.row_factory = sqlite3.Row                       #dostep do kolumny
cursor = con.cursor()

#Tworzenie baz danych

                                                    # tabela przychodow
cursor.executescript("""
            CREATE TABLE IF NOT EXISTS przychody (
                wartosc INTEGER NOT NULL,
                zrodlo TEXT)
            """)

                                                    #tabela kosztow
cursor.executescript("""
            CREATE TABLE IF NOT EXISTS koszty (
                wartosc INTEGER NOT NULL,
                cel TEXT
            )""")

#POBIERANIE DANYCH Z BAZ DANYCH

def readKoszt():
    cursor.execute(
        """
        SELECT * FROM koszty
        """)

    koszty = cursor.fetchall()
    for koszt in koszty:
        print(koszt['wartosc'],koszt['cel'])


def readPrzychod():
    cursor.execute(
        """
        SELECT * FROM przychody
        """)

    przychody = cursor.fetchall()
    for przychod in przychody:
        print(przychod['wartosc'],przychod['zrodlo'])


def readSaldo():
    #zmienne poczatkowe
    sumaKosztow = 0
    sumaPrzychodow = 0
    #Pobranie kosztow
    cursor.execute(
        """
        SELECT * FROM koszty
        """)
    koszty = cursor.fetchall()

    #Pobranie przychodow
    cursor.execute(
        """
        SELECT * FROM przychody
        """)
    przychody = cursor.fetchall()

    #obliczanie salda
    for koszt in koszty:
        sumaKosztow +=koszt['wartosc']
    for przychod in przychody:
        sumaPrzychodow +=przychod['wartosc']
    saldo = sumaPrzychodow - sumaKosztow
    print(saldo)

while True:

    celMenu = input("Jaka czynnosc chcesz wykonac: ")

    while celMenu == "dodaj":

        akcjaSalda = input("Chcesz dodac koszt czy przychod: ")
        if akcjaSalda == "koszt":
            kwota = int(input("Podaj kwote kosztu: "))
            celKosztu = input("Podaj na co wydajesz podana kwote: ")
            cursor.execute('INSERT INTO koszty VALUES(?,?);',(kwota,celKosztu))
            con.commit()

        if akcjaSalda == "przychod":
            kwota = int(input("Podaj kwote przychodu: "))
            celPrzychodu = input("Podaj skad masz podany przychod: ")
            cursor.execute('INSERT INTO przychody VALUES(?,?);',(kwota,celPrzychodu))
            con.commit()

        if akcjaSalda == "help":
            print('W tym menu do wyboru masz komendy "koszt" oraz "przychod" lub "cofnij"')

        if akcjaSalda == "cofnij":
            celMenu = ""


    while celMenu == "sprawdz":

        akcjaStanu = input("Co chcesz sprawdzic? ")
        if akcjaStanu == "saldo":
            readSaldo()

        if akcjaStanu == "przychody":
            readPrzychod()

        if akcjaStanu == "koszty":
            readKoszt()

        if akcjaStanu == "help":
            print('W tym menu do wyboru masz komendy "saldo", "przychody" oraz "koszty" lub "cofnij"')

        if akcjaStanu == "cofnij":
            celMenu = ""




    if celMenu == "help":
        print('W tym menu do wyboru masz komendy "dodaj" oraz "sprawdz" lub "koniec"')

    if celMenu == "koniec":
        con.close()
        break