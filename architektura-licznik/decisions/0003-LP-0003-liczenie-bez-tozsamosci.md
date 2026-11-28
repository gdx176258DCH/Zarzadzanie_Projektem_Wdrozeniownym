# 3. LP-0003 · Liczenie bez tożsamości

Date: 2026-11-25

## Status

Proposed

## Context

- Element: Śledzenie
- Źródło: [wnętrze aplikacji]({workspace}/documentation/Licznik%20os%C3%B3b#3)
- Rekomendacja: liczyć sylwetki z tymczasowym numerem śladu, bez zapisu cech twarzy i bez bazy osób.
- Decyzja: zespół projektowy, 25 listopada 2026; czeka na akceptację klienta.

## 1. Potrzeba biznesowa

Klient potrzebuje liczby osób, nie ich tożsamości. Identyfikacja osób podlega rozporządzeniu UE 2024/1689 (AI Act): wymaga oceny zgodności, rejestracji i nadzoru człowieka, a kary sięgają 35 mln euro albo 7% światowego obrotu.

## 2. Stan obecny, stan docelowy i luka

- Stan obecny: aplikacja nadaje sylwetce tymczasowy numer śladu i nie zapisuje go na dysk.
- Stan docelowy: to samo zachowanie na urządzeniu docelowym, przy obu rozwiązaniach.
- Luka: brak.

## 3. Funkcjonalności

1. Jednokrotne liczenie. Ta sama osoba jest liczona raz, mimo wielu klatek.
2. Brak tożsamości. Numer śladu nie wskazuje osoby i nie zostaje po sesji.
3. Brak zapisu obrazu. Klatka nie jest zapisywana po przetworzeniu.

## 4. Rozważane opcje

1. Krótki ślad sylwetki
2. Ponowne rozpoznawanie osoby na podstawie cech wyglądu

## 5. Opis opcji

### Opcja A. Krótki ślad sylwetki

Śledzenie łączy ramki z kolejnych klatek na podstawie położenia i ruchu. Numer znika najwyżej 3 sekundy po zniknięciu osoby z kadru.

- Jednokrotne liczenie: tak, w obrębie krótkiej obecności w kadrze.
- Brak tożsamości: tak.
- Brak zapisu obrazu: tak.

### Opcja B. Ponowne rozpoznawanie osoby

Dokładniejsze przy powrotach do kadru, ale wymaga zapisu cech wyglądu, czyli danych biometrycznych.

- Jednokrotne liczenie: tak, także po powrocie osoby.
- Brak tożsamości: nie.
- Brak zapisu obrazu: nie, cechy muszą być przechowywane.

## 6. Koszt opcji

### Opcja A. Krótki ślad sylwetki

- Wytworzenie: nie uzupełniono
- Wdrożenie: nie uzupełniono
- Używanie: nie uzupełniono
- Utrzymanie: nie uzupełniono
- Inny koszt: nie uzupełniono

### Opcja B. Ponowne rozpoznawanie osoby

- Wytworzenie: nie uzupełniono
- Wdrożenie: nie uzupełniono
- Używanie: nie uzupełniono
- Utrzymanie: nie uzupełniono
- Inny koszt: obowiązki systemu wysokiego ryzyka według rozporządzenia UE 2024/1689

## 7. Rekomendacja

Opcja A. Daje liczbę osób bez przetwarzania danych biometrycznych.

- Łatwiejsze: zgodność z przepisami, prostsza obsługa danych.
- Trudniejsze: osoba, która wróci do kadru po dłuższej przerwie, może zostać policzona ponownie.

## 8. Decyzja

- Kto zdecydował: zespół projektowy
- Kiedy: 25 listopada 2026
- Dlaczego: zlecenie dotyczy liczby osób, a identyfikacja podlega osobnym obowiązkom prawnym.
- Kogo pytano, a kto nie decydował: klient akceptuje zakres na spotkaniu. Status pozostaje Proposed do tej akceptacji.

## 9. Niezmienniki chronione przez decyzję

1. Brak tożsamości w wyniku
   - Musi pozostać prawdziwe: licznik nie zapisuje cech twarzy ani wyglądu, a numer śladu nie zostaje po sesji.
   - Źródło i powód: zakres zlecenia i rozporządzenie UE 2024/1689.
   - Wolno zmienić: czas życia numeru śladu w granicy kilku sekund.
   - Nie wolno zmienić bez nowej decyzji: zapis cech osoby, baza twarzy, analiza emocji.
   - Jak sprawdzić: przegląd kolumn pliku pomiarów i danych wyjścia wyniku.

## 10. Kiedy zmiana wymaga nowej decyzji

1. Zdarzenie: klient prosi o informację, kto przebywał w strefie.
   - Dlaczego narusza obecną decyzję: to identyfikacja osób, czyli inne zlecenie.
   - Kto podejmuje nową decyzję: klient, po ocenie obowiązków prawnych.

## 11. Związek z innymi elementami

Obraz pozostaje przy kamerze zgodnie z [LP-0001]({workspace}/decisions/Licznik%20os%C3%B3b#1).
