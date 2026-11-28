# Przegląd modelu Structurizr — Licznik osób

**Data:** 28 listopada 2026  
**Procedura:** skill `work/.agents/skills/modeluj-w-structurizr`, odbiór przeglądu z `work/operations/structurizr/zrodla-modelu.md`  
**Recenzent:** subagent generalPurpose  
**Autor modelu:** sesja agenta w katalogu przedmiotu

## Werdykt

Model jest gotowy do prezentacji prowadzącemu.

Pierwszy przegląd: gotowy po poprawkach. Po poprawkach i drugim sprawdzeniu tych samych miejsc: gotowy.

## Sprawdzenia narzędziowe

| Sprawdzenie | Wynik |
|---|---|
| `check-workspace` z oczekiwanymi widokami, ADR, dokumentacją i kierunkami relacji | passed |
| `check-workspace --preview http://127.0.0.1:8091/workspace/1` | passed |
| Inspections | 0 błędów, 0 ostrzeżeń, 204 kontrole |
| Structurizr | 2026.10.26 |

## Źródła porównane w przeglądzie

- kod: `LicznikPrzechodniow/main.py`, README aplikacji i README repozytorium;
- materiały: `materialy-dla-klienta/`, `materialy-do-oddania/`;
- pamięć przedmiotu: `ustalenia.md`, `brief.md`.

## Blokujące (usunięte)

1. Opis YOLO oraz relacja do GPU sugerowały działający TensorRT; w kodzie jest OpenCV DNN. Poprawione: stan obecny vs docelowy, tag `Planned`.
2. `docs/05-wdrozenie.md` mówił o GPU jak o fakcie. Poprawione: dziś DNN, TensorRT/int8 jako cel; HTTP jako planowane.

## Ostrzeżenia (pozostawione świadomie lub poprawione)

| Uwaga | Stan |
|---|---|
| Szerokości 1024/640/320 to protokół, nie jedyne możliwe | poprawione w modelu i docs |
| Wyjście wyniku bez słowa „planowane” w tabeli | poprawione |
| ADR LP-0001 i LP-0003: Decision vs Context | poprawione |
| Sekcje ADR 3.1/3.2 | świadomie pominięte; szablon assets ich nie wymaga |
| „Osoby w kadrze” vs „suma śladów” | otwarte; wymaga decyzji |
| Lokalny podgląd `imshow` w kodzie | poza produktem dla operatora; OK |

## Potwierdzone mocne strony

- HTTP i system odbiorcy oznaczone jako Planned.
- ADR mają status Proposed, nie Accepted.
- Przebieg LP-Klatka zgadza się z `main.py` dla rozwiązania A.
- Granice: tożsamość poza zakresem, obraz nie wychodzi, Jetson Nano, dwa rozwiązania / jeden protokół.
- Emby i dokumentacja bez znaczników historii, evidence i śladów AI.

## Pytania do decyzji

1. Czy Jetson Nano zamyka odbiór wydajności, a telefon zostaje drugim urządzeniem testowym?
2. Czy próg 90% wykrytych osób i 10 klatek na sekundę obowiązuje, i w jakich warunkach sceny?
3. Jaka liczba wychodzi do systemu odbiorcy: osoby w kadrze, suma potwierdzonych śladów, czy obie — oraz format, częstotliwość i adres?
4. Czy wynik może zawierać położenie osób, czy wyłącznie liczbę, czas i nazwę rozwiązania?
5. Skąd klatki testowe (publiczny zbiór vs nagranie za zgodą) i kto zatwierdza protokół?
6. Czy klient przyjmuje ADR LP-0001–LP-0005 jako decyzje zakresu, czy zostają propozycją zespołu?
7. Kto ma którą z pięciu ról w zespole?
