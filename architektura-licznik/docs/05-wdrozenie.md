## Rozmieszczenie w strefie klienta

Aplikacja licznika, wagi sieci i pliki pomiarów działają na NVIDIA Jetson Nano. Kamera jest podłączona bezpośrednio do urządzenia. System odbiorcy działa w infrastrukturze klienta.

![Rozmieszczenie licznika w strefie klienta](embed:LP-Wdrozenie)

Odbiór wydajności odbywa się na Jetson Nano. Dziś rozwiązanie B działa przez OpenCV DNN na procesorze. Docelowo sieć ma korzystać z procesora graficznego po dopasowaniu przez TensorRT i kwantyzację int8. Pomiar na laptopie lub telefonie jest pomocniczy i jest opisany nazwą sprzętu. Widok telefonu jako drugiego urządzenia testowego jest w osobnej sekcji.

Wysyłka wyniku do systemu odbiorcy jest planowana. Dopóki jej nie ma, wyniki zapisują się lokalnie. Po uruchomieniu wysyłki liczenie ma trwać także przy przerwie łącza; sposób ponowienia ustala się razem z formatem komunikatu.
