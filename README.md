# Auslegung-Fernwaerme
# Autor: Jonas Pfeiffer (Student Energie- und Umwelttechnik Hochschule Zittau/Görlitz)

Ziel des Projektes ist die automatisierte Versorgungskonzept-Erstellung für Wärmenetze anhand verschiedener Input-Parameter.

Für den Einstieg empfielt sich zunächst die Datei "GUI.py" auszuführen, welche auf die anderen zugreift. Dort ist die Eingabe von Parametern am einfachsten. 
Ansonsten ist zur Auslegung die Datei "Berechnung_Fernwaerme.py" zuständig. Diese führt Ihre Berechnung auf Basis der Dateien "Berechnung_Erzeuger.py", "Berechnung_Solarthermie.py" und "Wirtschaftlichkeitsbetrachtungen.py" durch. In der Datei "Berechnung_Solarthermie.py" kann die Solarthermieanlage auch einzeln betrachtet werden

Die Datei "Daten.csv" beinhaltet einen Beispieldatensatz für Wetterdaten und Wärmelastgang und Temperaturdaten für Vor- und Rücklauf.
Die Datei "Kennlinien WP.csv" beinhaltet ein COP-Kennfeld, welches zur Berechnung der Wärmepumpen genutzt wird. Innerhalb des Kennfeldes wird Interpoliert. Das Kennfeld stammt aus einem Produktblatt von Viessmann für deren Hochtemperatur-Großwärmepumpe "Vitocal 350-HT Pro"

Im Bild "GUI Ausschnitt 1.png" sind beispielhafte Eingabedaten und die Ergebnisse dargestellt.
Im "GUI Ausschnitt 2.png" folgt die Darstellung der Diagramme

Notwendige Bibliotheken sind:
- matplotlib
- scipy
- numpy
- math
- csv
- tkinter

Die Erzeugerauslegung funktioniert nach Einschätzung des Autor.

Kurzbeschreibungen zu den einzelnen Python-Dateien:
"Berechnung_Fernwaerme.py":
  - Hauptfunktion
  - verarbeitet die Inputdaten
  - setzt die Wärmeerzeuger der Reihenfolge nach zusammen
  - gibt den Erzeugermix mit allen relevanten Informationen wieder

"Berechnung_Solarthermie.py":
  - liest die CSV mit den Daten ein
  - Daten enthalten Wetterdaten des Standortes sowie Zeitreihe zum Wärmenetz
  - Berechnung der Solarstrahlung und der Solarthermie-Erzeugung nach Scenocalc Fernwärme 2.0 (Excel-Tool, www.scfw.de)
  - Optimierungsfunktion, welche nach Wärmegestehungskosten optimiert (funktioniert aktuell nicht, da es an anderer Stelle zuletzt signifikante Änderungen gab)
  
 "Berechnung_Erzeuger.py":
  - Berechnung PV
  - Berechnung Wärmepumpe
  - Berechnung Wärmequellen Wärmepumpe (aktuell Abwärme, Abwasserwärme, Geothermie)
  - Berechnung BHKW
  - Berechnung Gaskessel
  - Berechnung Biomassekessel
 
 "Wirtschaftlichkeitsbetrachtung.py":
 - Berechnung der Wärmegestehungskosten für die einzelnen Erzeugertechnologien nach Annuitätsmethode gemäß VDI 2067-1
 
 "GUI.py":
  - grafische Oberfläche zur Eingabe aller Parameter
  - Ausgabe von Diagrammen und Ergebnissen

Aktuelle ToDos für die Auslegung:
  - Wirtschaftlichkeitsberechnungen um BEW bzw. andere Fördermöglichkeiten erweitern (BEW in GUI implementiert aber noch nicht umgesetzt)
  - Weiterhin muss das "Bepreisungssystem" für Strom aus BHKW und in WP angepasst werden. Aktuell wird ein Strompreis definiert, zu dem das BHKW den gesamten Strom "verkaufen"     kann. Dadurch werden beim BHKW verhältnismäßig niedrige Wärmegestehungskosten erreicht. Der gleiche Strompreis wird für den Verbrauch durch die Wärmepumpen angesetzt. Hier     wird noch Literaturrecherche nötig sein.
  - Erweiterung Funktionalität Solarthermieberechnung auf Umfang Excel-Tool
  - weitere Erzeugertechnologien implementieren (Luftwärmepumpe (technologisch begrenzt), Elektrodenkessel, wasserstoffbasierte Lösungen auch denkbar, auch wenn diese primär       in der Wärmeversorgung keine Rolle spielen sollten (Kessel, BHKW, Elektrolyseur, Brennstoffzelle)
  - Optimierung Zusammenspiel Erzeuger
  - Überarbeitung der Struktur (gegebenenfalls Funktionen/Codeabschnitte auslagern, insgesamt Optimierung)
  
 Weitere Ideen:
  - Aktuell wird mit bekanntem/gesetztem Lastgang sowie vorgegebenen Vor- und Rücklauftemperaturen gearbeitet
    -> Erstrebenswert wäre Lastganggenerierung durch Standardlastprofile (BDEW, TUM) oder Volllaststunden oder ähnlichem
  - nach erfolgter Auslegung (u.a. Wahl tatsächlicher Anlagendimensionen) muss Betrieb simuliert werden
    -> Zusammenspiel mit Speicher, Implementation von Regelung, An- und Abfahrprozesse beachten
  - in weiteren Schritten müsste dann die Netzsimulation mit implementiert werden
    -> dabei wird das einlesen von GIS-Daten ein Thema
    -> Regelung und Hydraulik soll dann auf mehrere Erzeugerstandorte ausgeweitet werden können
