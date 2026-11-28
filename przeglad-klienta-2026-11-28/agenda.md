# Przegląd z klientem — 28 listopada 2026

**Dla:** mgr inż. Szymon Guzik  
**Od:** zespół projektowy (Dominik, Daria, Ania, Arek, Mateusz)  
**Czas:** 11:20–14:25, sala C314  
**Projekt:** Liczenie osób w jednej strefie

## Cel spotkania

Uzgodnić zakres, sprzęt, protokół pomiarów i plan dalszych prac. Po spotkaniu w dokumentach zostaje tylko to, co klient przyjmie.

## Proponowany przebieg

1. **Potrzeba i zakres** — brief i karta projektu. Jedna kamera, jedna strefa, wynik bez obrazu. Poza zakresem: tożsamość, baza twarzy, emocje.
2. **Dwa rozwiązania** — oferta. Detektor klasyczny HOG + SVM oraz sieć YOLOv8n. Ten sam protokół i te same klatki.
3. **Sprzęt** — Jetson Nano z kamerą do odbioru wydajności. Telefon z kamerą i API jako drugie urządzenie testowe.
4. **Architektura** — kontekst systemu, rozmieszczenie na Nano i widok telefonu.
5. **Protokół pomiarów** — szkic do uzgodnienia. Tabele wyników są jeszcze puste; film testowy jest przygotowany, klatki czekają na oznaczenie.
6. **Plan etapu 3** — sieć na Jetson Nano, optymalizacja, pomiar na telefonie, raport i odbiór.
7. **Decyzje** — lista w osobnym dokumencie.

## Dokumenty w tej paczce

| Plik | Do czego |
|---|---|
| `brief.docx` | potrzeba klienta i pytania |
| `proposal.docx` | zakres, harmonogram, ryzyka |
| `karta-projektu.docx` | jednostronicowa karta |
| `ZPW-01-karta-i-zespol.docx` | karta z zespołem |
| `ZPW-02-protokol-pomiarow.docx` | szkic protokołu |
| `ZPW-03-plan-etapu-3-i-ryzyka.docx` | plan i ryzyka |
| `decyzje-na-spotkanie.docx` | lista decyzji do podjęcia |
| `diagramy/` | trzy diagramy architektury |

Podgląd architektury na żywo: http://127.0.0.1:8091/workspace/1

## Stan prac

| Element | Stan |
|---|---|
| Kod licznika w repozytorium | gotowy (HOG i YOLO) |
| Film testowy | gotowy (licencja CC BY-SA) |
| 50 oznaczonych klatek | brak |
| Tabela pomiarów A i B | brak — do wypełnienia po oznaczeniu klatek |
| Pomiar na Jetson Nano | brak |
| Pomiar na telefonie | brak |
| Przydział pięciu ról | do ustalenia w zespole |
