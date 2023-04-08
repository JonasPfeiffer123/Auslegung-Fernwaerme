# Auslegung-Fernwaerme

Ziel des Projektes ist die automatisierte Versorgungskonzept-Erstellung für Wärmenetze anhand verschiedener Input-Parameter.

Für den Einstieg empfielt sich zunächst die Datei "GUI.py" auszuführen, welche auf die anderen zugreift. Dort ist die Eingabe von Parametern am einfachsten. 
Ansonsten ist zur Auslegung die Datei "Berechnung_Fernwaerme.py" zuständig. Diese führt Ihre Berechnung auf Basis der Dateien "Berechnung_Erzeuger.py", "Berechnung_Solarthermie.py" und "Wirtschaftlichkeitsbetrachtungen.py" durch. In der Datei "Berechnung_Solarthermie.py" kann die Solarthermieanlage auch einzeln betrachtet werden

Die Datei "Daten.csv" beinhaltet einen Beispieldatensatz für Wetterdaten und Wärmelastgang und Temperaturdaten für Vor- und Rücklauf.
Die Datei "COP.csv" beinhaltet ein COP-Kennfeld, welches zur Berechnung der Wärmepumpen genutzt wird. Innerhalb des Kennfeldes wird Interpoliert. Das Kennfeld stammt aus einem Produktblatt von Viessmann für deren Hochtemperatur-Großwärmepumpe "Vitocal 350-HT Pro"

Notwendige Bibliotheken:
- matplotlib
- scipy
- numpy
- math
- csv
- tkinter

Die Erzeugerauslegung funktioniert nach Einschätzung des Verfassers

Aktuelle ToDos:
- Wirtschaftlichkeitsberechnungen optimieren und erweitern (derzeitig ohne Förderung, Kapitalzins, Preissteigerung)
  Weiterhin muss das "Bepreisungssystem" für Strom aus BHKW und in WP angepasst werden. Aktuell wird ein Strompreis definiert, zu dem das BHKW den gesamten Strom "verkaufen"     kann. Dadurch werden beim BHKW verhältnismäßig niedrige Wärmegestehungskosten erreicht. Der gleiche Strompreis wird für den Verbrauch durch die Wärmepumpen angesetzt. Hier     wird noch Literaturrecherche nötig sein.
- Erweiterung Funktionalität Solarthermieberechnung auf Umfang Excel-Tool
- weitere Erzeugertechnologien implementieren
- Optimierung Zusammenspiel Erzeuger
- Überarbeitung der Struktur (gegebenenfalls Funktionen/Codeabschnitte auslagern, insgesamt Optimierung)
