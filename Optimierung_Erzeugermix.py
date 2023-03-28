import matplotlib.pyplot as plt

from Berechnung_Fernwaerme import Berechnung_Erzeugermix

def Optimierung_Erzeugermix_BHKW():
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

# Optimierung_Erzeugermix_BHKW()

def Optimierung_Erzeugermix_STA():
    tech_order = ["Solarthermie", "Geothermie", "Holzgas-BHKW", "Biomassekessel", "Gaskessel"]
    WGK_ges = []
    DA_ges = []
    flächen = range(300, 900, 100)
    volumen = range(5, 40, 5)
    typ = "Flachkollektor"
    for f in flächen:
        WGK = []
        DA = []
        for v in volumen:
            ergebnis_WGK, ergebnis_DA = Berechnung_Erzeugermix(f, v, typ, 2000, 200, 0.5, 100, 200, 70, "Daten.csv", tech_order)
            WGK.append(ergebnis_WGK)
            WGK_ges.append(ergebnis_WGK)
            DA.append(ergebnis_DA)
            DA_ges.append(ergebnis_DA)
        labelf = str(f) + " m² " + "Flachkollektor" + "en"
        #plt.plot(volumen, WGK, linewidth=1, label=labelf)
        plt.plot(volumen, DA, linewidth=1, label=labelf)
        print("Kollektorfläche: " + str(f) + " m²; Minimale Wärmegestehungskosten: " + str(round(min(WGK), 2)) + " €/MWh")

    print("Minimale Wärmegestehungskosten: " + str(round(min(WGK_ges), 2)) + " €/MWh")


    plt.title("Wärmegestehungskosten nach Solarthermieauslegung")
    plt.xlabel("Speichergröße in m³")
    plt.ylabel("Wärmegestehungskosten gesamt, Deckungsanteil")
    plt.legend(loc='upper center')
    plt.show()

Optimierung_Erzeugermix_STA()