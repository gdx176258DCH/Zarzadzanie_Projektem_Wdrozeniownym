## Wnętrze aplikacji licznika

Aplikacja ma jedną ścieżkę przetwarzania klatki i dwa wymienne detektory. Dzięki temu oba rozwiązania liczą te same klatki w tych samych warunkach.

![Odpowiedzialności aplikacji: od odczytu klatki do wyniku i pomiaru](embed:LP-Aplikacja)

| Część | Odpowiedzialność | Co zmienia się przy zmianie wymagań |
|---|---|---|
| Odczyt obrazu | Pobiera klatki z kamery albo z pliku wideo | Nowe źródło obrazu |
| Skalowanie | Zmniejsza klatkę do szerokości z parametru; w protokole: 1024, 640 i 320 pikseli | Wybrana rozdzielczość |
| Rozwiązanie A: HOG + SVM | Wykrywa sylwetki klasyczną metodą | Progi detektora |
| Rozwiązanie B: YOLOv8n | Wykrywa osoby siecią neuronową | Model i jego optymalizacja na urządzeniu |
| Śledzenie | Łączy wykrycia w krótkie ślady i liczy każdą osobę raz | Reguła liczenia unikalnej osoby |
| Rejestr pomiarów | Zapisuje liczbę wykryć, czasy i ustawienia | Zakres danych w protokole |
| Wyjście wyniku | Planowane: przekazuje liczbę osób do systemu odbiorcy | Format i adres wskazane przez klienta |

Śledzenie nadaje sylwetce tymczasowy numer, aby ta sama osoba nie była liczona w każdej klatce. Numer istnieje najwyżej 3 sekundy po zniknięciu osoby z kadru, nie jest zapisywany po sesji i nie wskazuje tożsamości.

Wybór rozwiązania i rozdzielczości to parametr uruchomienia. Zmiana detektora nie wymaga zmian w śledzeniu ani w rejestrze pomiarów.
