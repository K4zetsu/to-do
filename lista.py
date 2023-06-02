
import klasy
import json
from datetime import date, datetime

print("Witaj w twojej osobistej liście zadań!\n")
#próba otwarcia pliku lista_zadan.json , wyświetlenia jego zawartości i zapisania jej do tablicy zadania[]
# jeśli plik nie ma zawartości, wyświetlany jest stosowny komunikat i tworzona jest pusta lista zadania[]
try:
    with open("to_do_lista/lista_zadan.json", 'r', encoding='utf-8') as plik:
        zadania = json.load(plik)
        for i in range(0, len(zadania), +1):
            print("Zadanie numer {}".format(i+1))
            print("Nazwa:", zadania[i]["Tytuł"])
            print("Termin:", zadania[i]["Termin"])
            print("\n")
except json.JSONDecodeError:
    print("Nie masz jeszcze żadnych zadań na swojej liście :)")
    zadania = []
#Tworzenie zmiennych potrzebnych do funkcjonowania tego kodu. loop odpowiada za pętlę programu,
#listaZadan zczytuje nowo utworzone zadania gotowe do zapisania w pliku, ID jest tworzone teraz gdyż jest to konieczne w tym programie
#aby było one unikatowe dla każdego zadania, zmienna oraz uniqueID służą do elementu kodu sprawdzającego unikatowe ID
loop = True
listaZadan = []
warunek = len(zadania)
zmienna = 1
uniqueID = 2
dni_tygodnia = ['poniedziałek', 'wtorek', 'środa', 'czwartek', 'piątek', 'sobota', 'niedziela']
#Rozpoczęcie właściwego programu
while loop:
    print("Którą czynność chcesz wykonać?")
    print("""    1. Dodaj nowe zadanie
    2. Wyświetl żądanie zadanie
    3. Usuń zadanie
    4. Zautualizuj zadanie
    5. Zapisz zadanie do pliku
    6. Wyświetlenie wszystkich zadań w danym dniu tygodnia
    7. Wyjście""")
    try:
        wybor = int(input("Wybierz opcję, która cię interesuje!: "))
    except ValueError:
        print("Zła wartość, wpisz poprawną!")
        continue
#jeśli użytkownik wybierze "1", utworzy on nowe zadanie, któremu automatycznie zostanie przypisane unikatowe ID
#Mamy tu do czynienia z warunkiem sprawdzającym i przypisującym unikalne ID oraz prostym przypisaniem wartości do zmiennych znajdujących
#się w osobnej klasie
    if wybor == 1:
        ID = 0
        if len(zadania) == 0:
            ID = ID + 1
        elif len(listaZadan) >= 1:
            ID = len(zadania) + uniqueID
            uniqueID = uniqueID + 1
        elif warunek != len(zadania):
            ID = len(zadania) + 1
        else:
            ID = len(zadania) + zmienna
            zmienna = zmienna + 1

        nazwa = input("Nazwa zadania: ")
        opis = input("Dodaj opis zadania: ")
#Kwestia terminu, uznałem, że najlepiej będzie jeśli program sam określi jakim dniem tygodnia jest wpisana data
#Oszczędzi to użytkownikowi trudu w szukaniu odpowiedniego dnia
#co ma tu miejsce to użytkownik wpisuje datę w podanym formacie, dalej program konwertuje to w odpowiedni sposób
#aby można było wyciągnąć z tej daty dalsze informacje takie jak numer dnia tygodnia (1-7)
#następnie numer dnia odnosi się do listy, która zbiera nazwy dni tygodnia i przypisuje odpowiednią nazwę do zmiennej.
        termin = input("Dodaj termin wykonania zadania (DD-MM-RRRR): ")
        termin_data = datetime.strptime(termin, "%d-%m-%Y")
        dzien_tygodnia = termin_data.weekday()
        nazwa_dnia = dni_tygodnia[dzien_tygodnia]
        noweZadanie = klasy.Lista(ID, nazwa, termin, opis, nazwa_dnia)
        element = noweZadanie.dodajZadanie()
        element[0] = int(element[0])
        listaZadan.append(element)
#Po wyborze opcji "2" użytkownik będzie mógł wyświetlić wybrane przez niego zadanie oraz zostanie zapytany czy chce wyświetlić opis
    elif wybor == 2:
        numerZadania = int(input("Wybierz numer zadania, które chcesz wyswietlić: "))
        for zadanie in zadania:
            if numerZadania == zadanie["ID"]:
                print("ID zadania: ", zadanie["ID"])
                print("Nazwa zadania: ", zadanie["Tytuł"])
                print("Termin zadania: ", zadanie["Termin"])
                print("Dzień tygodnia: ", zadanie["Dzien"])
                decyzja = input("Czy chcesz wyświetlić opis zadania? t/n: ")
                if decyzja == "t":
                    print("Opis zadania: ", zadanie["Opis"])
            else:
                continue
