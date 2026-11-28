## Przetworzenie jednej klatki

Przebieg pokazuje, co dzieje się z jedną klatką przy rozwiązaniu A. Rozwiązanie B przechodzi tę samą drogę; różni się tylko detektorem.

![Przetworzenie jednej klatki rozwiązaniem A](embed:LP-Klatka)

Przebieg zaczyna się od odczytu klatki i kończy zapisem wiersza pomiaru. Czas mierzony jest osobno dla wykrywania, śledzenia i całego przetwarzania. Te czasy trafiają do tabeli wyników w protokole.

Gdy kamera przestanie dostarczać obraz, aplikacja kończy pracę z komunikatem. Wyniki zapisane do tej chwili zostają w pliku pomiarów. Przy pliku wideo koniec nagrania kończy pomiar i aplikacja podaje sumę potwierdzonych osób.

Klatka nie jest zapisywana. Po przetworzeniu zostaje tylko liczba osób, czasy i ustawienia.
