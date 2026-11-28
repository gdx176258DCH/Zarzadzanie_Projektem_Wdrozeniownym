# Liczenie osób w jednej strefie
## Plan etapu 3, karta i ryzyka po prototypie

**Data:** 28 listopada 2026  
**Status:** plan

### 1. Drugi moduł
Drugim modułem jest rozwiązanie B: sieć neuronowa liczy osoby w tej samej strefie, na tych samych klatkach i szerokościach co rozwiązanie A. Znaki drogowe i raport do serwera nie wchodzą do tego etapu.

Program zespołu ma już YOLOv8n przez OpenCV DNN, na procesorze. Model nie leży w repozytorium. Przed dystrybucją zespół sprawdza licencję modelu Ultralytics.

### 2. Dopasowanie do urządzenia
Na Jetson Nano zespół sprawdza TensorRT i wagi int8. Sieć startuje z gotowego modelu. Trenowania od zera nie ma.

Wyjście sieci to liczba osób, czas klatki, nazwa rozwiązania i ewentualnie ramki. Nie ma zapisu cech twarzy ani bazy osób.

### 3. Aktualizacja karty
| Pole karty | Obecnie | Po pomiarze |
|---|---|---|
| Cel mierzalny | propozycja: 90% i 10 klatek na sekundę na Jetson Nano | próg przyjęty albo zmieniony przez klienta |
| Sprzęt | Jetson Nano do odbioru; telefon do dodatkowych testów; pomiarów brak | nazwa i wersja urządzenia przy każdym wyniku |
| Dane testowe | film „Calle preciados”, Wikimedia Commons, autor OsvaldoGago, licencja CC BY-SA; klatki jeszcze nieoznaczone | źródło, licencja, liczba klatek |
| Harmonogram | spotkanie 3: 13 grudnia 2026, 8:00–11:05, B016; spotkanie 4: 23 stycznia 2027, 11:20–14:25, B018 | bez zmian |

### 4. Ryzyka po prototypie
| Ryzyko | Skutek dla klienta | Odpowiedź |
|---|---|---|
| Brak oznaczonych klatek | tabela A pozostaje pusta | oznaczenie 50 klatek przed pomiarem sieci |
| Jetson Nano niedostępny w dniu pomiaru | brak odbioru wydajności | pomiar na laptopie lub telefonie, podpisany nazwą sprzętu |
| Telefon niedostępny w dniu testu | brak drugiej tabeli testowej | odbiór na Nano zostaje; lukę zapisujemy w raporcie |
| HOG nie widzi osób przy 320 px | szybsza rozdzielczość gubi ludzi | klient wybiera rozdzielczość z tabeli |
| Sieć poniżej 10 klatek na sekundę | rozwiązanie B nie spełnia progu | TensorRT, int8 albo mniejsze wejście; wynik zapisany jawnie |
| Śledzenie zamienia albo dubluje ślady | błąd sumy przechodniów | błąd sumy mierzony osobno od błędu na klatce |
| Prośba o identyfikację osób | inne zlecenie objęte rozporządzeniem UE 2024/1689 | w projekcie pozostaje liczenie osób |
| Licencja modelu YOLOv8 | ograniczenie dalszego użycia | sprawdzenie licencji przed dystrybucją |

### 5. Kolejność
1. Pomiar rozwiązania A na zbiorze zespołu i trzech szerokościach.
2. Uzgodnienie protokołu z opiekunem.
3. Uruchomienie sieci na Jetson Nano i dopasowanie modelu.
4. Pomiar rozwiązania B tym samym protokołem na Nano.
5. Pomiar pomocniczy na telefonie z kamerą i API, tym samym protokołem.
6. Raport z tabelami i prezentacja na spotkaniu 4.
