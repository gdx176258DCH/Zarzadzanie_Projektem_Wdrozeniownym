workspace "Licznik osób" "Liczenie osób w jednej strefie na urządzeniu przy kamerze. Dwa rozwiązania porównane jednym protokołem." {
    !impliedRelationships false

    model {
        operator = person "Operator strefy" "Potrzebuje bieżącej liczby osób w strefie. Nie ogląda nagrania."
        zespol = person "Zespół projektowy" "Uruchamia pomiary, oznacza klatki i porównuje oba rozwiązania."

        odbiorca = softwareSystem "System odbiorcy wyniku" "Serwer lub panel klienta, który przyjmuje liczbę osób. Adres i format wskazuje klient." "External,Planned"

        licznik = softwareSystem "Licznik osób" "Liczy osoby w jednej strefie przy kamerze. Na zewnątrz przekazuje liczbę, czas i nazwę rozwiązania, bez obrazu." {
            !docs docs
            !adrs decisions

            kamera = container "Kamera" "Rejestruje obraz strefy. Obraz nie opuszcza urządzenia." "Kamera USB lub CSI" "Device"

            aplikacja = container "Aplikacja licznika" "Wykrywa osoby na klatce, śledzi je przez kilka sekund i liczy potwierdzone sylwetki." "Python, OpenCV" "App" {
                url "{workspace}/decisions/Licznik%20os%C3%B3b#2"

                odczyt = component "Odczyt obrazu" "Pobiera klatki z kamery albo z pliku wideo." "OpenCV VideoCapture" "Component"
                skalowanie = component "Skalowanie" "Zmniejsza klatkę do szerokości z parametru. W protokole pomiarów: 1024, 640 i 320 pikseli." "OpenCV" "Component"
                hog = component "Rozwiązanie A: detektor HOG + SVM" "Klasyczny detektor sylwetek. Działa bez karty graficznej i bez trenowania." "OpenCV HOGDescriptor" "Component"
                yolo = component "Rozwiązanie B: sieć YOLOv8n" "Sieć neuronowa wykrywająca osoby przez OpenCV DNN i ONNX. Docelowo na Jetson Nano przez TensorRT i int8." "OpenCV DNN, ONNX" "Component"
                sledzenie = component "Śledzenie" "Łączy wykrycia z kolejnych klatek w krótkie ślady. Liczy ślad raz, po potwierdzeniu. Numer śladu żyje najwyżej 3 s po zniknięciu osoby." "Python" "Component"
                rejestr = component "Rejestr pomiarów" "Zapisuje dla każdej klatki liczbę wykryć, czasy przetwarzania i ustawienia." "CSV" "Component"
                wyjscie = component "Wyjście wyniku" "Przekazuje liczbę osób, czas i nazwę rozwiązania do systemu odbiorcy." "HTTP" "Component,Planned"
            }

            modelSieci = container "Plik modelu sieci" "Wagi YOLOv8n w formacie ONNX. Nie są częścią repozytorium." "ONNX" "File"
            pomiary = container "Pliki pomiarów" "Wyniki pomiarów w CSV: jeden plik na rozwiązanie i rozdzielczość." "CSV" "File"
        }

        zespol -> licznik "Uruchamia pomiary i odczytuje wyniki." "Wiersz poleceń"
        licznik -> odbiorca "Przekazuje liczbę osób, czas i nazwę rozwiązania." "HTTP" "Planned"
        operator -> odbiorca "Odczytuje liczbę osób w strefie." "Panel" "Planned"

        zespol -> aplikacja "Uruchamia pomiar z wybranym rozwiązaniem i rozdzielczością." "Wiersz poleceń"
        aplikacja -> kamera "Odczytuje klatki." "USB lub CSI"
        aplikacja -> modelSieci "Wczytuje wagi sieci." "Plik"
        aplikacja -> pomiary "Zapisuje wyniki pomiaru." "Plik CSV"
        zespol -> pomiary "Odczytuje wyniki i porównuje rozwiązania." "Arkusz"
        aplikacja -> odbiorca "Przekazuje liczbę osób, czas i nazwę rozwiązania." "HTTP" "Planned"

        zespol -> odczyt "Wskazuje źródło obrazu." "Wiersz poleceń"
        odczyt -> kamera "Odczytuje klatki." "USB lub CSI"
        odczyt -> skalowanie "Przekazuje klatkę." "Wywołanie w aplikacji"
        skalowanie -> hog "Przekazuje klatkę, gdy wybrano rozwiązanie A." "Wywołanie w aplikacji"
        skalowanie -> yolo "Przekazuje klatkę, gdy wybrano rozwiązanie B." "Wywołanie w aplikacji"
        yolo -> modelSieci "Wczytuje wagi sieci." "Plik"
        hog -> sledzenie "Przekazuje ramki osób." "Wywołanie w aplikacji"
        yolo -> sledzenie "Przekazuje ramki osób." "Wywołanie w aplikacji"
        sledzenie -> rejestr "Przekazuje liczbę wykryć i sumę potwierdzonych osób." "Wywołanie w aplikacji"
        rejestr -> pomiary "Dopisuje wiersz pomiaru." "Plik CSV"
        sledzenie -> wyjscie "Przekazuje bieżącą liczbę osób." "Wywołanie w aplikacji" "Planned"
        wyjscie -> odbiorca "Wysyła liczbę osób, czas i nazwę rozwiązania." "HTTP" "Planned"

        strefa = deploymentEnvironment "Strefa klienta" {
            deploymentNode "Kamera w strefie" "Kamera podłączona bezpośrednio do Jetson Nano." "USB lub CSI" {
                kameraInst = containerInstance kamera
            }
            deploymentNode "Jetson Nano" "Urządzenie przy kamerze. Na nim odbywa się odbiór wydajności." "NVIDIA Jetson Nano, JetPack" {
                deploymentNode "Środowisko Python" "Wirtualne środowisko z OpenCV." "Python 3" {
                    aplikacjaInst = containerInstance aplikacja
                    modelInst = containerInstance modelSieci
                    pomiaryInst = containerInstance pomiary
                }
                gpu = infrastructureNode "Procesor graficzny" "Przyspiesza sieć po dopasowaniu przez TensorRT." "NVIDIA Maxwell, TensorRT"
                aplikacjaInst -> gpu "Docelowo uruchamia sieć na procesorze graficznym." "TensorRT" "Planned"
            }
            deploymentNode "Infrastruktura klienta" "Serwer lub panel wskazany przez klienta." "Do ustalenia z klientem" {
                odbiorcaInst = softwareSystemInstance odbiorca
            }
        }

        telefonTesty = deploymentEnvironment "Testy na telefonie" {
            telefonGrupa = deploymentGroup "Telefon"
            deploymentNode "Telefon komórkowy" "Drugie urządzenie testowe. Kamera wbudowana. Wynik wydajności z telefonu nie zastępuje odbioru na Jetson Nano." "Android lub iOS" {
                kameraTelefon = infrastructureNode "Kamera telefonu" "Wbudowana kamera telefonu. Obraz nie opuszcza urządzenia." "Kamera"
                deploymentNode "Aplikacja na telefonie" "Uruchomienie licznika albo klienta API na telefonie." "Do wyboru z zespołem" {
                    aplikacjaTel = containerInstance aplikacja telefonGrupa
                    modelTel = containerInstance modelSieci telefonGrupa
                    pomiaryTel = containerInstance pomiary telefonGrupa
                }
                aplikacjaTel -> kameraTelefon "Odczytuje klatki." "API kamery"
            }
            deploymentNode "Infrastruktura klienta" "Serwer lub panel wskazany przez klienta." "Do ustalenia z klientem" {
                odbiorcaTel = softwareSystemInstance odbiorca telefonGrupa
            }
        }
    }

    views {
        systemContext licznik "LP-Kontekst" "Kto korzysta z licznika i dokąd trafia wynik." {
            include * operator
            autoLayout lr
            default
        }

        container licznik "LP-Kontenery" "Kamera, aplikacja licznika i pliki, z których korzysta." {
            include *
            autoLayout lr
        }

        component aplikacja "LP-Aplikacja" "Odpowiedzialności aplikacji: od odczytu klatki do wyniku i pomiaru." {
            include *
            autoLayout lr
        }

        dynamic aplikacja "LP-Klatka" "Przetworzenie jednej klatki rozwiązaniem A: od odczytu do zapisu pomiaru." {
            odczyt -> kamera "Odczytuje klatkę."
            odczyt -> skalowanie "Przekazuje klatkę."
            skalowanie -> hog "Przekazuje klatkę w wybranej szerokości."
            hog -> sledzenie "Przekazuje ramki osób."
            sledzenie -> rejestr "Przekazuje liczbę wykryć i sumę potwierdzonych osób."
            rejestr -> pomiary "Dopisuje wiersz pomiaru."
            autoLayout lr
        }

        deployment licznik strefa "LP-Wdrozenie" "Rozmieszczenie odbioru: Jetson Nano, kamera i system odbiorcy." {
            include *
            autoLayout tb
        }

        deployment licznik telefonTesty "LP-Telefon" "Drugie urządzenie testowe: telefon z kamerą i API wyniku. Nie zastępuje odbioru na Jetson Nano." {
            include *
            autoLayout tb
        }

        styles {
            element "Element" {
                background #e8edf5
                color #182536
            }
            element "Person" {
                shape Person
                background #334155
                color #ffffff
            }
            element "Software System" {
                background #234552
                color #ffffff
            }
            element "External" {
                background #eceff3
                color #273849
            }
            element "Device" {
                shape Box
                background #f3e8d4
                color #2b2112
            }
            element "App" {
                background #c9e8f5
                color #17211f
            }
            element "File" {
                shape Folder
                background #e5eee4
                color #17211f
            }
            element "Planned" {
                border dashed
            }
            relationship "Relationship" {
                color #526174
                thickness 2
                style solid
            }
            relationship "Planned" {
                style dashed
            }
        }
    }

    configuration {
        scope softwaresystem
    }
}
