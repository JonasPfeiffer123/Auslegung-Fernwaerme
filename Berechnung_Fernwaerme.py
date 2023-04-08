# Berechnungsprogramm Fernwärme-Erzeugermix
# Import Bibliotheken
import numpy as np
from Berechnung_Solarthermie import Berechnung_STA, Daten
from Berechnung_Erzeuger import aw, Geothermie, BHKW, Biomassekessel, Gaskessel
from Wirtschaftlichkeitsbetrachtung import WGK_WP, WGK_BHKW, WGK_Biomassekessel, WGK_Gaskessel, WGK_STA

def Berechnung_Erzeugermix(bruttofläche_STA, vs, Typ, Fläche, Bohrtiefe, P_BMK, Gaspreis, Strompreis, Holzpreis,
                           filename, tech_order, BEW, el_Leistung_BHKW=0, Kapitalzins=5, Preissteigerungsrate=3,
                           Betrachtungszeitraum=20):
    # Kapitalzins und Preissteigerungsrate in % -> Umrechung in Zinsfaktor und Preissteigerungsfaktor
    q = 1 + Kapitalzins/100
    r = 1 + Preissteigerungsrate/100
    T = Betrachtungszeitraum

    Kühlleistung_Abwärme = 30  # kW
    Temperatur_Abwärme = 30  # °C
    Kühlleistung_AWW = 30  # kW
    Temperatur_AWW = 10  # °C
    Temperatur_Geothermie = 15  # °C

    Jahreswärmebedarf = Daten(filename)[9]
    Last_L = Daten(filename)[6]
    VLT_L = Daten(filename)[7]

    print("Jahreswärmebedarf: " + str(round(Jahreswärmebedarf, 2)) + " MWh")

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
    colors = []

    WGK = []
    Anteile = []
    Wärmemengen = []
    Deckungsanteil = 0
    # zunächst Berechnung der Erzeugung
    for tech in tech_order:
        if tech == "Solarthermie":
            Wärmemenge_Solarthermie, Wärmeleistung_Solarthermie_L = Berechnung_STA(bruttofläche_STA, vs, Typ, filename)

            Restlast_L -= Wärmeleistung_Solarthermie_L

            Restwärmebedarf -= Wärmemenge_Solarthermie

            Anteil_Solarthermie = Wärmemenge_Solarthermie / Jahreswärmebedarf

            data.append(Wärmeleistung_Solarthermie_L)
            colors.append("red")

            WGK_Solarthermie = WGK_STA(bruttofläche_STA, vs, Typ, Wärmemenge_Solarthermie, q, r, T, BEW)
            WGK_Gesamt += Wärmemenge_Solarthermie * WGK_Solarthermie

            Wärmemengen.append(Wärmemenge_Solarthermie)
            Anteile.append(Anteil_Solarthermie)
            WGK.append(WGK_Solarthermie)
            print("Wärmemenge Solarthermie: " + str(round(Wärmemenge_Solarthermie, 2)) + " MWh")
            print("Anteil Solarthermie an Wärmeversorgung: " + str(round(Anteil_Solarthermie, 3)))
            print("Wärmegestehungskosten Solarthermie: " + str(round(WGK_Solarthermie, 2)) + " €/MWh")

            Deckungsanteil = Wärmemenge_Solarthermie / Jahreswärmebedarf * 100  # %

        elif tech == "Abwärme":
            Wärmemenge_Abwärme, Strombedarf_Abwärme, Wärmeleistung_Abwärme_L, el_Leistung_Abwärme_L, \
                max_Wärmeleistung_Abwärme, Betriebsstunden_Abwärme = aw(Restlast_L, VLT_L, Kühlleistung_Abwärme,
                                                                        Temperatur_Abwärme)

            el_Leistung_ges_L += el_Leistung_Abwärme_L
            Wärmeleistung_ges_L += Wärmeleistung_Abwärme_L
            Restlast_L -= Wärmeleistung_Abwärme_L

            Restwärmebedarf -= Wärmemenge_Abwärme
            Strombedarf_WP += Strombedarf_Abwärme

            Anteil_Abwärme = Wärmemenge_Abwärme / Jahreswärmebedarf

            data.append(Wärmeleistung_Abwärme_L)
            colors.append("grey")

            WGK_Abwärme = WGK_WP(max_Wärmeleistung_Abwärme, Wärmemenge_Abwärme, Strombedarf_Abwärme, tech, 0,
                                 Strompreis, q, r, T)
            WGK_Gesamt += Wärmemenge_Abwärme * WGK_Abwärme

            Wärmemengen.append(Wärmemenge_Abwärme)
            Anteile.append(Anteil_Abwärme)
            WGK.append(WGK_Abwärme)

            print("Wärmemenge Abwärme: " + str(round(Wärmemenge_Abwärme, 2)) + " MWh")
            print("Anteil Abwärme an Wärmeversorgung: " + str(round(Anteil_Abwärme, 3)))
            print("Wärmegestehungskosten Abwärme: " + str(round(WGK_Abwärme, 2)) + " €/MWh")

        elif tech == "Abwasserwärme":
            Wärmemenge_AWW, Strombedarf_AWW, Wärmeleistung_AWW_L, el_Leistung_AWW_L, max_Wärmeleistung_AWW, \
                Betriebsstunden_AWW = aw(Restlast_L, VLT_L, Kühlleistung_AWW, Temperatur_AWW)

            el_Leistung_ges_L += el_Leistung_AWW_L
            Wärmeleistung_ges_L += Wärmeleistung_AWW_L
            Restlast_L -= Wärmeleistung_AWW_L

            Restwärmebedarf -= Wärmemenge_AWW
            Strombedarf_WP += Strombedarf_AWW

            Anteil_AWW = Wärmemenge_AWW / Jahreswärmebedarf

            data.append(Wärmeleistung_AWW_L)
            colors.append("brown")

            WGK_AWW = WGK_WP(max_Wärmeleistung, Wärmemenge_Abwärme, Strombedarf_Abwärme, tech, 0, Strompreis, q, r, T)
            WGK_Gesamt += Wärmemenge_AWW * WGK_AWW

            Wärmemengen.append(Wärmemenge_AWW)
            Anteile.append(Anteil_AWW)
            WGK.append(WGK_AWW)
            print("Wärmemenge Abwasserwärme: " + str(round(Wärmemenge_AWW, 2)) + " MWh")
            print("Anteil Abwasserwärme an Wärmeversorgung: " + str(round(Anteil_AWW, 3)))
            print("Wärmegestehungskosten Abwasserwärme: " + str(round(WGK_AWW, 2)) + " €/MWh")

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
            colors.append("blue")

            WGK_Geothermie = WGK_WP(max_Wärmeleistung, Wärmemenge_Geothermie, Strombedarf_Geothermie, tech,
                                    spez_Investitionskosten_Erdsonden, Strompreis, q, r, T)
            WGK_Gesamt += Wärmemenge_Geothermie * WGK_Geothermie

            Wärmemengen.append(Wärmemenge_Geothermie)
            Anteile.append(Anteil_Geothermie)
            WGK.append(WGK_Geothermie)
            print("Wärmemenge Geothermie: " + str(round(Wärmemenge_Geothermie, 2)) + " MWh")
            print("Anteil Geothermie an Wärmeversorgung: " + str(round(Anteil_Geothermie, 3)))
            print("Wärmegestehungskosten Geothermie: " + str(round(WGK_Geothermie, 2)) + " €/MWh")

        elif tech == "BHKW" or tech == "Holzgas-BHKW":
            el_Leistung_BHKW = max(el_Leistung_ges_L) if max(el_Leistung_ges_L) > 0 else el_Leistung_BHKW

            Wärmeleistung_BHKW, Wärmeleistung_BHKW_L, el_Leistung_BHKW_L, Wärmemenge_BHKW, Strommenge_BHKW, \
                Brennstoffbedarf_BHKW = BHKW(el_Leistung_BHKW, Restlast_L)

            Wärmeleistung_ges_L += Wärmeleistung_BHKW_L

            Restlast_L -= Wärmeleistung_BHKW_L
            Restwärmebedarf -= Wärmemenge_BHKW

            Anteil_BHKW = Wärmemenge_BHKW / Jahreswärmebedarf

            data.append(Wärmeleistung_BHKW_L)
            colors.append("yellow")

            if tech == "BHKW":
                Brennstoffpreis = Gaspreis
            elif tech == "Holzgas-BHKW":
                Brennstoffpreis = Holzpreis

            wgk_BHKW = WGK_BHKW(Wärmeleistung_BHKW, Wärmemenge_BHKW, Strommenge_BHKW, tech, Brennstoffbedarf_BHKW,
                                Brennstoffpreis, Strompreis, q, r, T)
            WGK_Gesamt += Wärmemenge_BHKW * wgk_BHKW

            Wärmemengen.append(Wärmemenge_BHKW)
            Anteile.append(Anteil_BHKW)
            WGK.append(wgk_BHKW)
            print("Wärmemenge BHKW: " + str(round(Wärmemenge_BHKW, 2)) + " MWh")
            print("Anteil BHKW an Wärmeversorgung: " + str(round(Anteil_BHKW, 3)))
            print("Wärmegestehungskosten BHKW: " + str(round(wgk_BHKW, 2)) + " €/MWh")

        elif tech == "Gaskessel":
            Wärmemenge_GK, Wärmeleistung_GK_L, Gasbedarf = Gaskessel(Restlast_L)
            P_max = max(Last_L) * 1
            WGK_GK = WGK_Gaskessel(P_max, Wärmemenge_GK, Gasbedarf, Gaspreis, q, r, T)

            Restlast_L -= Wärmeleistung_GK_L
            Restwärmebedarf -= Wärmemenge_GK

            Anteil_GK = Wärmemenge_GK / Jahreswärmebedarf

            data.append(Wärmeleistung_GK_L)
            colors.append("purple")

            WGK_Gesamt += Wärmemenge_GK * WGK_GK

            Wärmemengen.append(Wärmemenge_GK)
            Anteile.append(Anteil_GK)
            WGK.append(WGK_GK)
            print("Wärmemenge Gaskessel: " + str(round(Wärmemenge_GK, 2)) + " MWh")
            print("Anteil Erdgas an Wärmeversorgung: " + str(round(Anteil_GK, 3)))
            print("Wärmegestehungskosten Gaskessel: " + str(round(WGK_GK, 2)) + " €/MWh")

        elif tech == "Biomassekessel":
            Wärmeleistung_BMK_L, Wärmemenge_BMK = Biomassekessel(Restlast_L, P_BMK)

            Restlast_L -= Wärmeleistung_BMK_L
            Restwärmebedarf -= Wärmemenge_BMK

            Anteil_BMK = Wärmemenge_BMK / Jahreswärmebedarf

            data.append(Wärmeleistung_BMK_L)
            colors.append("green")

            Nutzungsgrad_BMK = 0.8
            Brennstoffbedarf_BMK = Wärmemenge_BMK/Nutzungsgrad_BMK
            WGK_BMK = WGK_Biomassekessel(P_BMK, Wärmemenge_BMK, Brennstoffbedarf_BMK, Holzpreis, q, r, T)
            WGK_Gesamt += Wärmemenge_BMK * WGK_BMK

            Wärmemengen.append(Wärmemenge_BMK)
            Anteile.append(Anteil_BMK)
            WGK.append(WGK_BMK)
            print("Wärmemenge Biomassekessel: " + str(round(Wärmemenge_BMK, 2)) + " MWh")
            print("Anteil Biomassekessel an Wärmeversorgung: " + str(round(Anteil_BMK, 3)))
            print("Wärmegestehungskosten Biomassekessel: " + str(round(WGK_BMK, 2)) + " €/MWh")

    WGK_Gesamt /= Jahreswärmebedarf
    print("Wärmegestehungskosten Gesamt: " + str(round(WGK_Gesamt, 2)) + " €/MWh")

    """plt.plot(range(1, 8761), Last_L, color="black", linewidth=1, label="Last in kW")
    plt.stackplot(range(1, 8761), data, labels=tech_order, colors=colors)

    plt.title("Lastgang und Erzeugung Wärmenetz")
    plt.xlabel("Jahresstunden")
    plt.ylabel("thermische Leistung in kW")
    plt.legend(loc='upper center')
    plt.show()"""

    if BEW == "Ja":
        WGK_Gesamt = 0
    return WGK_Gesamt, Jahreswärmebedarf, Deckungsanteil, Last_L, data, tech_order, colors, Wärmemengen, WGK, Anteile

