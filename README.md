# Auslegung-Fernwaerme

Ziel des Projektes ist die automatisierte Versorgungskonzept-Erstellung für Wärmenetze anhand verschiedener Input-Parameter.

Für den Einstieg empfielt sich zunächst die Datei "GUI.py" auszuführen, welche auf die anderen zugreift. Dort ist die Eingabe von Parametern am einfachsten. 
Ansonsten ist zur Auslegung die Datei "Berechnung_Fernwaerme.py" zuständig. 
In der Datei "Berechnung_Solarthermie.py" kann die Solarthermieanlage einzeln betrachtet werden

Notwendige Bibliotheken:
- matplotlib
- scipy
- numpy
- math
- csv
- customtkinter
- tkinter

Aktuelle ToDos:
- Erweiterung Funktionalität Solarthermieberechnung auf Umfang Excel-Tool
- weitere Erzeugertechnologien implementieren
- Wirtschaftlichkeitsberechnungen optimieren und erweitern (derzeitig ohne Förderung, Kapitalzins, Preissteigerung)
- Optimierung Zusammenspiel Erzeuger
- Überarbeitung der Struktur (gegebenenfalls Funktionen/Codeabschnitte auslagern, insgesamt Optimierung)
