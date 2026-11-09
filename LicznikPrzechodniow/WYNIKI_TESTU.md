# Wynik testu — 2026-11-09

Film lokalny: dane/przechodnie.mp4, 602 klatki, 1280×720, około 25.1 s, 23.976 FPS. Liczba referencyjna około 27 pochodzi z szacunku użytkownika, nie z oznaczonych trajektorii.

- Poprzedni HOG 640 px: 19 (zapis użytkownika wyniki/test.csv).
- Eksperymentalny HOG 960 px, NMS 0.60, trzy kolejne potwierdzenia: 38. Nie ustawiono go jako domyślnego.
- YOLOv8n + tracker, ustawienia domyślne nowej wersji: 31, wszystkie 602 klatki.

Dla orientacyjnego odniesienia 27: błąd bezwzględny zmniejszył się z 8 do 4 osób. Zgodność sumy nie mierzy poprawności trajektorii, precyzji ani czułości. Wynik 31 nadal wskazuje nadliczanie lub niedokładność ręcznego odniesienia i wymaga sprawdzenia ID na filmie. Nie dopasowywano progów do uzyskania dokładnie 27.

Średni czas samej detekcji YOLO po pominięciu 10 klatek rozgrzewki: 204.3 ms; mediana 180.2 ms, w środowisku testowym agenta na tym komputerze. To nie jest pomiar urządzenia docelowego ani gwarancja FPS. OpenCV 4.14.0. Szczegóły: wyniki/yolo_weryfikacja.csv.

Dziewięć testów automatycznych logiki przeszło. Nie zweryfikowano jeszcze skuteczności na innych nagraniach ani urządzeniu brzegowym. Dalszy krok: ręcznie oznaczyć trajektorie i sprawdzić tracker przy zasłonięciach; rozważyć globalne przypisanie, ByteTrack/BoT-SORT lub cechy wyglądu.
