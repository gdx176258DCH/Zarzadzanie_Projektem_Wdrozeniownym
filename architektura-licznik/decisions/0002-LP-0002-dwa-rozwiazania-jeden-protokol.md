# 2. LP-0002 · Dwa rozwiązania i jeden protokół

Date: 2026-11-25

## Status

Proposed

## Context

- Element: Aplikacja licznika
- Źródło: [wnętrze aplikacji]({workspace}/documentation/Licznik%20os%C3%B3b#3)
- Rekomendacja: dostarczyć detektor klasyczny i sieć neuronową, mierzone na tych samych klatkach jednym protokołem.
- Decyzja: zespół projektowy, 25 listopada 2026; czeka na akceptację klienta.

## 1. Potrzeba biznesowa

Klient musi wybrać rozwiązanie, które na jego urządzeniu daje wystarczającą dokładność przy wystarczającej szybkości. Wybór przed pomiarem byłby zgadywaniem.

## 2. Stan obecny, stan docelowy i luka

- Stan obecny: aplikacja ma oba detektory: HOG + SVM oraz YOLOv8n przez OpenCV DNN.
- Stan docelowy: dwie tabele wyników z Jetson Nano, zmierzone na tych samych klatkach, w trzech rozdzielczościach.
- Luka: oznaczone klatki, pomiar na Jetson Nano i optymalizacja sieci.

## 3. Funkcjonalności

1. Wymienny detektor. Wybór rozwiązania jest parametrem uruchomienia.
2. Wspólna ścieżka. Odczyt, skalowanie, śledzenie i rejestr są wspólne dla obu rozwiązań.
3. Porównywalny pomiar. Te same klatki, rozdzielczości i miary.

## 4. Rozważane opcje

1. Dwa rozwiązania w jednej aplikacji
2. Jedno rozwiązanie wybrane przed pomiarem

## 5. Opis opcji

### Opcja A. Dwa rozwiązania w jednej aplikacji

Detektory różnią się jedną częścią aplikacji. Reszta ścieżki jest wspólna.

- Wymienny detektor: tak, parametr uruchomienia.
- Wspólna ścieżka: tak.
- Porównywalny pomiar: tak, jeden protokół.

### Opcja B. Jedno rozwiązanie wybrane przed pomiarem

Mniej pracy, ale wybór opiera się na założeniu, a nie na wynikach.

- Wymienny detektor: nie.
- Wspólna ścieżka: nie dotyczy.
- Porównywalny pomiar: nie, brak drugiej tabeli.

## 6. Koszt opcji

### Opcja A. Dwa rozwiązania w jednej aplikacji

- Wytworzenie: nie uzupełniono
- Wdrożenie: nie uzupełniono
- Używanie: nie uzupełniono
- Utrzymanie: nie uzupełniono
- Inny koszt: nie uzupełniono

### Opcja B. Jedno rozwiązanie wybrane przed pomiarem

- Wytworzenie: nie uzupełniono
- Wdrożenie: nie uzupełniono
- Używanie: nie uzupełniono
- Utrzymanie: nie uzupełniono
- Inny koszt: nie uzupełniono

## 7. Rekomendacja

Opcja A. Klient wybiera na podstawie wyników, a zespół utrzymuje jedną aplikację.

- Łatwiejsze: świadomy wybór klienta, dodanie kolejnego detektora.
- Trudniejsze: dwa pomiary i optymalizacja sieci na urządzeniu.

## 8. Decyzja

- Kto zdecydował: zespół projektowy
- Kiedy: 25 listopada 2026
- Dlaczego: wybór rozwiązania wymaga porównywalnych wyników na sprzęcie docelowym.
- Kogo pytano, a kto nie decydował: klient akceptuje zakres na spotkaniu.

## 9. Niezmienniki chronione przez decyzję

1. Jeden protokół dla obu rozwiązań
   - Musi pozostać prawdziwe: oba rozwiązania są mierzone na tych samych klatkach, rozdzielczościach i miarach.
   - Źródło i powód: porównywalność tabel dla klienta.
   - Wolno zmienić: ustawienia każdego detektora, zapisane przy wyniku.
   - Nie wolno zmienić bez nowej decyzji: osobne zbiory klatek dla rozwiązań.
   - Jak sprawdzić: źródło i lista klatek w protokole każdej tabeli.

## 10. Kiedy zmiana wymaga nowej decyzji

1. Zdarzenie: klient rezygnuje z jednego rozwiązania.
   - Dlaczego narusza obecną decyzję: zmienia się zakres dostawy.
   - Kto podejmuje nową decyzję: klient.

## 11. Związek z innymi elementami

Pomiar odbywa się na urządzeniu z [LP-0004]({workspace}/decisions/Licznik%20os%C3%B3b#4).