#Opcja "3" pozwala użykownikowi permanentnie usunąć zadanie z listy, niestety nie jest to odwracalne
    elif wybor == 3:
        usuwanie_zadania = klasy.Lista(1, "", "", "", "")
        numer_zadania = int(input("Wybierz ID zadania, które chcesz usunąć: "))
        usuwanie_zadania.usunZadanie(numer_zadania)
        listaZadan = [element for element in listaZadan if element[0] != numer_zadania]
        zadania = [element for element in zadania if element['ID'] != numer_zadania]
#Opcja "4" umożliwia aktualizację dowolnego zadania z zachowaniem jego ID, nie ma potrzeby go zmieniać.
    elif wybor == 4:
        numerZadania = int(input("Wybierz numer zadania, które chcesz zaktualizować: "))
        for zadanie in zadania:
            if zadanie["ID"] == numerZadania:
                zadanie["Tytuł"] = input("Wpisz nową nazwę zadania: ")
#Podobnie tutaj, jeśli użytkownik zmieni termin wykonania zadania, dzień tygodnia automatycznie się zmieni. Nie ma sensu kazać mu tego robić samodzielnie
                zadanie["Termin"] = input("Wpisz nowy termin wykonania zadania (DD-MM-RRRR): ")
                nowy_termin_data = datetime.strptime(zadanie["Termin"], "%d-%m-%Y")
                nowy_dzien_tygodnia = nowy_termin_data.weekday()
                nowa_nazwa_dnia = dni_tygodnia[nowy_dzien_tygodnia]
                zadanie["Opis"] = input("Wpisz nowy opis zadania: ")
                zadanie["Dzien"] = nowa_nazwa_dnia
            else:
                continue
#Opcja "5" służy do ręcznego zapisania utworzonych zadań na wypadek, gdyby użytkownik nie zaufał programowi. I tutaj mała dygresja
#Zarówno w punkcie "5" jak i "6" bardzo ciężkie do wykonania było zachowanie unikalności ID, próbowałem wielu wariantów jednak ten,
#który widzisz jest pierwszym, który działa. Być może jest łatwiejszy sposób ale jak pisałem wcześniej starałem się.
    elif wybor == 5:
        istniejace_id = [zadanie['ID'] for zadanie in zadania]
        for zadanie in listaZadan:
            if zadanie[0] not in istniejace_id:
                formatowane = {"ID": zadanie[0], "Tytuł": zadanie[1], "Termin": zadanie[2], "Opis": zadanie[3], "Dzien": zadanie[4]}
                zadania.append(formatowane)
        with open("to_do_lista/lista_zadan.json", "w", encoding='utf-8') as plik:
            json.dump(zadania, plik, ensure_ascii=False, indent=4)
            print("Zadania zostały zapisane!\n")
#Wybranie opcji "6" umożliwi użytkownikowi wyświetlenie wszystkich zadań zaplanowanych na konkretny dzień tygodnia
#kod pobiera od użytkownika nazwę dnia tygodnia następnie dostosowuje go do odpowiedniego formatu
#porównuje go z listą dni tygodnia i szuka takiej wartości w tablicy z pobranymi zadaniami, jeśli na takie natrafi, drukuje je.
    elif wybor == 6:
        wybrany_dzien = input("Wybierz dzien tygodnia, który chcesz wyświetlić: ")
        wybrany_dzien = wybrany_dzien.lower()
        if wybrany_dzien in dni_tygodnia:
            print("Oto wszystkie zadania, które masz zaplanowane na {}".format(wybrany_dzien))
            for zadanie in zadania:
                if zadanie["Dzien"] == wybrany_dzien:
                    print("ID zadania: ", zadanie["ID"])
                    print("Nazwa zadania: ", zadanie["Tytuł"])
                    print("Termin zadania: ", zadanie["Termin"])
                    print("Dzień tygodnia: ", zadanie["Dzien"], "\n")
                    b = input("Czy wyświetlić opis? t/n :")
                    if b == "t":
                        print("Opis: ", zadanie["Opis"])
                    else: continue
                    
        pass
#Opcja "7" służy do zapisania wszystkich nowych zadań w pliku oraz zakończenie programu
    elif wybor == 7:
        with open("to_do_lista/lista_zadan.json", "w", encoding='utf-8') as plik:
            istniejace_id = [zadanie['ID'] for zadanie in zadania]
            for zadanie in listaZadan:
                if zadanie[0] in istniejace_id:
                    continue
                else:
                    formatowane = {"ID":zadanie[0], "Tytuł":zadanie[1], "Termin":zadanie[2], "Opis":zadanie[3], "Dzien": zadanie[4]}
                    zadania.append(formatowane)
            if len(zadania) == 0:
                print("Nie masz żadnych danych do zapisania!\n")
            else:
                json.dump(zadania, plik, ensure_ascii=False, indent=4)
                print("Dane zapisane, widzimy się wkrótce!\n")
        loop = False
    else:
        print("Nie ma takiej funkcji, wybierz inną!")