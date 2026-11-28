# Liczenie osób w jednej strefie
## Karta projektu i zespół

**Klient:** mgr inż. Szymon Guzik, opiekun z firmy  
**Wykonawca:** zespół projektowy, pięć osób  
**Data:** 28 listopada 2026  
**Status:** propozycja na spotkanie 2

### 1. Problem klienta
Klient chce znać bieżącą liczbę osób w jednej strefie. Kamera i komputer stoją na miejscu. Obraz zostaje przy kamerze, bo jego wysyłka to dziesiątki megabitów na sekundę. Klient dostaje liczbę i nazwę rozwiązania, które ją podało. Nagrania nie dostaje.

### 2. Cel mierzalny
Proponowany próg odbioru: co najmniej 90% wykrytych osób i co najmniej 10 klatek na sekundę na Jetson Nano. Próg dotyczy obu rozwiązań: detektora klasycznego HOG + SVM i sieci neuronowej. Miary to czułość, precyzja, błąd liczenia i czas klatki na urządzeniu docelowym.

Próg obowiązuje, gdy klient go przyjmie.

### 3. Zakres
| W zakresie | Poza zakresem |
|---|---|
| Jedna kamera, jedna strefa, Jetson Nano | Tożsamość, baza twarzy, emocje |
| Dwa rozwiązania, jeden zbiór klatek | Obraz w chmurze, wiele kamer |
| Protokół, co najmniej 50 oznaczonych klatek | Trenowanie modelu od zera, zakup sprzętu |
| Wynik bez obrazu, raport, prezentacja | Inne wyzwania z katalogu |

### 4. Sprzęt i dane
| Element | Ustalenie |
|---|---|
| Sprzęt | Jetson Nano z kamerą — odbiór wydajności. Telefon komórkowy z kamerą i API — drugie urządzenie testowe. |
| Program | `LicznikPrzechodniow` w repozytorium zespołu. Ma HOG + SVM oraz YOLOv8n przez OpenCV. |
| Dane testowe | Nagranie za zgodą albo zbiór publiczny z licencją. Zbiór wspólny dla obu rozwiązań. |

### 5. Ryzyka
| Ryzyko | Odpowiedź |
|---|---|
| Sieć poniżej 10 klatek na sekundę na Nano | Dopasowanie modelu do urządzenia. Wynik z laptopa nie jest odbiorem. |
| Brak zgody na nagranie | Zbiór publiczny z licencją i opis różnicy wobec miejsca montażu. |
| Różne klatki dla obu rozwiązań | Jeden zbiór i jeden protokół. |
| Zapis twarzy albo cech osoby | Poza zakresem. To identyfikacja osoby. |

### 6. Harmonogram
| Etap | Termin | Rezultat |
|---|---|
| Start | 7 listopada 2026 | Temat i zespół |
| Karta | 25 listopada 2026 | Ten dokument |
| Prototyp HOG + SVM | 28 listopada 2026, 11:20–14:25, sala C314 | Tabela pomiarów i protokół |
| Dane | 29 listopada–12 grudnia 2026 | 50 oznaczonych klatek, pomiar A |
| Sieć na Jetson Nano | 13 grudnia 2026, 8:00–11:05, sala B016 | Pomiar rozwiązania B |
| Odbiór | 23 stycznia 2027, 11:20–14:25, sala B018 | Raport, prezentacja, wybór licznika |


### 7. Zespół
| Imię | Numer albumu |
|---|---|
| Dominik | 83468 |
| Daria | 61707 |
| Ania | 85508 |
| Arek | 84482 |
| Mateusz | 88286 |

Repozytorium zespołu: https://github.com/gdx176258DCH/Zarzadzanie_Projektem_Wdrozeniownym

| Rola | Odpowiedzialność |
|---|---|
| Lider | kontakt z klientem, harmonogram, protokół |
| Model i przetwarzanie obrazu | rozwiązanie A, rozdzielczości, czas klatki |
| Model i przetwarzanie obrazu | rozwiązanie B i dopasowanie do urządzenia |
| Aplikacja i integracja ze sprzętem | uruchomienie na Jetson Nano, wyjście wyniku |
| Testy, dane i dokumentacja | zbiór, oznaczenia, protokół, raport |
