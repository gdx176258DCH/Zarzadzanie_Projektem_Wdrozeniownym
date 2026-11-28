# Liczenie osób w jednej strefie

Projekt zespołowy z przedmiotu Zarządzanie projektem wdrożeniowym, WSB Merito Gdańsk, semestr zimowy 2026/2027.

Klient chce znać bieżącą liczbę osób w jednej strefie. Kamera i mały komputer stoją na miejscu. Obraz zostaje przy kamerze. Na zewnątrz wychodzi tylko liczba osób i nazwa rozwiązania, które ją podało.

## Zakres

| W zakresie | Poza zakresem |
|---|---|
| Jedna kamera, jedna strefa; Jetson Nano do odbioru; telefon do testów | Tożsamość, baza twarzy, emocje |
| Dwa rozwiązania porównane na tych samych klatkach | Obraz w chmurze, wiele kamer |
| Protokół pomiarów, co najmniej 50 oznaczonych klatek | Trenowanie modelu od zera |

Program nadaje osobie tymczasowy numer śladu, żeby nie liczyć jej dwa razy. Numer żyje najwyżej kilka sekund, nie zostaje po sesji i nie wskazuje tożsamości.

## Dwa rozwiązania

- **Rozwiązanie A:** klasyczny detektor HOG + SVM z OpenCV.
- **Rozwiązanie B:** sieć neuronowa YOLOv8n uruchamiana przez OpenCV DNN, docelowo dopasowana do Jetson Nano (TensorRT, int8).

Proponowany próg odbioru: co najmniej 90% wykrytych osób i co najmniej 10 klatek na sekundę na Jetson Nano.

## Struktura repozytorium

| Katalog | Zawartość |
|---|---|
| [`LicznikPrzechodniow/`](LicznikPrzechodniow/) | Program licznika, testy, Dockerfile. Instrukcja instalacji i uruchomienia jest w [README aplikacji](LicznikPrzechodniow/README.md). |
| [`architektura-licznik/`](architektura-licznik/) | Model Structurizr: widoki, dokumentacja, decyzje ADR. |
| [`materialy-dla-klienta/`](materialy-dla-klienta/) | Brief, oferta i karta projektu. |
| [`materialy-do-oddania/`](materialy-do-oddania/) | Karta z zespołem, protokół pomiarów, plan etapu 3. |
| [`przeglad-klienta-2026-11-28/`](przeglad-klienta-2026-11-28/) | Paczka na przegląd z klientem 28 listopada 2026. |

Filmy (`dane/`), wyniki pomiarów (`wyniki/`) i model (`models/`) nie trafiają do Gita.

## Szybki start

```bash
cd LicznikPrzechodniow
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m unittest -v
.venv/bin/python main.py --detector hog --width 640 --no-display --source dane/<film> --csv wyniki/hog-640.csv
```

Polecenia dla Windows i opis wszystkich opcji są w [README aplikacji](LicznikPrzechodniow/README.md).

## Pomiary według protokołu

Oba rozwiązania mierzymy w trzech szerokościach obrazu, na tym samym filmie i z tymi samymi ustawieniami. Polecenia uruchamiamy w katalogu `LicznikPrzechodniow`.

Wspólne ustawienia:

```text
--confirm-window 3 --max-gap 2 --nms 0.45 --pyramid-scale 1.05 --no-display --source dane/<film>
```

Rozwiązanie A, HOG + SVM:

```bash
.venv/bin/python main.py --detector hog --width 1024 --confirm-window 3 --max-gap 2 --nms 0.45 --pyramid-scale 1.05 --no-display --source dane/<film> --csv wyniki/hog-1024.csv
.venv/bin/python main.py --detector hog --width 640  --confirm-window 3 --max-gap 2 --nms 0.45 --pyramid-scale 1.05 --no-display --source dane/<film> --csv wyniki/hog-640.csv
.venv/bin/python main.py --detector hog --width 320  --confirm-window 3 --max-gap 2 --nms 0.45 --pyramid-scale 1.05 --no-display --source dane/<film> --csv wyniki/hog-320.csv
```

Rozwiązanie B, YOLOv8n: te same polecenia z `--detector yolo` i plikami `wyniki/yolo-<szerokość>.csv`. Opcja `--pyramid-scale` dotyczy tylko HOG.

Plik CSV zawiera dla każdej klatki liczbę wykryć, czasy detekcji, śledzenia i przetwarzania, wersję OpenCV i ustawienia. Precyzję i czułość liczymy osobno, z ręcznie oznaczonych klatek.

## Dane testowe

Pierwszy materiał to film „Calle preciados” z Wikimedia Commons, autor OsvaldoGago, licencja [CC BY-SA](https://commons.wikimedia.org/wiki/File:Calle_preciados.ogv). Plik nie jest w repozytorium. Każdy wynik zapisujemy z datą, wersją kodu, sprzętem, rozdzielczością i ustawieniami.

## Harmonogram

| Etap | Termin | Rezultat |
|---|---|---|
| Start | 7 listopada 2026 | Temat i zespół |
| Prototyp HOG + SVM | 28 listopada 2026 | Tabela pomiarów i protokół |
| Sieć na Jetson Nano | 13 grudnia 2026 | Pomiar rozwiązania B |
| Odbiór | 23 stycznia 2027 | Raport, prezentacja, wybór rozwiązania |

## Zespół

Dominik, Daria, Ania, Arek, Mateusz.
