import matplotlib.pyplot as plt

from Berechnung_Fernwaerme import Berechnung_Erzeugermix

def Optimierung_Erzeugermix():
    tech_order = ["Solarthermie", "Geothermie", "Holzgas-BHKW", "Biomassekessel", "Gaskessel"]
    WGK = []
    el_Leistung_BHKW = range(10, 200, 10)
    for i in range(10, 200, 10):
        WGK.append(Berechnung_Erzeugermix(600, 20, "Flachkollektor", 2000, 200, 0.5, 100, 200, 70, "Daten.csv", tech_order, i))

    plt.plot(el_Leistung_BHKW, WGK, color="blue", linewidth=1, label="Wärmegestehungskosten")

    plt.title("Wärmegestehungskosten nach BHKW-Größe")
    plt.xlabel("elektrische Leistung BHKW")
    plt.ylabel("Wärmegestehungskosten gesamt")
    plt.legend(loc='upper center')
    plt.show()

Optimierung_Erzeugermix()