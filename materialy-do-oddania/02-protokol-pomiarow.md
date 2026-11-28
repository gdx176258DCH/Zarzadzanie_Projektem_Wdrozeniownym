# Liczenie osób w jednej strefie
## Protokół pomiarów

**Do uzgodnienia z:** mgr inż. Szymon Guzik, opiekun z firmy, mailowo  
**Data:** 28 listopada 2026  
**Status:** szkic do uzgodnienia z opiekunem

### 1. Cel pomiaru
Protokół mówi klientowi, kiedy wynik liczenia osób jest wiarygodny. Ten sam protokół obowiązuje detektor klasyczny i sieć neuronową. Klient porównuje dwie tabele zmierzone na tych samych klatkach.

### 2. Zbiór testowy
| Element | Ustalenie |
|---|---|
| Liczba klatek | co najmniej 50 |
| Pochodzenie | miejsce montażu kamery za zgodą albo zbiór publiczny z licencją |
| Oznaczenie | liczba osób na klatce oznaczona ręcznie; ramki osób do liczenia precyzji i czułości |
| Opis | źródło, licencja albo zgoda, data, kamera |
| Wykluczenie | obrazy wygenerowane przez sztuczną inteligencję |
| Ochrona osób | twarze rozmyte; do raportu nie wchodzi klatka z rozpoznawalną twarzą |

### 3. Miary
| Miara | Znaczenie |
|---|---|
| Czułość | jaki udział prawdziwych osób detektor znalazł |
| Precyzja | jaki udział ramek pokazuje osobę |
| Błąd liczenia | różnica między liczbą wykrytą a liczbą oznaczoną na klatce |
| Czas klatki | milisekundy na klatkę na Jetson Nano, po rozgrzewce, i wynikowe klatki na sekundę |

Precyzja i czułość wymagają dopasowania ramek do oznaczeń. Porównanie samych liczb ich nie daje. Błąd liczby osób na klatce jest osobną miarą od błędu sumy przechodniów w nagraniu.

### 4. Warunki
Dzień, noc, deszcz, tłum i różne odległości od kamery. Klient wskazuje, które z nich są obowiązkowe przy odbiorze.

### 5. Zapis każdego wyniku
Data, wersja kodu (commit), nazwa rozwiązania, sprzęt, rozdzielczość i ustawienia detektora. Odbiór wydajności podpisujemy jako Jetson Nano. Wynik z laptopa lub telefonu jest opisany nazwą tego sprzętu i ma charakter pomocniczy.

### 6. Program i uruchomienie
Pomiar wykonuje program licznika z repozytorium zespołu. Oba rozwiązania są mierzone w trzech szerokościach obrazu: 1024, 640 i 320 pikseli, z tymi samymi ustawieniami. Program zapisuje dla każdej klatki liczbę wykryć, czasy przetwarzania, wersję oprogramowania i ustawienia. Precyzję i czułość wyliczamy z ręcznych oznaczeń. Polecenia uruchomienia opisuje README repozytorium.

### 7. Tabela pomiarów
Rozwiązanie A, HOG + SVM

| Rozdzielczość | Wykryte | Prawdziwe | ms na klatkę | Klatki na sekundę | Sprzęt | Data i wersja |
|---|---|---|---|---|---|---|
| 1024 px | – | – | – | – | – | – |
| 640 px | – | – | – | – | – | – |
| 320 px | – | – | – | – | – | – |

Rozwiązanie B, sieć neuronowa

| Rozdzielczość | Wykryte | Prawdziwe | ms na klatkę | Klatki na sekundę | Sprzęt | Data i wersja |
|---|---|---|---|---|---|---|
| 1024 px | – | – | – | – | – | – |
| 640 px | – | – | – | – | – | – |
| 320 px | – | – | – | – | – | – |

Przy każdej tabeli stoi wynik: próg spełniony albo niespełniony.

### 8. Decyzje opiekuna
1. Czy próg 90% wykrytych osób i 10 klatek na sekundę na Jetson Nano jest progiem odbioru?
2. Które warunki są obowiązkowe?
3. Jak liczymy unikalnego przechodnia i jaki błąd sumy jest dopuszczalny?
4. Skąd pochodzą klatki i kto daje zgodę na nagranie?
