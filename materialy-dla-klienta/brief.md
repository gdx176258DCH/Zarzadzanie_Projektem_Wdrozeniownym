# Liczenie osób w jednej strefie

**Dla:** mgr inż. Szymon Guzik  
**Od:** zespół projektowy (Dominik, Daria, Ania, Arek, Mateusz)  
**Data:** 28 listopada 2026  
**Status:** propozycja do omówienia na spotkaniu

## Potrzeba klienta

Klient chce na bieżąco wiedzieć, ile osób przebywa w jednej strefie. Kamera i mały komputer pracują na miejscu, a obraz nie opuszcza urządzenia. Na zewnątrz trafia wyłącznie wynik: liczba osób i, w razie potrzeby, ich położenie w kadrze.

Przetwarzanie przy kamerze ma sens, gdy liczy się czas reakcji, łącze nie przeniesie strumienia wideo, dane mają zostać na miejscu albo lokalizacja pracuje bez stałego dostępu do internetu. Urządzenie brzegowe jest słabsze od serwera, dlatego model dobieramy do sprzętu.

## Co dostarczamy

Dwa rozwiązania liczenia osób, uruchomione na tym samym urządzeniu i porównane na tych samych klatkach:

- detektor klasyczny HOG + SVM,
- sieć neuronowa (YOLO) dopasowana do urządzenia.

Każde rozwiązanie mierzymy osobno: ile osób wykrywa i ile trwa przetworzenie jednej klatki. Wynik zawiera liczbę osób, czas i nazwę rozwiązania, które go podało. Na zakończenie klient otrzymuje raport z obiema tabelami i wybiera rozwiązanie do codziennej pracy.

## Proponowane kryteria odbioru

Proponujemy próg: co najmniej 90% wykrytych osób i co najmniej 10 klatek na sekundę na Jetson Nano. Sam odsetek wykryć nie pokazuje, czy liczenie jest poprawne, dlatego odbiór opiera się na czterech miarach:

1. Czułość: jaki odsetek rzeczywistych osób detektor znalazł.
2. Precyzja: jaki odsetek wskazanych ramek rzeczywiście pokazuje osobę.
3. Błąd liczenia: różnica między liczbą wykrytą a rzeczywistą liczbą osób na klatce.
4. Wydajność: czas przetworzenia klatki na urządzeniu docelowym i wynikowa liczba klatek na sekundę.

Ostateczny próg, urządzenie i warunki testu (dzień, noc, deszcz, tłum, odległość od kamery) zatwierdza klient.

## Zakres

| W zakresie | Poza zakresem |
| --- | --- |
| Jedna kamera, jedna strefa, liczenie osób | Rozpoznawanie twarzy i tożsamości, analiza emocji |
| Przetwarzanie na urządzeniu przy kamerze | Przesyłanie obrazu do chmury |
| Wynik bez strumienia wideo | Wiele kamer i lokalizacji |
| Zbiór testowy i protokół pomiarów | Trenowanie modelu od zera |
| Dwa rozwiązania mierzone tym samym protokołem | Zakup sprzętu |
| Raport porównawczy i prezentacja | Inne scenariusze, np. wykrywanie kasków czy znaków drogowych |

Dodatkowy scenariusz może wejść do zakresu, jeśli klient go wybierze i wskaże, który element planu zastępuje.

## Dane i prywatność

Nagranie osób jest danymi osobowymi. Miejsce montażu nagrywamy wyłącznie za zgodą i z rozmyciem twarzy. Do pierwszych pomiarów używamy publicznego nagrania z otwartą licencją albo materiału wskazanego przez klienta.

Wynikiem jest liczba osób, nie ich tożsamość. Nie tworzymy bazy twarzy, nie zapisujemy cech wyglądu i nie analizujemy emocji. Klatka jest usuwana po zliczeniu, a do raportu nie trafia obraz z rozpoznawalną twarzą. Tymczasowy numer śladu, który zapobiega podwójnemu liczeniu tej samej osoby, istnieje najwyżej kilka sekund, nie jest przechowywany po sesji i nie wskazuje tożsamości.

Identyfikacja osób byłaby osobnym zleceniem. Rozporządzenie UE 2024/1689 (AI Act) nakłada na takie systemy ocenę zgodności, rejestrację i nadzór człowieka, a za naruszenia przewiduje kary do 35 mln euro albo 7% światowego obrotu. Ten zakres wykracza poza budżet semestru.

## Sprzęt

Rozwiązania uruchamiamy na NVIDIA Jetson Nano z kamerą. Zespół dysponuje tym urządzeniem. Odbiór wydajności odbywa się na Jetson Nano.

Drugim urządzeniem testowym jest telefon komórkowy z wbudowaną kamerą. Wynik z telefonu może trafiać do systemu odbiorcy przez API. Pomiar na telefonie i na laptopie ma charakter pomocniczy i jest opisany nazwą sprzętu; nie zastępuje odbioru na Jetson Nano.

## Rozdzielczość obrazu

Mniejszy obraz przetwarza się szybciej, ale detektor gubi osoby dalekie i na krawędziach kadru. Zbyt mały obraz uniemożliwia wykrycie sylwetki. Dlatego każde rozwiązanie mierzymy w trzech rozdzielczościach, a wybór rozdzielczości jest decyzją klienta podejmowaną na podstawie tabel.

## Decyzje do podjęcia na spotkaniu

1. Czy wynikiem ma być wyłącznie liczba osób?
2. Czy strefa jest publicznie dostępna?
3. Czy pomiar na Jetson Nano zamyka odbiór wydajności, a telefon zostaje drugim urządzeniem testowym?
4. Jaki próg i jakie warunki obowiązują przy odbiorze? Próg jest wspólny dla obu rozwiązań.
5. Skąd pochodzą nagrania testowe i kto udziela zgody na nagrywanie?
6. Dokąd trafia wynik: w jakiej postaci, jak często i do jakiego systemu?
7. Kto wystawia rekomendację po odbiorze?
