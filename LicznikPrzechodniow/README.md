# Licznik przechodniów — YOLOv8n i HOG + SVM

Projekt wykrywa sylwetki i nadaje tymczasowe ID. Suma rośnie raz na potwierdzony ślad, nie w każdej klatce. Nie rozpoznaje tożsamości. HOG + SVM pozostaje wariantem bazowym do porównania na zajęciach; domyślny YOLOv8n dodano do trudniejszych scen z dalszymi i częściowo zasłoniętymi osobami. Nie trenowano własnego modelu.

## Windows — instalacja

Python 3.12 64-bit. W folderze projektu:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

YOLO działa przez OpenCV DNN na CPU. Nie wymaga PyTorch, ultralytics ani ONNX Runtime. Model `models/yolov8n.onnx` pobieramy z adresu używanego przez oficjalne przykłady OpenCV:

https://github.com/CVHub520/X-AnyLabeling/releases/download/v0.1.0/yolov8n.onnx

Źródło i kontrolna suma modelu:
https://github.com/opencv/opencv/blob/4.x/samples/dnn/models.yml

Program sprawdza SHA-1 pliku: `68f864475d06e2ec4037181052739f268eeac38d`. Jest to kontrola zgodności eksportu, nie weryfikacja prawa do jego użycia. Model YOLOv8 pochodzi z Ultralytics; przed dystrybucją lub komercjalizacją sprawdź aktualną licencję modelu i warunki Ultralytics (AGPL-3.0 / licencja komercyjna). Modelu nie umieszczamy w Git.

Q/Esc kończy pracę. R zeruje licznik i rozpoczyna nową sesję w CSV. `--source 1` wybiera inną kamerę; przy problemach spróbuj `--backend any`. Kamera powinna widzieć sylwetki.

## Film i pomiary

```powershell
.\.venv\Scripts\python.exe main.py --source "dane\przechodnie.mp4" --csv "wyniki\yolo.csv"
.\.venv\Scripts\python.exe main.py --detector hog --width 640 --confirm-window 3 --max-gap 2 --nms 0.45 --pyramid-scale 1.05 --source "dane\przechodnie.mp4" --csv "wyniki\hog.csv"
```

CSV jest nadpisywany przy tej samej nazwie. Zawiera datę, numer klatki i sesji, czas filmu, rozdzielczość, liczbę wykryć, sumę ID, czasy detekcji/śledzenia/przetwarzania, wersję OpenCV i ustawienia. Nie wylicza precyzji ani czułości bez oznaczeń referencyjnych. FPS to szybkość pętli, nie FPS kamery. Dla filmu tracker korzysta z czasu `numer klatki / FPS materiału`; pliki o zmiennym FPS wymagają dokładniejszej obsługi znaczników czasu.

## Nakładanie się osób i odległość

Domyślne parametry: obraz o szerokości 1280 px, próg YOLO 0.35, NMS 0.60, potwierdzenie po 3 wykryciach w ostatnich 8 klatkach i przechowywanie niewidocznego ID przez 3 s. Prognoza ruchu jest ograniczona do 0.75 s, aby po zasłonięciu nie oddalać jej zbyt mocno.

YOLO otrzymuje obraz z zachowaniem proporcji i dopełnieniem do 640×640, RGB 0–1; odczytujemy tylko klasę person (0) z wyjścia 1×84×8400, bez dodatkowego softmax. Szerokość 1280 px obrazu wyświetlanego nie oznacza wejścia sieci 1280×1280. Dalsi ludzie nadal mogą być zbyt mali lub całkowicie zasłonięci.

Opcje: `--confidence` (YOLO), `--threshold` i `--pyramid-scale` (HOG), `--nms`, `--confirmations`, `--confirm-window`, `--max-gap`, `--width`. Większy NMS zachowuje więcej nakładających się ramek, ale może też pozostawić duplikaty. Niższy próg może zwiększyć fałszywe wykrycia. Dłuższe zachowanie ID może łączyć różne osoby. Nie dobieraj parametrów tylko do oczekiwanej końcowej sumy.

Śledzenie jest heurystyką opartą na prostokątach i ruchu, bez modelu ponownej identyfikacji. Skrzyżowania i zasłonięcia nadal mogą zamieniać ID lub prowadzić do podwójnego liczenia. Osoba, która wyjdzie i wróci po dłuższej przerwie, może zostać policzona ponownie. Licznik nie mierzy unikalnych tożsamości ani kierunkowych wejść i wyjść przez linię. Nie zawiera anti-spoofingu.

## Testy i protokół

```powershell
.\.venv\Scripts\python.exe -m unittest -v
```

Przygotuj minimum 50 ręcznie oznaczonych klatek i osobno nagrania z oznaczonymi trajektoriami. Porównaj HOG i YOLO na tym samym materiale i sprzęcie. Testuj pojedyncze osoby, tłum, mijanie, zasłonięcia, zatrzymanie, wyjście/powrót i pustą scenę. Sama zgodna końcowa suma nie dowodzi prawidłowego śledzenia.

Precyzja i czułość wymagają dopasowania wykrytych ramek do oznaczeń, a nie tylko porównania liczb. Oddziel błąd liczby osób w klatce od błędu sumy przechodniów. Zapisz źródło i licencję materiału, datę, wersję kodu, CPU, kamerę oraz ustawienia. Zmierz wydajność po rozgrzewce na urządzeniu docelowym. Uzgodnij definicję unikalnego przechodnia i dopuszczalny błąd z opiekunem.
