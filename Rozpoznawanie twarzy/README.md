# YuNet + SFace + pasywny anti-spoofing

Wersja zintegrowana z prototypem w folderze na D. Zachowuje bazę faces, domyślną kamerę 640×480, pomiary FPS i czasu AI oraz reset klawiszem R. Oryginalny main.py zachowano w kopii main.przed_pas_fas.py.bak. Plik liveness_test.py to dawny, oddzielny test mrugania; nie służy do uruchamiania nowej weryfikacji. Nie wymaga MediaPipe ani mrugania. FPS i czas przetwarzania są widoczne w oknie.

## Instalacja na Windows (PowerShell)

Uruchom polecenia w folderze projektu. Zalecany Python 3.11 lub 3.12, 64-bit.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
New-Item -ItemType Directory -Force models, faces
```

Pobierz te trzy pliki (linki prowadzą bezpośrednio do modeli):

* [face_detection_yunet_2023mar.onnx](https://github.com/opencv/opencv_zoo/raw/refs/heads/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx)
* [face_recognition_sface_2021dec.onnx](https://github.com/opencv/opencv_zoo/raw/refs/heads/main/models/face_recognition_sface/face_recognition_sface_2021dec.onnx)
* [MiniFASNetV2.onnx](https://github.com/yakhyo/face-anti-spoofing/releases/download/weights/MiniFASNetV2.onnx)

Zapisz je pod dokładnie tymi nazwami w `models`. Pobierz pliki binarne, a nie stronę HTML lub wskaźnik Git LFS. SFace zajmuje około 37 MB, a MiniFASNet około 2 MB. Zapoznaj się z licencjami modeli przed wykorzystaniem poza prototypem.

Przykładowa baza zdjęć:

```text
faces/
  Jan Kowalski/
    przod.jpg
    lekki_obrot.jpg
  Anna Nowak/
    przod.jpg
