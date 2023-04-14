import numpy as np
import matplotlib.pyplot as plt

def Betriebsoptimierung(Last, Zeitschritte, Daten_Erzeuger, Daten_Speicher):
    QSmax = 1.16 * Daten_Speicher["Volumen"] * (Daten_Speicher["VLT"] - Daten_Speicher["RLT"])
    QS = QSmax * Daten_Speicher["Füllstand"]/100

    print(f"{QSmax:.2f} kWh")
    print(f"{QS:.2f} kWh")

    t = 1/6  # h

    BHKW_oS = []
    for l in Last:
        if Daten_Erzeuger["BHKW"]["Betrieb"] == 1:
            if Daten_Erzeuger["BHKW"]["Nennleistung"] > l and Daten_Erzeuger["BHKW"]["Nennleistung"] * \
                    Daten_Erzeuger["BHKW"]["Teillast"] <= l:
                BHKW_oS.append(l)
            elif Daten_Erzeuger["BHKW"]["Nennleistung"] * Daten_Erzeuger["BHKW"]["Teillast"] > l:
                Daten_Erzeuger["BHKW"]["Betrieb"] = 0
                BHKW_oS.append(0)
            elif Daten_Erzeuger["BHKW"]["Nennleistung"] <= l:
                BHKW_oS.append(Daten_Erzeuger["BHKW"]["Nennleistung"])

        elif Daten_Erzeuger["BHKW"]["Betrieb"] == 0:
            if l >= Daten_Erzeuger["BHKW"]["Nennleistung"]:
                Daten_Erzeuger["BHKW"]["Betrieb"] = 1
                BHKW_oS.append(Daten_Erzeuger["BHKW"]["Nennleistung"])
            else:
                BHKW_oS.append(0)


    plt.plot(Zeitschritte, Last)
    plt.plot(Zeitschritte, BHKW_oS)
    plt.show()



Sollleistung = [150, 200, 240, 300, 500, 600, 700, 900, 1800, 1500, 600, 200]
Zeitschritte = range(12)  # 10 min Schritte
Erzeuger = {'BHKW': {'Nennleistung': 230, 'Teillast': 0.8, 'Betrieb': 1},
            'Pelletkessel': {'Nennleistung': 500, 'Teillast': 0.6, 'Betrieb': 0},
            'Gaskessel': {'Nennleistung': 900, 'Teillast': 0.3, 'Betrieb': 0}}

Speicher = {'Volumen': 20,      # in m³
            'RLT': 60,          # in °C
            'VLT': 90,          # in °C
            'Füllstand': 10}    # in %

Betriebsoptimierung(Sollleistung, Zeitschritte, Erzeuger, Speicher)
