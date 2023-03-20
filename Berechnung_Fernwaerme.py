# Berechnungsprogramm Fernwärme-Erzeugerauslegung

# Import Bibliotheken
from math import pi
import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import RegularGridInterpolator
from Berechnung_Solarthermie import Berechnung_STA, WGK_STA, Daten

def Berechnung_PV(Bruttofläche):
    data = np.loadtxt("Daten.csv", delimiter=",", skiprows=1).T
    h_L, G_L, Ta_L, W_L = data[0], data[3], data[4], data[5]

    P_L = []
    E = 0
    eff_nom = 0.199
    sys_loss = 0.14
    U0 = 26.9  # W / (°C * m^2)
    U1 = 6.2  # W * s / (°C * m^3
    k1, k2, k3, k4, k5, k6 = -0.017237, -0.040465, -0.004702, 0.000149, 0.000170, 0.000005

    for G, Ta, W in zip(G_L, Ta_L, W_L):
        if G == 0:
            P = 0
        else:
            Tm = Ta + G / (U0 + U1 * W)
            G1 = G / 1000
            T1m = Tm - 25
            eff_rel = 1 + k1 * np.log(G1) + k2 * np.log(G1) ** 2 + k3 * T1m + k4 * T1m * np.log(G1) + k5 * Tm * np.log(
                G1) ** 2 + k6 * Tm ** 2
            P = G1 * Bruttofläche * eff_nom * eff_rel * (1 - sys_loss)
        P_L.append(P)
        E += P

    print("Jährlicher PV-Ertrag: " + str(round(E, 2)) + " kWh")
    plt.plot(h_L, P_L)
    plt.show()
# Berechnung_PV(1000)

def COP_WP(VLT_L, QT):
    # Interpolationsformel für den COP
    values = np.genfromtxt('Kennlinien WP.csv', delimiter=';')
    row_header = values[0, 1:]  # Vorlauftempertauren
    col_header = values[1:, 0]  # Quelltemperaturen
    values = values[1:, 1:]
    f = RegularGridInterpolator((col_header, row_header), values, method='linear')
    # technische Grenze der Wärmepumpe ist Temperaturhub von 75 °C
    VLT_L = np.minimum(VLT_L, 75)
    QT_array = np.full_like(VLT_L, QT)

    COP_L = f(np.column_stack((QT_array, VLT_L))).flatten()
    return COP_L, VLT_L

def Berechnung_WP(Kühlleistung, QT, VLT_L):
    COP_L = COP_WP(VLT_L, QT)
    el_Leistung_L = []
    Wärmeleistung_L = []

    for COP in COP_L:
        Wärmeleistung = Kühlleistung / (1 - (1 / COP))
        Wärmeleistung_L.append(Wärmeleistung)

        el_Leistung = Wärmeleistung - Kühlleistung
        el_Leistung_L.append(el_Leistung)

    return Wärmeleistung_L, el_Leistung_L

def WGK_WP(Wärmeleistung, Wärmemenge, Strombedarf, Wärmequelle, spez_Investitionskosten_WQ, Strompreis):
    # Kosten Wärmepumpe: Viessmann Vitocal 350 HT-Pro: 140.000€, 350 kW Nennleistung; 120 kW bei 10/85
    # Annahme Kosten Wärmepumpe: 1000 €/kW; Vereinfachung
    spez_Investitionskosten_WP = 1000 #€/kW
    Nutzungsdauer_WP = 20

    Investitionskosten_WP = spez_Investitionskosten_WP * round(Wärmeleistung, 0)

    Anteil_Betriebskosten_WP = 0.02
    Betriebskosten_Jahr_WP = Investitionskosten_WP * Anteil_Betriebskosten_WP
    Betriebskosten_Gesamt_WP = Betriebskosten_Jahr_WP * Nutzungsdauer_WP

    # Strompreis = 200  # €/MWh
    Stromkosten_Jahr = round(Strombedarf, 0) * Strompreis
    Stromkosten_Gesamt = Stromkosten_Jahr * Nutzungsdauer_WP

    Gesamtkosten_WP = Investitionskosten_WP + Betriebskosten_Gesamt_WP + Stromkosten_Gesamt
    Gesamtwärmemenge_WP = Wärmemenge * Nutzungsdauer_WP

    WGK_WP = Gesamtkosten_WP / Gesamtwärmemenge_WP

    if Wärmequelle == "Abwärme":
        spez_Investitionskosten_WQ = 500
        Nutzungsdauer_WQ = 20
    elif Wärmequelle == "Abwasserwärme":
        spez_Investitionskosten_WQ = 1000
        Nutzungsdauer_WQ = 20
    elif Wärmequelle == "Geothermie":
        Nutzungsdauer_WQ = 30
    else:
        raise ValueError("Ungültige Art der Wärmequelle")

    Investitionskosten_WQ = spez_Investitionskosten_WQ * Wärmeleistung

    Anteil_Betriebskosten_WQ = 0.01
    Betriebskosten_Jahr_WQ = Investitionskosten_WQ * Anteil_Betriebskosten_WQ
    Betriebskosten_Gesamt_WQ = Betriebskosten_Jahr_WQ * Nutzungsdauer_WQ

    Gesamtkosten_WQ = Investitionskosten_WQ + Betriebskosten_Gesamt_WQ
    Gesamtwärmemenge_WQ = Wärmemenge * Nutzungsdauer_WQ

    WGK_WQ = Gesamtkosten_WQ / Gesamtwärmemenge_WQ

    WGK_Gesamt = WGK_WQ + WGK_WP

    return WGK_Gesamt

