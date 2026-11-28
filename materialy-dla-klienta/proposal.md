# Oferta: liczenie osób w jednej strefie

**Dla:** mgr inż. Szymon Guzik  
**Od:** zespół projektowy (Dominik, Daria, Ania, Arek, Mateusz)  
**Data:** 28 listopada 2026  
**Status:** propozycja zakresu i harmonogramu

## Podsumowanie

Dostarczamy dwa rozwiązania liczenia osób działające na urządzeniu przy kamerze. Rozwiązanie A to klasyczny detektor HOG + SVM. Rozwiązanie B to sieć neuronowa YOLO dopasowana do sprzętu. Oba rozwiązania przetwarzają te same klatki i są mierzone tym samym protokołem. Klient otrzymuje dwie tabele wyników i na ich podstawie wybiera rozwiązanie do codziennej pracy.

## Dlaczego dwa rozwiązania

Detektor klasyczny działa bez karty graficznej i bez trenowania, dzięki czemu pozwala szybko uruchomić prototyp. Jego słabością są tłum, zasłonięcia i nietypowe pozy.

Sieć neuronowa wykrywa osoby skuteczniej, ale na małym komputerze wymaga optymalizacji: kwantyzacji int8 i uruchomienia przez TensorRT.

Porównanie obu podejść na tych samych danych pozwala klientowi świadomie wybrać kompromis między jakością a szybkością.

## Plan realizacji

1. Uruchomienie rozwiązania A i pierwsza tabela pomiarów: rozdzielczość, osoby wykryte, osoby rzeczywiste, czas klatki, sprzęt.
2. Wspólny protokół pomiarów: co najmniej 50 ręcznie oznaczonych klatek, czułość, precyzja, błąd liczenia, wydajność na urządzeniu docelowym, warunki testu. Każdy wynik ma datę, wersję oprogramowania, nazwę rozwiązania i sprzęt.
3. Uruchomienie rozwiązania B na Jetson Nano, optymalizacja i pomiar na tych samych klatkach i rozdzielczościach.
4. Raport porównawczy i prezentacja wyników.

## Zakres dostawy

- rozwiązanie A: detekcja osób w OpenCV metodą HOG + SVM;
- rozwiązanie B: gotowy model YOLO dopasowany do Jetson Nano, bez trenowania od zera;
- tabela wyników w trzech rozdzielczościach dla każdego rozwiązania;
- protokół pomiarów i zbiór co najmniej 50 oznaczonych klatek z opisem źródła i licencji;
- wynik bez obrazu: liczba osób, czas i nazwa rozwiązania, z możliwością wysyłki do serwera wskazanego przez klienta;
- raport z obiema tabelami: wyniki, sprzęt, wersja, warunki i ograniczenia każdego rozwiązania;
- prezentacja końcowa.

Zakres wykluczony opisuje brief.

## Kryteria odbioru

Proponujemy próg: co najmniej 90% wykrytych osób i co najmniej 10 klatek na sekundę na Jetson Nano. Odbiór obejmuje protokół oraz dwie tabele z urządzenia docelowego, każdą z jednoznaczną oceną: próg spełniony albo niespełniony. Słabszy wynik jednego rozwiązania nie blokuje odbioru, jeśli oba zostały zmierzone tym samym protokołem. Wynik z laptopa lub telefonu jest opisany jako pomiar pomocniczy i nie zastępuje pomiaru na Jetson Nano. Telefon komórkowy z kamerą jest drugim urządzeniem testowym; wynik może iść do systemu odbiorcy przez API.

## Budżet

Budżetem projektu jest czas zespołu: 16 godzin zajęć oraz 20 godzin pracy własnej każdej osoby. Projekt nie obejmuje wyceny finansowej.

## Harmonogram

| Etap | Termin | Rezultat | Decyzja klienta |
| --- | --- | --- | --- |
| Start | 7 listopada 2026 | temat, zespół | wybór scenariusza |
| Oferta | 25 listopada 2026 | brief, oferta, karta projektu | odpowiedzi na pytania z briefu |
| Rozwiązanie A | 28 listopada 2026 | prototyp HOG + SVM, tabela, szkic protokołu | akceptacja protokołu |
| Dane i pomiary | 29 listopada – 12 grudnia 2026 | 50 oznaczonych klatek, pomiar A na Jetson Nano | zgoda na dane, próg odbioru, odbiorca wyniku |
| Rozwiązanie B | 13 grudnia 2026 | sieć na Jetson Nano, druga tabela | akceptacja wyników |
| Odbiór | 23 stycznia 2027 | raport, prezentacja, wynik z nazwą rozwiązania | wybór rozwiązania, rekomendacja |

## Prywatność

Oferujemy liczbę osób, nie ich tożsamość. Nie przechowujemy bazy twarzy ani cech wyglądu. Licznik nadaje sylwetce tymczasowy numer śladu, aby nie liczyć tej samej osoby wielokrotnie. Numer istnieje najwyżej 3 sekundy po zniknięciu osoby z kadru, nie jest zapisywany po sesji i nie wskazuje tożsamości. Klatka jest usuwana po zliczeniu, a zbiór testowy ma licencję albo zgodę oraz rozmyte twarze.

Detektor klasyczny analizuje wyłącznie kształt sylwetki i nie porównuje jej z żadną bazą. Sieć neuronowa dostarcza liczbę i ramki; w zakresie nie ma zapisu cech, który mógłby służyć do ponownego rozpoznania osoby. Identyfikacja osób byłaby osobnym zleceniem, objętym wymogami rozporządzenia UE 2024/1689.

## Ryzyka

| Ryzyko | Skutek dla klienta | Działanie |
| --- | --- | --- |
| Jetson Nano niedostępny w dniu pomiaru | brak odbioru wydajności | pomiar pomocniczy na laptopie lub telefonie, jednoznacznie opisany |
| Telefon niedostępny w dniu testu | brak drugiej tabeli testowej | odbiór na Nano zostaje; lukę w testach na telefonie zapisujemy w raporcie |
| Brak zgody na nagranie w miejscu montażu | brak klatek z docelowej sceny | publiczny zbiór z licencją i opis różnic względem sceny |
| Sieć nie osiąga progu na Jetson Nano | rozwiązanie B nie spełnia kryterium | optymalizacja TensorRT i int8, mniejsze wejście, wynik raportowany jawnie |
| Różne dane dla obu rozwiązań | wyniki nieporównywalne | jeden zbiór, jeden protokół, te same rozdzielczości |
| Rozszerzenie zakresu o kolejny scenariusz | zagrożenie terminu | zmiana zakresu tylko za decyzją klienta |
| Obraz z twarzą w materiałach | ryzyko przetwarzania danych biometrycznych | usuwanie klatek, rozmycie twarzy w raporcie |
| Prośba o identyfikację osób | inne zlecenie o wysokim ryzyku prawnym | w projekcie pozostaje liczenie osób |

## Zespół

| Rola | Zakres odpowiedzialności |
| --- | --- |
| Lider | kontakt z klientem, harmonogram, protokół |
| Model i przetwarzanie obrazu | rozwiązanie A, rozdzielczości, czas klatki |
| Model i przetwarzanie obrazu | rozwiązanie B, optymalizacja na urządzeniu |
| Aplikacja i sprzęt | uruchomienie na Jetson Nano, wyjście wyniku |
| Testy, dane i dokumentacja | zbiór, oznaczenia, protokół, raport |

Skład zespołu: Dominik, Daria, Ania, Arek, Mateusz. Kod: https://github.com/gdx176258DCH/Zarzadzanie_Projektem_Wdrozeniownym
