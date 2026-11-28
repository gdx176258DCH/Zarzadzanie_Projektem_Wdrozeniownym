# Karta projektu

**Projekt:** Liczenie osób w jednej strefie  
**Data:** 28 listopada 2026  
**Opiekun z firmy:** mgr inż. Szymon Guzik  
**Wykonawca:** zespół projektowy: Dominik, Daria, Ania, Arek, Mateusz  
**Urządzenie odbioru:** NVIDIA Jetson Nano z kamerą  
**Urządzenie testowe:** telefon komórkowy z kamerą i API wyniku

**Problem.** Klient potrzebuje bieżącej liczby osób w jednej strefie. Obraz pozostaje przy kamerze; na zewnątrz trafia wyłącznie wynik.

**Cel.** Co najmniej 90% wykrytych osób i co najmniej 10 klatek na sekundę na Jetson Nano, dla detektora klasycznego i dla sieci neuronowej. Miary: czułość, precyzja, błąd liczenia, czas klatki. Próg wymaga akceptacji klienta.

| W zakresie | Poza zakresem |
| --- | --- |
| Jedna kamera, jedna strefa, Jetson Nano | Tożsamość, baza twarzy, emocje |
| Dwa rozwiązania, jeden zbiór klatek | Obraz w chmurze, wiele kamer |
| Protokół, 50 oznaczonych klatek, pomiar na urządzeniu | Trenowanie od zera, zakup sprzętu |
| Wynik bez obrazu, raport, prezentacja | Inne scenariusze |

| Ryzyko | Działanie |
| --- | --- |
| Sieć poniżej 10 klatek na sekundę | Optymalizacja na Jetson Nano |
| Brak zgody na nagranie | Publiczny zbiór z licencją |
| Różne dane dla obu rozwiązań | Jeden zbiór i jeden protokół |
| Zapis wizerunku lub cech twarzy | Poza zakresem projektu |

| Etap | Termin | Rezultat |
| --- | --- | --- |
| Start | 7.11.2026 | Temat i zespół |
| Karta projektu | 25.11.2026 | Zakres i kryteria |
| Prototyp detektora | 28.11.2026 | Rozwiązanie A, pierwsza tabela |
| Dane i protokół | 29.11–12.12.2026 | 50 klatek, pomiar A |
| Sieć na Jetson Nano | 13.12.2026 | Rozwiązanie B, druga tabela |
| Odbiór | 23.01.2027 | Raport, prezentacja, wybór rozwiązania |
