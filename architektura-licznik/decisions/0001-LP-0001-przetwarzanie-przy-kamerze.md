# 1. LP-0001 · Przetwarzanie przy kamerze

Date: 2026-11-25

## Status

Proposed

## Context

- Element: Aplikacja licznika
- Źródło: [kontekst licznika]({workspace}/documentation/Licznik%20os%C3%B3b#1)
- Rekomendacja: przetwarzać obraz na urządzeniu przy kamerze i przekazywać wyłącznie wynik.
- Decyzja: zespół projektowy, 25 listopada 2026; czeka na akceptację klienta.

## 1. Potrzeba biznesowa

Klient potrzebuje bieżącej liczby osób w strefie. Strumień wideo wymaga dziesiątek megabitów na sekundę, a wynik zajmuje kilka bajtów. Obraz osób jest danymi osobowymi, więc im krócej istnieje i im bliżej kamery zostaje, tym mniejsze ryzyko dla klienta.

## 2. Stan obecny, stan docelowy i luka

- Stan obecny: aplikacja licznika liczy osoby na komputerze, do którego podłączona jest kamera, i zapisuje wyniki lokalnie.
- Stan docelowy: urządzenie przy kamerze przekazuje do systemu klienta liczbę osób, czas i nazwę rozwiązania, bez obrazu.
- Luka: połączenie z systemem odbiorcy i jego format.

## 3. Funkcjonalności

1. Liczenie lokalne. Urządzenie przy kamerze wykrywa i liczy osoby.
2. Wynik bez obrazu. Na zewnątrz trafia liczba, czas i nazwa rozwiązania.
3. Praca przy przerwie łącza. Liczenie trwa, gdy system odbiorcy jest niedostępny.

## 4. Rozważane opcje

1. Przetwarzanie przy kamerze
2. Przesyłanie obrazu do serwera lub chmury

## 5. Opis opcji

### Opcja A. Przetwarzanie przy kamerze

Model dobierany jest do możliwości urządzenia. Obraz nie opuszcza strefy.

- Liczenie lokalne: tak, aplikacja działa na urządzeniu przy kamerze.
- Wynik bez obrazu: tak, przekazywana jest tylko liczba.
- Praca przy przerwie łącza: tak, wyniki zapisują się lokalnie.

### Opcja B. Przesyłanie obrazu do serwera lub chmury

Serwer ma większą moc obliczeniową, ale wymaga stałego łącza o dużej przepustowości i przenosi obraz osób poza strefę.

- Liczenie lokalne: nie.
- Wynik bez obrazu: nie, obraz trafia na serwer.
- Praca przy przerwie łącza: nie.

## 6. Koszt opcji

### Opcja A. Przetwarzanie przy kamerze

- Wytworzenie: nie uzupełniono
- Wdrożenie: nie uzupełniono
- Używanie: nie uzupełniono
- Utrzymanie: nie uzupełniono
- Inny koszt: nie uzupełniono

### Opcja B. Przesyłanie obrazu do serwera lub chmury

- Wytworzenie: nie uzupełniono
- Wdrożenie: nie uzupełniono
- Używanie: nie uzupełniono
- Utrzymanie: nie uzupełniono
- Inny koszt: nie uzupełniono

## 7. Rekomendacja

Opcja A. Spełnia potrzebę klienta bez przesyłania obrazu i działa przy przerwie łącza.

- Łatwiejsze: ochrona danych osobowych, praca bez stałego łącza, mały ruch sieciowy.
- Trudniejsze: model musi zmieścić się w możliwościach urządzenia; sieć neuronowa wymaga optymalizacji.

## 8. Decyzja

- Kto zdecydował: zespół projektowy
- Kiedy: 25 listopada 2026
- Dlaczego: obraz osób nie powinien opuszczać strefy, a wynik zajmuje kilka bajtów.
- Kogo pytano, a kto nie decydował: klient akceptuje zakres na spotkaniu. Status pozostaje Proposed do tej akceptacji.

## 9. Niezmienniki chronione przez decyzję

1. Obraz zostaje przy kamerze
   - Musi pozostać prawdziwe: na zewnątrz urządzenia trafia tylko liczba osób, czas i nazwa rozwiązania.
   - Źródło i powód: potrzeba klienta i ochrona danych osobowych.
   - Wolno zmienić: format komunikatu i częstotliwość wysyłki.
   - Nie wolno zmienić bez nowej decyzji: wysyłanie obrazu lub klatek poza urządzenie.
   - Jak sprawdzić: przegląd danych wysyłanych przez wyjście wyniku.

## 10. Kiedy zmiana wymaga nowej decyzji

1. Zdarzenie: klient prosi o podgląd obrazu na zewnątrz.
   - Dlaczego narusza obecną decyzję: obraz osób opuszcza strefę.
   - Kto podejmuje nową decyzję: klient razem z zespołem.

## 11. Związek z innymi elementami

Wybór urządzenia opisuje [LP-0004]({workspace}/decisions/Licznik%20os%C3%B3b#4).