def aw(Last_L, VLT_L, Kühlleistung, Temperatur):
    if Kühlleistung == 0:
        return 0, 0, np.zeros_like(Last_L), np.zeros_like(VLT_L), 0

    Wärmeleistung_L, el_Leistung_L = Berechnung_WP(Kühlleistung, Temperatur, VLT_L)

    mask = Last_L >= Wärmeleistung_L
    Wärmemenge = np.sum(np.where(mask, Wärmeleistung_L / 1000, 0))
    Strombedarf = np.sum(np.where(mask, el_Leistung_L / 1000, 0))
    Betriebsstunden = np.sum(mask)

    max_Wärmeleistung = np.max(Wärmeleistung_L)

    return Wärmemenge, Strombedarf, Wärmeleistung_L, el_Leistung_L, max_Wärmeleistung, Betriebsstunden

def Geothermie(Last_L, VLT_L, Fläche, Bohrtiefe, Quelltemperatur):
    if Fläche == 0 or Bohrtiefe == 0:
        return 0, 0, np.zeros_like(Last_L), np.zeros_like(VLT_L), 0, 0

    Vollbenutzungsstunden = 2400  # h
    spez_Entzugsleistung = 50  # W/m bei 2400 h
    spez_Bohrkosten = 120  # €/m

    Abstand_Sonden = 6  # m
    Fläche_Sonde = (pi/4) * (2*Abstand_Sonden)**2
    Anzahl_Sonden = round(Fläche / Fläche_Sonde, 0)  # 22

    Entzugsleistung_2400 = Bohrtiefe * spez_Entzugsleistung * Anzahl_Sonden / 1000  # kW bei 2400 h, 22 Sonden, 50 W/m: 220 kW
    Entzugswärmemenge = Entzugsleistung_2400 * Vollbenutzungsstunden / 1000  # MWh
    Investitionskosten_Sonden = Bohrtiefe * spez_Bohrkosten * Anzahl_Sonden

    COP_L, VLT_WP = COP_WP(VLT_L, Quelltemperatur)

    # tatsächliche Anzahl der Betriebsstunden der Wärmepumpe hängt von der Wärmeleistung ab, diese hängt über Entzugsleistung
    # von der angenommenen Betriebsstundenzahl ab
    B_min = 1
    B_max = 8760
    tolerance = 0.5
    while B_max - B_min > tolerance:
        B = (B_min + B_max) / 2
        #Berechnen der Entzugsleistung
        Entzugsleistung = Entzugswärmemenge * 1000 / B  # kW
        # Berechnen der Wärmeleistung und elektrischen Leistung
        Wärmeleistung_L = Entzugsleistung / (1 - (1 / COP_L))
        el_Leistung_L = Wärmeleistung_L - Entzugsleistung

        # Bestimmen des Anteils, der tatsächlich genutzt wird
        Anteil = np.minimum(1, Last_L / Wärmeleistung_L)

        # Berechnen der tatsächlichen Werte
        Wärmeleistung_tat_L = Wärmeleistung_L * Anteil
        el_Leistung_tat_L = el_Leistung_L * Anteil
        Entzugsleistung_tat_L = Wärmeleistung_tat_L - el_Leistung_tat_L
        Entzugswärme = np.sum(Entzugsleistung_tat_L) / 1000
        Wärmemenge = np.sum(Wärmeleistung_tat_L) / 1000
        Strombedarf = np.sum(el_Leistung_tat_L) / 1000
        Betriebsstunden = np.count_nonzero(Wärmeleistung_tat_L)

        # Falls es keine Nutzung gibt, wird das Ergebnis 0
        if Betriebsstunden == 0:
            Wärmeleistung_tat_L = np.array([0])
            el_Leistung_tat_L = np.array([0])

        if Entzugswärme > Entzugswärmemenge:
            B_min = B
        else:
            B_max = B

    max_Wärmeleistung = max(Wärmeleistung_tat_L)
    JAZ = Wärmemenge / Strombedarf

    return Wärmemenge, Strombedarf, Wärmeleistung_tat_L, el_Leistung_tat_L, max_Wärmeleistung, Investitionskosten_Sonden