```

Każde zdjęcie musi zawierać dokładnie jedną twarz. Użyj kilku ostrych zdjęć z różnych sesji. Obsługiwane są także pliki bez podfolderów, np. `faces/osoba_A.jpg`. Nie mieszaj obu sposobów dla tej samej osoby. Zdjęcia referencyjne są zaufanym źródłem tożsamości; model FAS nie sprawdza procesu ich dodawania.

```powershell
.\.venv\Scripts\python.exe main.py
```

Zakończenie: Q lub Esc. Reset serii: R. Inna kamera: `--camera 1`. Jeśli kamera się nie otwiera, zamknij aplikacje korzystające z niej i spróbuj `--backend any`.

## Polskie znaki w ścieżkach

Ścieżki domyślne odnoszą się do folderu main.py, a nie bieżącego katalogu terminala. Zdjęcia są wczytywane przez `Path.read_bytes` i `imdecode`, model FAS przez OpenCV DNN z bufora bajtów. Modele YuNet i SFace są kopiowane na czas działania do folderu tymczasowego o ścieżce ASCII, co omija problemy natywnych loaderów OpenCV ze znakami Unicode. Folder projektu może zawierać polskie znaki. Jeśli także ścieżka TEMP ma znaki spoza ASCII, ustaw na czas tej sesji istniejący, zapisywalny folder ASCII, np.:

```powershell
New-Item -ItemType Directory -Force C:\Temp
$env:TEMP = 'C:\Temp'
$env:TMP = 'C:\Temp'
.\.venv\Scripts\python.exe main.py
```

Nazwy osób z polskimi znakami są poprawne w bazie i konsoli; standardowa czcionka okna OpenCV zastępuje te znaki znakiem `?`.

## Kontrakt modelu i decyzja

Kod obsługuje konkretnie eksport **MiniFASNetV2 z repozytorium yakhyo**: wejście float32 NCHW 1×3×80×80, BGR, wartości 0–255, bez dzielenia przez 255, kontekstowy crop 2.7×, trzy logity wyjściowe i klasa żywej twarzy pod indeksem 1. Softmax wykonywany jest raz, w main.py. Nie podmieniaj modelu na przypadkowy plik ONNX o tej samej nazwie: inne eksporty mogą wymagać innego przetwarzania.

Źródła: [referencyjne przetwarzanie ONNX](https://github.com/yakhyo/face-anti-spoofing/blob/main/onnx_inference.py), [modele i eksport](https://github.com/yakhyo/face-anti-spoofing), [oryginalny Silent-Face](https://github.com/minivision-ai/Silent-Face-Anti-Spoofing), [SFace OpenCV](https://github.com/opencv/opencv_zoo/tree/main/models/face_recognition_sface).

W każdej odczytanej klatce wykonywana jest detekcja, a dla jednej dostatecznie dużej twarzy także FAS i SFace. Zliczane są wyłącznie kolejne klatki, które spełniają wszystkie warunki:

1. Dokładnie jedna twarz, w całości w kadrze, minimum 100 px na krótszym boku.
2. FAS wybiera klasę real oraz jej wynik wynosi co najmniej 0.90.
3. SFace wybiera tę samą osobę, podobieństwo cosinusowe wynosi co najmniej 0.363, a przewaga nad drugą osobą co najmniej 0.05.
4. Prostokąt twarzy zachowuje ciągłość (IoU ≥ 0.3), a odstęp między pomiarami nie przekracza 1 s.

Po trzeciej klatce pojawia się `OK`. Każdy niespełniony warunek zeruje serię; zmiana osoby lub utrata ciągłości rozpoczyna serię od 1. Wynik nie jest utrzymywany przez kilka sekund po utracie twarzy. Przy błędzie modelu program kończy pracę i zwalnia kamerę. Nie istnieje awaryjna ścieżka akceptacji bez FAS. Ciągłość prostokąta jest heurystyką, nie pełnym trackerem tożsamości.

Wynik FAS to ocena modelu, nie skalibrowane prawdopodobieństwo bezpieczeństwa. Pasywny model RGB może przepuścić zdjęcie, nagranie lub inny atak; trzy sąsiednie klatki są silnie skorelowane. Nie traktuj prototypu jako gotowego zabezpieczenia dostępu. Brak mrugnięcia nie jest ani błędem, ani powodem odrzucenia. `NIEZWERYFIKOWANA FAS` oznacza brak spełnienia progu, nie dowód oszustwa.

## Testy na docelowej kamerze

| Próba | Oczekiwane zachowanie |
|---|---|
| Osoba z bazy, patrzy spokojnie bez mrugania | 1/3 → 2/3 → OK, jeśli spełnia progi |
| Osoba spoza bazy | NIEZNANA, bez OK |
| Twarz znika po dwóch klatkach | Seria resetuje się; po powrocie 1/3 |
| Druga osoba w kadrze | WIELE TWARZY, reset |
| Zmiana osoby | Brak przenoszenia serii między nazwami |
| Zdjęcie na papierze, na ekranie, odtwarzane wideo | Oczekiwane odrzucenie FAS; każdy przypadek OK zapisz jako fałszywą akceptację |
| Słabe światło, okulary, różne odległości | Zapisz odrzucenia prawdziwej osoby i FPS |
| Przeniesienie projektu do folderu `Próba rozpoznawania` | Zdjęcia i modele nadal się wczytują |
| Brak/uszkodzony model albo odłączenie kamery | Błąd i zakończenie, bez akceptacji |

Przeprowadź osobne sesje dla rejestracji, strojenia progów i końcowych testów. Testuj różne osoby, urządzenia wyświetlające, jasność ekranu, wydruki, kąty i odległości. Notuj liczbę prób oraz fałszywe akceptacje i odrzucenia na poziomie całej próby. Nie raportuj ogólnej skuteczności z kilku przykładów. Progi 0.90, 0.363 i 0.05 są punktami startowymi, a nie walidacją dla Twojej kamery.

Opcje strojenia: `--live-threshold`, `--identity-threshold`, `--margin`, `--min-face`. Nie obniżaj progów tylko dlatego, że zdjęcie na ekranie przechodzi test. Jeśli ataki przechodzą, oceniaj inny model, zestaw modeli lub kamerę z głębią/IR.

Testy automatyczne logiki uruchomisz poleceniem:

```powershell
.\.venv\Scripts\python.exe -m unittest -v test_stability.py
```
