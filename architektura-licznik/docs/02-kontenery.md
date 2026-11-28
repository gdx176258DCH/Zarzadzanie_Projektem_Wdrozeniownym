## Kamera, aplikacja i pliki

Licznik składa się z kamery, aplikacji licznika oraz dwóch rodzajów plików: wag sieci neuronowej i wyników pomiarów.

![Kamera, aplikacja licznika i pliki, z których korzysta](embed:LP-Kontenery)

Aplikacja odczytuje klatki z kamery, wykrywa osoby i liczy je. Rozwiązanie B wczytuje wagi sieci YOLOv8n z pliku ONNX. Wagi nie są przechowywane w repozytorium kodu.

Każdy pomiar trafia do pliku CSV: jeden plik na rozwiązanie i rozdzielczość. Zespół porównuje te pliki z ręcznie oznaczonymi klatkami i wylicza czułość, precyzję oraz błąd liczenia.

Przekazanie wyniku do systemu odbiorcy jest planowane. Zakres połączenia ustala klient: format komunikatu, częstotliwość i adres serwera.
