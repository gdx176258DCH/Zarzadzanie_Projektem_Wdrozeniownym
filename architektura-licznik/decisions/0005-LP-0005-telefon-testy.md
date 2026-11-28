# 5. LP-0005 · Telefon jako drugie urządzenie testowe

Date: 2026-11-28

## Status

Proposed

## Context

- Element: Telefon komórkowy
- Źródło: [testy na telefonie]({workspace}/documentation/Licznik%20os%C3%B3b#7)
- Rekomendacja: dodać telefon z kamerą i API wyniku jako drugie urządzenie testowe obok Jetson Nano.
- Decyzja: Ania, 28 listopada 2026; czeka na akceptację klienta jako zakresu testów.

## 1. Potrzeba biznesowa

Klient i zespół chcą zobaczyć, jak licznik zachowuje się nie tylko na Jetson Nano, lecz także na telefonie. Telefon jest łatwiej dostępny w terenie. Wynik może iść przez API do systemu odbiorcy.

## 2. Stan obecny, stan docelowy i luka

- Stan obecny: odbiór wydajności jest zaplanowany na Jetson Nano; aplikacja działa na komputerze z Pythonem.
- Stan docelowy: te same rozwiązania i protokół zmierzone także na telefonie; tabela z telefonu jest osobno podpisana.
- Luka: wybór systemu operacyjnego telefonu, sposób uruchomienia aplikacji albo klienta API oraz format API.

## 3. Funkcjonalności

1. Drugi pomiar. Te same klatki i miary na telefonie.
2. Wynik przez API. Liczba osób, czas i nazwa rozwiązania trafiają do systemu odbiorcy.
3. Rozróżnienie sprzętu. Wynik z telefonu nie jest podpisany jako Jetson Nano.

## 4. Rozważane opcje

1. Tylko Jetson Nano
2. Jetson Nano do odbioru oraz telefon do dodatkowych testów

## 5. Opis opcji

### Opcja A. Tylko Jetson Nano

Jeden sprzęt, prostszy raport.

- Drugi pomiar: nie.
- Wynik przez API: możliwe także z Nano.
- Rozróżnienie sprzętu: nie dotyczy.

### Opcja B. Jetson Nano do odbioru oraz telefon do dodatkowych testów

Odbiór zostaje na Nano. Telefon daje drugą tabelę i doświadczenie z API.

- Drugi pomiar: tak.
- Wynik przez API: tak, planowane.
- Rozróżnienie sprzętu: tak, kolumna sprzętu w protokole.

## 6. Koszt opcji

### Opcja A. Tylko Jetson Nano

- Wytworzenie: nie uzupełniono
- Wdrożenie: nie uzupełniono
- Używanie: nie uzupełniono
- Utrzymanie: nie uzupełniono
- Inny koszt: nie uzupełniono

### Opcja B. Jetson Nano do odbioru oraz telefon do dodatkowych testów

- Wytworzenie: nie uzupełniono
- Wdrożenie: nie uzupełniono
- Używanie: nie uzupełniono
- Utrzymanie: nie uzupełniono
- Inny koszt: telefon zespołu; bez zakupu osobnego urządzenia brzegowego

## 7. Rekomendacja

Opcja B. Nano zamyka odbiór wydajności. Telefon poszerza testy bez zmiany progu odbioru.

- Łatwiejsze: porównanie sprzętów, pokaz API.
- Trudniejsze: drugi zestaw pomiarów i ustalenie sposobu uruchomienia na telefonie.

## 8. Decyzja

- Kto zdecydował: Ania
- Kiedy: 28 listopada 2026
- Dlaczego: drugie urządzenie do testów obok Jetson Nano.
- Kogo pytano, a kto nie decydował: klient akceptuje zakres testów na spotkaniu. Status pozostaje Proposed do tej akceptacji.

## 9. Niezmienniki chronione przez decyzję

1. Odbiór wydajności zostaje na Jetson Nano
   - Musi pozostać prawdziwe: tabela z telefonu nie zastępuje tabeli z Nano w odbiorze wydajności.
   - Źródło i powód: LP-0004 oraz decyzja Ani o drugim urządzeniu testowym.
   - Wolno zmienić: system operacyjny telefonu i sposób uruchomienia aplikacji.
   - Nie wolno zmienić bez nowej decyzji: uznanie samego telefonu za odbiór wydajności zamiast Nano.
   - Jak sprawdzić: kolumna sprzętu w protokole i raport odbioru.

## 10. Kiedy zmiana wymaga nowej decyzji

1. Zdarzenie: klient chce, żeby telefon zamykał odbiór wydajności zamiast Jetson Nano.
   - Dlaczego narusza obecną decyzję: zmienia sprzęt odbioru.
   - Kto podejmuje nową decyzję: klient.

## 11. Związek z innymi elementami

Sprzęt odbioru opisuje [LP-0004]({workspace}/decisions/Licznik%20os%C3%B3b#4).