def WGK_Gaskessel(Last_L, P_ein, P_max, spez_Brennstoffkosten):
    Erzeugung_GK_L = np.maximum(Last_L - P_ein, 0)
    Wärmemenge_GK = np.sum(Erzeugung_GK_L) / 1000

    # Kosten 1000 kW Gaskessel ~ 30000 €
    Nutzungsdauer = 20
    spez_Investitionskosten = 30  # €/kW
    Investitionskosten = spez_Investitionskosten * P_max

    Anteil_Betriebskosten = 0.01
    Betriebskosten_Jahr = Investitionskosten * Anteil_Betriebskosten
    Betriebskosten_Gesamt = Betriebskosten_Jahr * Nutzungsdauer

    # spez_Brennstoffkosten = 100  # €/MWh
    Nutzungsgrad_GK = 0.9
    Brennstoffkosten_Jahr = spez_Brennstoffkosten * Wärmemenge_GK / Nutzungsgrad_GK
    Brennstoffkosten_Gesamt = Brennstoffkosten_Jahr * Nutzungsdauer

    Gesamtkosten_GK = Investitionskosten + Betriebskosten_Gesamt + Brennstoffkosten_Gesamt
    Wärmemenge_GK_Gesamt = Wärmemenge_GK * Nutzungsdauer

    if Wärmemenge_GK > 0:
        WGK_GK = Gesamtkosten_GK / Wärmemenge_GK_Gesamt
        return Wärmemenge_GK, WGK_GK, Erzeugung_GK_L

    else:
        return 0, 0, 0

def WGK_Biomassekessel(Leistung_BMK, Wärmemenge_BMK, spez_Brennstoffkosten):
    # Kosten 200 kW Holzpelletkessel ~ 40000 €
    for i in range(100, 1000, 100):
        if Leistung_BMK <= i:
            Leistung_BMK = i
    Nutzungsdauer = 15
    spez_Investitionskosten = 200  # €/kW
    spez_Investitionskosten_Holzlager = 400  # €/t
    Größe_Holzlager = 40  # t
    Investitionskosten = spez_Investitionskosten * Leistung_BMK + spez_Investitionskosten_Holzlager * Größe_Holzlager

    Anteil_Betriebskosten = 0.02
    Betriebskosten_Jahr = Investitionskosten * Anteil_Betriebskosten
    Betriebskosten_Gesamt = Betriebskosten_Jahr * Nutzungsdauer

    # Kosten Holzpellets 360 € / t = 0.36 € / kg; Heizwert Holzpellets = 4.8 MWh/t
    # Kosten Holzhackschnitzel 20 % Restfeuchte: 160 € / t = 0.16 € / kg; Heizwert Holzhackschnitzel = 3.4 kWh / kg
    # massespez_Brennstoffkosten = 160  # €/t
    # Heizwert_Holzpellets = 4.8 # MWh/t
    # spez_Brennstoffkosten = massespez_Brennstoffkosten / Heizwert_Holzpellets  # €/MWh 360/4.8=75
    Nutzungsgrad_BMK = 0.9
    Brennstoffkosten_Jahr = spez_Brennstoffkosten * Wärmemenge_BMK / Nutzungsgrad_BMK
    Brennstoffkosten_Gesamt = Brennstoffkosten_Jahr * Nutzungsdauer

    Gesamtkosten_BMK = Investitionskosten + Betriebskosten_Gesamt + Brennstoffkosten_Gesamt
    Wärmemenge_BMK_Gesamt = Wärmemenge_BMK * Nutzungsdauer

    if Wärmemenge_BMK > 0:
        WGK_BMK = Gesamtkosten_BMK / Wärmemenge_BMK_Gesamt
        return WGK_BMK

    else:
        return 0

