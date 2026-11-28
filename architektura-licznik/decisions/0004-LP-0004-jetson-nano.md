# 4. LP-0004 · Jetson Nano jako urządzenie odbioru

Date: 2026-11-25

## Status

Proposed

## Context

- Element: Jetson Nano
- Źródło: [rozmieszczenie w strefie klienta]({workspace}/documentation/Licznik%20os%C3%B3b#5)
- Rekomendacja: mierzyć i odbierać wydajność na NVIDIA Jetson Nano.
- Decyzja: zespół projektowy, 25 listopada 2026; czeka na akceptację klienta.

## 1. Potrzeba biznesowa

Wydajność licznika zależy od sprzętu. Klient potrzebuje wyniku z urządzenia, które będzie pracować w strefie, a nie z komputera zespołu.

## 2. Stan obecny, stan docelowy i luka

- Stan obecny: zespół dysponuje Jetson Nano; aplikacja działa na komputerze z Pythonem i OpenCV.
- Stan docelowy: oba rozwiązania zmierzone na Jetson Nano, sieć dopasowana przez TensorRT i int8.
- Luka: uruchomienie środowiska na Jetson Nano i optymalizacja sieci.

## 3. Funkcjonalności

1. Pomiar na sprzęcie docelowym. Tabela wyników pochodzi z urządzenia w strefie.
2. Przyspieszenie sieci. Sieć korzysta z procesora graficznego urządzenia.

## 4. Rozważane opcje

1. NVIDIA Jetson Nano
2. Raspberry Pi

## 5. Opis opcji

### Opcja A. NVIDIA Jetson Nano

Mały komputer z procesorem graficznym i obsługą TensorRT.

- Pomiar na sprzęcie docelowym: tak.
- Przyspieszenie sieci: tak, TensorRT i int8.

### Opcja B. Raspberry Pi

Tańszy i popularny, bez procesora graficznego do sieci neuronowych; wymaga osobnego akceleratora.

- Pomiar na sprzęcie docelowym: tak.
- Przyspieszenie sieci: nie, bez dodatkowego akceleratora.

## 6. Koszt opcji

### Opcja A. NVIDIA Jetson Nano

- Wytworzenie: nie uzupełniono
- Wdrożenie: nie uzupełniono
- Używanie: nie uzupełniono
- Utrzymanie: nie uzupełniono
- Inny koszt: brak, zespół dysponuje urządzeniem

### Opcja B. Raspberry Pi

- Wytworzenie: nie uzupełniono
- Wdrożenie: nie uzupełniono
- Używanie: nie uzupełniono
- Utrzymanie: nie uzupełniono
- Inny koszt: zakup urządzenia i akceleratora

## 7. Rekomendacja

Opcja A. Zespół ma urządzenie, a procesor graficzny daje sieci realną szansę na próg 10 klatek na sekundę.

- Łatwiejsze: optymalizacja sieci, pomiar bez zakupu sprzętu.
- Trudniejsze: konfiguracja JetPack i TensorRT.

## 8. Decyzja

- Kto zdecydował: zespół projektowy
- Kiedy: 25 listopada 2026
- Dlaczego: zespół ma urządzenie, a sieć potrzebuje procesora graficznego.
- Kogo pytano, a kto nie decydował: klient potwierdza, czy pomiar na Jetson Nano zamyka odbiór wydajności.

## 9. Niezmienniki chronione przez decyzję

1. Odbiór wydajności na sprzęcie docelowym
   - Musi pozostać prawdziwe: wynik wydajności w odbiorze pochodzi z Jetson Nano.
   - Źródło i powód: wydajność zależy od sprzętu.
   - Wolno zmienić: pomiary pomocnicze na innym sprzęcie, opisane jego nazwą.
   - Nie wolno zmienić bez nowej decyzji: odbiór na podstawie wyniku z laptopa.
   - Jak sprawdzić: kolumna sprzętu w tabeli wyników.

## 10. Kiedy zmiana wymaga nowej decyzji

1. Zdarzenie: klient wskazuje inne urządzenie docelowe.
   - Dlaczego narusza obecną decyzję: zmienia się sprzęt odbioru.
   - Kto podejmuje nową decyzję: klient.

## 11. Związek z innymi elementami

Przetwarzanie przy kamerze opisuje [LP-0001]({workspace}/decisions/Licznik%20os%C3%B3b#1).