tech_order_d = ["Solarthermie", "Geothermie", "Holzgas-BHKW", "Biomassekessel", "Gaskessel"]
tech_order_g = ["Solarthermie", "Holzgas-BHKW", "Geothermie", "Biomassekessel", "Gaskessel"]
techorder_beleg = ["Solarthermie", "Geothermie", "Biomassekessel", "Gaskessel"]

# Berechnung_Erzeugermix(Fläche STA, Volumen Speicher, Typ STA, Fläche Erdsondenfeld, Tiefe Erdsondenbohrung,
# Einschaltpunkt GK, Gaspreis, Strompreis, Holzpreis, Dateiname, tech_order_d, BEW, Leistung BHKW)

# Berechnung_Erzeugermix(600, 20, "Vakuumröhrenkollektor", 2000, 200, 0.5, 100, 200, 50, "Daten.csv", tech_order,"Nein")

# Berechnung_Erzeugermix(1000, 30, "Vakuumröhrenkollektor", 11000, 150, 0.5, 100, 200, 50, "Daten Görlitz.csv",
# tech_order_g, "Nein", 210)

# Berechnung_Erzeugermix(1000, 50, "Vakuumröhrenkollektor", 2000, 100, 0.5, 100, 200, 50, "Daten Görlitz Beleg.csv",
# techorder_beleg, "Nein")