def wgk_BHKW(Wärmeleistung_BHKW, Wärmemenge_BHKW, Strommenge_BHKW, Art, Brennstoffbedarf_BHKW, spez_Brennstoffkosten, Strompreis):
    # Holzvergaser-BHKW: 130 kW: 240.000 -> 1850 €/kW
    # (Erd-)Gas-BHKW: 100 kW: 150.000 € -> 1500 €/kW
    if Art == "BHKW":
        spez_Investitionskosten_BHKW = 1500  # €/kW
    elif Art == "Holzgas-BHKW":
        spez_Investitionskosten_BHKW = 1850  # €/kW

    Investitionskosten_BHKW = spez_Investitionskosten_BHKW * Wärmeleistung_BHKW
    Nutzungsdauer_BHKW = 15

    Anteil_Betriebskosten_BHKW = 0.02
    Betriebskosten_BHKW_Jahr = Investitionskosten_BHKW * Anteil_Betriebskosten_BHKW
    Betriebskosten_BHKW_Gesamt = Betriebskosten_BHKW_Jahr * Nutzungsdauer_BHKW

    Brennstoffkosten_BHKW_Jahr = spez_Brennstoffkosten * Brennstoffbedarf_BHKW
    Brennstoffkosten_BHKW_Gesamt = Brennstoffkosten_BHKW_Jahr * Nutzungsdauer_BHKW

    Gesamtkosten_BHKW = Investitionskosten_BHKW + Betriebskosten_BHKW_Gesamt + Brennstoffkosten_BHKW_Gesamt
    Wärmemenge_BHKW_Gesamt = Wärmemenge_BHKW * Nutzungsdauer_BHKW
    Strommenge_BHKW_Gesamt = Strommenge_BHKW * Nutzungsdauer_BHKW
    Stromeinnahmen_Gesamt = Strommenge_BHKW_Gesamt * Strompreis

    WGK_BHKW = (Gesamtkosten_BHKW-Stromeinnahmen_Gesamt) / Wärmemenge_BHKW_Gesamt

    return WGK_BHKW

def BHKW(el_Leistung_Soll, Last_L):
    el_Wirkungsgrad = 0.33
    KWK_Wirkungsgrad = 0.9
    thermischer_Wirkungsgrad = KWK_Wirkungsgrad - el_Wirkungsgrad
    Wärmeleistung_BHKW = round((el_Leistung_Soll / el_Wirkungsgrad) * thermischer_Wirkungsgrad, 0)

    Wärmeleistung_BHKW_L = []
    el_Leistung_BHKW_L = []
    Betriebsstunden_BHKW = 0
    Wärmemenge_BHKW = 0
    Strommenge_BHKW = 0
    for l in Last_L:
        if l >= Wärmeleistung_BHKW:
            Wärmeleistung_BHKW_L.append(Wärmeleistung_BHKW)
            el_Leistung_BHKW_L.append(el_Leistung_Soll)
            Wärmemenge_BHKW += Wärmeleistung_BHKW / 1000
            Strommenge_BHKW += el_Leistung_Soll / 1000
            Betriebsstunden_BHKW += 1
        else:
            Wärmeleistung_BHKW_L.append(l)
            el_Leistung_BHKW_L.append(el_Leistung_Soll*(l/Wärmeleistung_BHKW))
            Wärmemenge_BHKW += l / 1000
            Strommenge_BHKW += el_Leistung_Soll*(l/Wärmeleistung_BHKW) /1000

    Gasbedarf_BHKW = (Wärmemenge_BHKW + Strommenge_BHKW) / KWK_Wirkungsgrad

    return Wärmeleistung_BHKW, Wärmeleistung_BHKW_L, el_Leistung_BHKW_L, Wärmemenge_BHKW, Strommenge_BHKW, Gasbedarf_BHKW

def Berechnung_Erzeugermix(Bruttofläche_STA, VS, Typ, Fläche, Bohrtiefe, f_P_GK, Gaspreis, Strompreis, Holzpreis, filename, tech_order, el_Leistung_BHKW):
    Kühlleistung_Abwärme = 10  # kW
    Temperatur_Abwärme = 30  # °C
    Kühlleistung_AWW = 30  # kW
    Temperatur_AWW = 10  # °C
    Temperatur_Geothermie = 15  # °C

    Jahreswärmebedarf = Daten(filename)[9]
    Last_L = Daten(filename)[6]
    VLT_L = Daten(filename)[7]


    Restlast_L = Last_L.copy()
    Restwärmebedarf = Jahreswärmebedarf
    WGK_Gesamt = 0

    Wärmemenge_Geothermie = 0
    Wärmemenge_Abwärme = 0
    Wärmemenge_AWW = 0
    Strombedarf_WP = 0
    Strommenge_BHKW = 0
    el_Leistung_ges_L = np.zeros_like(Last_L)
    Wärmeleistung_ges_L = np.zeros_like(Last_L)

    data = []
    data_labels = []
    colors = []

    P_max = max(Last_L) * 1.1
    P_ein_GK = P_max * f_P_GK

    # zunächst Berechnung der Erzeugung
    for tech in tech_order:
        if tech == "Solarthermie":
            Wärmemenge_Solarthermie, Wärmeleistung_Solarthermie_L = Berechnung_STA(Bruttofläche_STA, VS, Typ, filename)

            Restlast_L -= Wärmeleistung_Solarthermie_L

            Restwärmebedarf -= Wärmemenge_Solarthermie

            Anteil_Solarthermie = Wärmemenge_Solarthermie / Jahreswärmebedarf

            data.append(Wärmeleistung_Solarthermie_L)
            data_labels.append("thermische Leistung Solarthermie")
            colors.append("red")

        elif tech == "Abwärme":
            Wärmemenge_Abwärme, Strombedarf_Abwärme, Wärmeleistung_Abwärme_L, el_Leistung_Abwärme_L, \
                max_Wärmeleistung_Abwärme, Betriebsstunden_Abwärme = aw(Restlast_L, VLT_L, Kühlleistung_Abwärme, Temperatur_Abwärme)

            el_Leistung_ges_L += el_Leistung_Abwärme_L
            Wärmeleistung_ges_L += Wärmeleistung_Abwärme_L
            Restlast_L -= Wärmeleistung_Abwärme_L

            Restwärmebedarf -= Wärmemenge_Abwärme
            Strombedarf_WP += Strombedarf_Abwärme

            Anteil_Abwärme = Wärmemenge_Abwärme / Jahreswärmebedarf

            data.append(Wärmeleistung_Abwärme_L)
            data_labels.append("thermische Leistung Abwärmepumpe")
            colors.append("grey")

        elif tech == "Abwasserwärme":
            Wärmemenge_AWW, Strombedarf_AWW, Wärmeleistung_AWW_L, el_Leistung_AWW_L, max_Wärmeleistung_AWW, Betriebsstunden_AWW\
                = aw(Restlast_L, VLT_L, Kühlleistung_AWW, Temperatur_AWW)

            el_Leistung_ges_L += el_Leistung_AWW_L
            Wärmeleistung_ges_L += Wärmeleistung_AWW_L
            Restlast_L -= Wärmeleistung_AWW_L

            Restwärmebedarf -= Wärmemenge_AWW
            Strombedarf_WP += Strombedarf_AWW

            Anteil_AWW = Wärmemenge_AWW / Jahreswärmebedarf

            data.append(Wärmeleistung_AWW_L)
            data_labels.append("thermische Leistung Abwasserwärmepumpe")
            colors.append("brown")

        elif tech == "Geothermie":
            Wärmemenge_Geothermie, Strombedarf_Geothermie, Wärmeleistung_Geothermie_L, el_Leistung_Geothermie_L, \
                max_Wärmeleistung, Investitionskosten_Sonden = Geothermie(Restlast_L, VLT_L, Fläche, Bohrtiefe,
                                                                          Temperatur_Geothermie)
            spez_Investitionskosten_Erdsonden = Investitionskosten_Sonden / max_Wärmeleistung

            el_Leistung_ges_L += el_Leistung_Geothermie_L
            Wärmeleistung_ges_L += Wärmeleistung_Geothermie_L
            Restlast_L -= Wärmeleistung_Geothermie_L

            Restwärmebedarf -= Wärmemenge_Geothermie
            Strombedarf_WP += Strombedarf_Geothermie

            Anteil_Geothermie = Wärmemenge_Geothermie / Jahreswärmebedarf

            data.append(Wärmeleistung_Geothermie_L)
            data_labels.append("thermische Leistung Erdsonden-Wärmepumpe")
            colors.append("blue")

        elif tech == "BHKW" or tech == "Holzgas-BHKW":
            Wärmeleistung_BHKW, Wärmeleistung_BHKW_L, el_Leistung_BHKW_L, Wärmemenge_BHKW, Strommenge_BHKW, \
                Brennstoffbedarf_BHKW = BHKW(el_Leistung_BHKW, Restlast_L)

            Wärmeleistung_ges_L += Wärmeleistung_BHKW_L

            Restlast_L -= Wärmeleistung_BHKW_L
            Restwärmebedarf -= Wärmemenge_BHKW

            Anteil_BHKW = Wärmemenge_BHKW / Jahreswärmebedarf

            data.append(Wärmeleistung_BHKW_L)
            data_labels.append("thermische Leistung BHKW")
            colors.append("yellow")

        elif tech == "Gaskessel":
            Wärmemenge_GK, WGK_GK, Wärmeleistung_GK_L = WGK_Gaskessel(Last_L, P_ein_GK, P_max, Gaspreis)

            Restlast_L -= Wärmeleistung_GK_L
            Restwärmebedarf -= Wärmemenge_GK

            Anteil_Erdgas = Wärmemenge_GK / Jahreswärmebedarf

            data.append(Wärmeleistung_GK_L)
            data_labels.append("thermische Leistung Gaskessel")
            colors.append("purple")

        elif tech == "Biomassekessel":
            P_BMK = P_ein_GK - max(Wärmeleistung_ges_L)
            Wärmemenge_BMK = Restwärmebedarf - WGK_Gaskessel(Last_L, P_ein_GK, P_max, Gaspreis)[0]
            Wärmeleistung_BMK_L = Restlast_L

            Anteil_Holzpellets = Wärmemenge_BMK / Jahreswärmebedarf

            data.append(Wärmeleistung_BMK_L)
            data_labels.append("thermische Leistung Biomassekessel")
            colors.append("green")

    # nun Berechnung der Wärmegestehungskosten
    for tech in tech_order:
        if tech == "Solarthermie":
            WGK_Solarthermie = WGK_STA(Bruttofläche_STA, VS, Typ, filename)
            WGK_Gesamt += Wärmemenge_Solarthermie * WGK_Solarthermie

        elif tech == "Abwärme":
            WGK_Abwärme = WGK_WP(max_Wärmeleistung, Wärmemenge_Abwärme, Strombedarf_Abwärme, tech, 0, Strompreis)
            WGK_Gesamt += Wärmemenge_Abwärme * WGK_Abwärme

        elif tech == "Abwasserwärme":
            WGK_AWW = WGK_WP(max_Wärmeleistung, Wärmemenge_Abwärme, Strombedarf_Abwärme, tech, 0, Strompreis)
            WGK_Gesamt += Wärmemenge_AWW * WGK_AWW

        elif tech == "Geothermie":
            WGK_Geothermie = WGK_WP(max_Wärmeleistung, Wärmemenge_Geothermie, Strombedarf_Geothermie, tech,
                                    spez_Investitionskosten_Erdsonden, Strompreis)
            WGK_Gesamt += Wärmemenge_Geothermie * WGK_Geothermie

        elif tech == "BHKW":
            WGK_BHKW = wgk_BHKW(Wärmeleistung_BHKW, Wärmemenge_BHKW, Strommenge_BHKW, tech, Brennstoffbedarf_BHKW,
                                Gaspreis, Strompreis)
            WGK_Gesamt += Wärmemenge_BHKW * WGK_BHKW

        elif tech == "Holzgas-BHKW":
            WGK_BHKW = wgk_BHKW(Wärmeleistung_BHKW, Wärmemenge_BHKW, Strommenge_BHKW, tech, Brennstoffbedarf_BHKW,
                                Holzpreis, Strompreis)
            WGK_Gesamt += Wärmemenge_BHKW * WGK_BHKW

        elif tech == "Gaskessel":
            Wärmemenge_GK, WGK_GK, Wärmeleistung_GK_L = WGK_Gaskessel(Last_L, P_ein_GK, P_max, Gaspreis)
            WGK_Gesamt += Wärmemenge_GK * WGK_GK

        elif tech == "Biomassekessel":
            WGK_BMK = WGK_Biomassekessel(P_BMK, Wärmemenge_BMK, Holzpreis)
            WGK_Gesamt += Wärmemenge_BMK * WGK_BMK

    WGK_Gesamt /= Jahreswärmebedarf

    """print("Jahreswärmebedarf: " + str(round(Jahreswärmebedarf, 2)) + " MWh")
    print("Wärmemenge Solarthermie: " + str(round(Wärmemenge_Solarthermie, 2)) + " MWh")
    #print("Wärmemenge Abwärme: " + str(round(Wärmemenge_Abwärme, 2)) + " MWh")
    #print("Wärmemenge Abwasserwärme: " + str(round(Wärmemenge_AWW, 2)) + " MWh")
    print("Wärmemenge Geothermie: " + str(round(Wärmemenge_Geothermie, 2)) + " MWh")
    print("Wärmemenge BHKW: " + str(round(Wärmemenge_BHKW, 2)) + " MWh")
    print("Wärmemenge BMK: " + str(round(Wärmemenge_BMK, 2)) + " MWh")
    print("Wärmemenge GK: " + str(round(Wärmemenge_GK, 2)) + " MWh")

    print("Anteil Solarthermie an Wärmeversorgung: " + str(round(Anteil_Solarthermie, 3)))
    #print("Anteil Abwärme an Wärmeversorgung: " + str(round(Anteil_Abwärme, 3)))
    #print("Anteil Abwasserwärme an Wärmeversorgung: " + str(round(Anteil_AWW, 3)))
    print("Anteil Geothermie an Wärmeversorgung: " + str(round(Anteil_Geothermie, 3)))
    print("Anteil BHKW an Wärmeversorgung: " + str(round(Anteil_BHKW, 3)))
    print("Anteil Holzpellets an Wärmeversorgung: " + str(round(Anteil_Holzpellets, 3)))
    print("Anteil Erdgas an Wärmeversorgung: " + str(round(Anteil_Erdgas, 3)))

    print("Wärmegestehungskosten Solarthermie: " + str(round(WGK_Solarthermie, 2)) + " €/MWh")
    #print("Wärmegestehungskosten Abwärme: " + str(round(WGK_Abwärme, 2)) + " €/MWh")
    #print("Wärmegestehungskosten Abwasserwärme: " + str(round(WGK_AWW, 2)) + " €/MWh")
    print("Wärmegestehungskosten Geothermie: " + str(round(WGK_Geothermie, 2)) + " €/MWh")
    print("Wärmegestehungskosten BHKW: " + str(round(WGK_BHKW, 2)) + " €/MWh")
    print("Wärmegestehungskosten BMK: " + str(round(WGK_BMK, 2)) + " €/MWh")
    print("Wärmegestehungskosten GK: " + str(round(WGK_GK, 2)) + " €/MWh")
    print("Wärmegestehungskosten Gesamt: " + str(round(WGK_Gesamt, 2)) + " €/MWh")

    plt.plot(range(1, 8761), Last_L, color="black", linewidth=1, label="Last in kW")
    plt.stackplot(range(1, 8761), data, labels=data_labels, colors=colors)

    plt.title("Lastgang und Erzeugung Wärmenetz")
    plt.xlabel("Jahresstunden")
    plt.ylabel("thermische Leistung in kW")
    plt.legend(loc='upper center')
    plt.show()"""

    return WGK_Gesamt

# tech_order = ["Solarthermie", "Geothermie", "BHKW", "Biomassekessel", "Gaskessel"]
tech_order = ["Solarthermie", "Geothermie", "BHKW", "Biomassekessel", "Gaskessel"]

# Berechnung_Erzeugermix(Fläche STA, Volumen Speicher, Typ STA, Fläche Erdsondenfeld, Tiefe Erdsondenbohrung, Einschaltpunkt GK, Gaspreis, Strompreis, Holzpreis, Dateiname, tech_order, Leistung BHKW)
Berechnung_Erzeugermix(600, 20, "Flachkollektor", 2000, 200, 0.5, 100, 200, 50, "Daten.csv", tech_order, 80)

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


# Optimierung_Erzeugermix()
