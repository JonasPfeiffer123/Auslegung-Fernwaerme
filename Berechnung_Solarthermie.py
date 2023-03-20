# Ertragsberechnungsprogramm Solarthermie in Wärmenetz (Berechnungsgrundlage: ScenoCalc Fernwärme 2.0 https://www.scfw.de/)

# Import Bibliotheken
from math import pi, exp, log, sqrt
import csv
import numpy as np

def Daten(filename):
    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")
        next(csv_reader)  # skip header
        data = np.array(list(csv_reader)).astype(float)

        Jahresstunden_L = data[:, 0]
        Stunde_L = data[:, 1]
        Tag_des_Jahres_L = data[:, 2]
        Temperatur_L = data[:, 3]
        Einstrahlung_hori_L = data[:, 4]
        Windgeschwindigkeit_L = data[:, 5]
        Last_L = data[:, 6]
        Jahreswärmebedarf = np.sum(Last_L)/1000
        VLT_L = data[:, 7]
        RLT_L = data[:, 8]

    return Jahresstunden_L, Stunde_L, Tag_des_Jahres_L, Einstrahlung_hori_L, \
            Temperatur_L, Windgeschwindigkeit_L, Last_L, VLT_L, RLT_L, Jahreswärmebedarf

def vorzeichen(zahl):
    return (zahl > 0) ^ (zahl < 0)

def Berechnung_Solarstrahlung(Stunde_L, Tag_des_Jahres_L, Einstrahlung_hori_L,
                              Longitude, STD_Longitude, Latitude,Albedo, IAM_W, IAM_N):
    East_West_collector_azimuth_angle = 0  # Keine Nachführung
    Collector_tilt_angle = 35  # Keine Nachführung
    B = (Tag_des_Jahres_L - 1) * 360 / 365  # °
    E = 229.2 * (0.000075 + 0.001868 * np.cos(B * np.pi / 180) - 0.032077 * np.sin(B * np.pi / 180) - 0.014615 * np.cos(
        2 * B * np.pi / 180) - 0.04089 * np.sin(2 * B * np.pi / 180))

    Solar_time = ((Stunde_L - 0.5) * 3600 + E * 60 + 4 * (STD_Longitude - Longitude) * 60) / 3600

    Solar_declination = 23.45 * np.sin(360 * (284 + Tag_des_Jahres_L) / 365 * np.pi / 180)

    Hour_angle = -180 + Solar_time * 180 / 12

    Solar_Zenith_angle = 180 / np.pi * np.arccos(
        np.cos(Latitude * np.pi / 180) * np.cos(Hour_angle * np.pi / 180) * np.cos(Solar_declination * np.pi / 180) +
        np.sin(Latitude * np.pi / 180) * np.sin(Solar_declination * np.pi / 180))

    East_West_solar_azimuth_angle = vorzeichen(Hour_angle) * 180 / np.pi * np.arccos(
        (np.cos(Solar_Zenith_angle * np.pi / 180) * np.sin(Latitude * np.pi / 180) - np.sin(Solar_declination * pi / 180)) /
        (np.sin(Solar_Zenith_angle * np.pi / 180) * np.cos(Latitude * np.pi / 180)))

    Incidence_angle_onto_collector = 180 / np.pi * \
                                     np.arccos(np.cos(Solar_Zenith_angle * np.pi / 180) * np.cos(Collector_tilt_angle * np.pi / 180) +
                                          np.sin(Solar_Zenith_angle * np.pi / 180) * np.sin(Collector_tilt_angle * np.pi / 180) *
                                          np.cos((East_West_solar_azimuth_angle - East_West_collector_azimuth_angle) * np.pi / 180) + 0.0000000001)

    condition = (Solar_Zenith_angle < 90) & (Incidence_angle_onto_collector < 90)
    function_EW = 180 / np.pi * np.arctan(np.sin(Solar_Zenith_angle * np.pi / 180) *
                                          np.sin((East_West_solar_azimuth_angle -
                                                  East_West_collector_azimuth_angle) * np.pi / 180) /
                                          np.cos(Incidence_angle_onto_collector * np.pi / 180))

    function_NS = -(180 / pi * np.arctan(np.tan(Solar_Zenith_angle * pi / 180) *
                                         np.cos((East_West_solar_azimuth_angle -
                                                 East_West_collector_azimuth_angle) * pi / 180)) - Collector_tilt_angle)

    Incidence_angle_EW = np.where(condition, function_EW, 89.999)
    Incidence_angle_NS = np.where(condition, function_NS, 89.999)

    def IAM_EW(Incidence_angle_EW, iam_w):
        sverweis_1 = np.abs(Incidence_angle_EW) - np.abs(Incidence_angle_EW) % 10
        sverweis_2 = np.vectorize(iam_w.get)(sverweis_1)
        sverweis_3 = (np.abs(Incidence_angle_EW) + 10) - (np.abs(Incidence_angle_EW) + 10) % 10
        sverweis_4 = np.vectorize(iam_w.get)(sverweis_3)

        ergebnis = sverweis_2 + (np.abs(Incidence_angle_EW) - sverweis_1) / (sverweis_3 - sverweis_1) * (
                sverweis_4 - sverweis_2)
        return ergebnis

    IAM_EW = IAM_EW(Incidence_angle_EW, IAM_W)

    def IAM_NS(Incidence_angle_NS, iam_n):
        sverweis_1 = np.abs(Incidence_angle_NS) - np.abs(Incidence_angle_NS) % 10
        sverweis_2 = np.vectorize(lambda x: iam_n.get(x, None))(sverweis_1)
        sverweis_3 = (np.abs(Incidence_angle_NS) + 10) - (np.abs(Incidence_angle_NS) + 10) % 10
        sverweis_4 = np.vectorize(lambda x: iam_n.get(x, None))(sverweis_3)

        ergebnis = sverweis_2 + (np.abs(Incidence_angle_NS) - sverweis_1) / (sverweis_3 - sverweis_1) * (
                sverweis_4 - sverweis_2)
        return ergebnis

    IAM_NS = IAM_NS(Incidence_angle_NS, IAM_N)

    function_Rb = np.cos(Incidence_angle_onto_collector * np.pi / 180) / np.cos(Solar_Zenith_angle * np.pi / 180)
    Rb = np.where(condition, function_Rb, 0)

    Wert = 0

    Gbhoris = Wert * np.cos(Solar_Zenith_angle * np.pi / 180)

    Ai = Gbhoris / (1367 * (1 + 0.033 * np.cos(360 * Tag_des_Jahres_L / 365 * np.pi / 180)) * np.cos(Solar_Zenith_angle * np.pi / 180))

    Gdhoris = Einstrahlung_hori_L - Gbhoris

    GT_H_Gk = Gbhoris * Rb + Gdhoris * Ai * Rb + Gdhoris * (1 - Ai) * 0.5 * (1 + np.cos(Collector_tilt_angle * np.pi / 180)) + \
              Gdhoris * Albedo * (1 - 0.5) * (1 - np.cos(Collector_tilt_angle * np.pi / 180))

    GbT = Gbhoris * Rb
    GdT_H_Dk = GT_H_Gk - GbT
    K_beam = IAM_EW * IAM_NS

    return K_beam, GbT, GdT_H_Dk

def Berechnung_STA(Bruttofläche_STA, VS, Typ, filename):
    if Bruttofläche_STA == 0:
        return 0, 0, 0, 0
    if VS == 0:
        return 0, 0, 0, 0
    # statische Vorgabewerte
    # Location = "Bautzen"
    Longitude = -14.4222
    STD_Longitude = -15
    Latitude = 51.1676

    Albedo = 0.2
    wcorr = 0.5

    # Typ = "Flachkollektor"
    # Typ = "Röhrenkollektor"

    if Typ == "Flachkollektor":
        # Vorgabewerte Flachkollektor Vitosol 200-F XL13
        # Bruttofläche ist Bezugsfläche
        Eta0b_neu = 0.763
        Kthetadiff = 0.931
        Koll_c1 = 1.969
        Koll_c2 = 0.015
        Koll_c3 = 0
        KollCeff_A = 9.053
        KollAG = 13.17
        KollAAp = 12.35

        Aperaturfläche = Bruttofläche_STA * (KollAAp / KollAG)
        Bezugsfläche = Bruttofläche_STA

        IAM_W = {0: 1, 10: 1, 20: 0.99, 30: 0.98, 40: 0.96, 50: 0.91, 60: 0.82, 70: 0.53, 80: 0.27, 90: 0.0}
        IAM_N = {0: 1, 10: 1, 20: 0.99, 30: 0.98, 40: 0.96, 50: 0.91, 60: 0.82, 70: 0.53, 80: 0.27, 90: 0.0}

    if Typ == "Vakuumröhrenkollektor":
        # Vorgabewerte Vakuumröhrenkollektor
        # Aperaturfläche ist Bezugsfläche
        Eta0hem = 0.688
        a1 = 0.583
        a2 = 0.003
        KollCeff_A = 8.78
        KollAG = 4.94
        KollAAp = 4.5

        Koll_c1 = a1
        Koll_c2 = a2
        Koll_c3 = 0
        Eta0b_neu = 0.693
        Kthetadiff = 0.951

        Aperaturfläche = Bruttofläche_STA * (KollAAp / KollAG)
        Bezugsfläche = Aperaturfläche

        IAM_W = {0: 1, 10: 1.02, 20: 1.03, 30: 1.03, 40: 1.03, 50: 0.96, 60: 1.07, 70: 1.19, 80: 0.595, 90: 0.0}
        IAM_N = {0: 1, 10: 1, 20: 0.99, 30: 0.96, 40: 0.93, 50: 0.9, 60: 0.87, 70: 0.86, 80: 0.43, 90: 0.0}

    # Vorgabewerte Rohrleitungen
    Y_R = 2  # 1 oberirdisch, 2 erdverlegt, 3...
    Lrbin_E = 80
    Drbin_E = 0.1071
    P_KR_E = 0.26

    AR = Lrbin_E * Drbin_E * 3.14
    KR_E = P_KR_E * Lrbin_E / AR
    VRV_bin = Lrbin_E * (Drbin_E / 2) ** 2 * 3.14

    D46 = 0.035
    D47 = D46 / KR_E / 2
    L_Erdreich = 2
    D49 = 0.8
    # D50 = 2 * (Drbin_E + 2 * D47)
    D51 = L_Erdreich / D46 * log((Drbin_E / 2 + D47) / (Drbin_E / 2))
    D52 = log(2 * D49 / (Drbin_E / 2 + D47)) + D51 + log(sqrt(1 + (D49 / Drbin_E) ** 2))
    hs_RE = 1 / D52
    D54 = 2 * pi * L_Erdreich * hs_RE
    D55 = 2 * D54
    D56 = pi * (Drbin_E + 2 * D47)
    Keq_RE = D55 / D56
    CRK = VRV_bin * 3790 / 3.6 / AR  # 3790 für Glykol, 4180 für Wasser

    # Interne Verrohrung
    VRV = 0.0006
    KK = 0.06
    CKK = VRV * 3790 / 3.6

    # Vorgabewerte Speicher
    Tsmax = 90
    Tm_rl = 53.4
    QSmax = 1.16 * VS * (Tsmax - Tm_rl)
    Qsa = 0  # Speicherinhalt zu Beginn

    # Vorgabewerte Wärmenetz
    # Vorwärmbetrieb = 1
    Vorwärmung = 8  # K
    DT_WT_Solar = 5
    DT_WT_Netz = 5

    # dynamische Vorgabewerte
    Jahresstunden_L, Stunde_L, Tag_des_Jahres_L, Einstrahlung_hori_L, \
        Temperatur_L, Windgeschwindigkeit_L, Last_L, VLT_L, RLT_L, Jahreswärmebedarf = Daten(filename)

    K_beam_L, GbT_L, GdT_H_Dk_L = Berechnung_Solarstrahlung(Stunde_L, Tag_des_Jahres_L, Einstrahlung_hori_L, Longitude, STD_Longitude, Latitude, Albedo, IAM_W, IAM_N)

    Speicher_Wärmeoutput_L = []
    Speicherladung_L = []
    Jahreswärmemenge = 0

    Zähler = 0

    Kollektorfeldertrag_ges = 0

    #for Jahresstunden, Stunde, Tag_des_Jahres, Einstrahlung_hori, Temperatur, Windgeschwindigkeit, Last, VLT, RLT in zip(
    #        Jahresstunden_L, Stunde_L, Tag_des_Jahres_L, Einstrahlung_hori_L, Temperatur_L, Windgeschwindigkeit_L,
    #        Last_L, VLT_L, RLT_L):
    for Tag_des_Jahres, K_beam, GbT, GdT_H_Dk, Temperatur, Windgeschwindigkeit, Last, VLT, RLT in zip(Tag_des_Jahres_L, K_beam_L, GbT_L, GdT_H_Dk_L, Temperatur_L, Windgeschwindigkeit_L, Last_L, VLT_L, RLT_L):
        if Zähler < 1:
            TS_unten = RLT
            Zieltemperatur_Solaranlage = TS_unten + Vorwärmung + DT_WT_Solar + DT_WT_Netz
            TRL_Solar = RLT
            Tm_a = (Zieltemperatur_Solaranlage + TRL_Solar) / 2
            Pkoll_a = 0
            Tgkoll_a = 9.3
            T_koll_a = Temperatur - (Temperatur - Tgkoll_a) * exp(-Koll_c1 / KollCeff_A * 3.6) + (Pkoll_a * 3600) / (
                        KollCeff_A * Bezugsfläche)
            Pkoll_b = 0
            T_koll_b = Temperatur - (Temperatur - 0) * exp(-Koll_c1 / KollCeff_A * 3.6) + (Pkoll_b * 3600) / (
                        KollCeff_A * Bezugsfläche)
            Tgkoll = 9.3  # Kollektortemperatur im Gleichgewicht

            # Verluste Verbindungsleitung
            TRV_bin_vl = Temperatur
            TRV_bin_rl = Temperatur

            # Verluste interne Rohrleitungen
            TRV_int_vl = Temperatur
            TRV_int_rl = Temperatur
            Summe_PRV = 0  # Rohrleitungsverluste aufsummiert
            Kollektorfeldertrag = 0
            PSout = min(Kollektorfeldertrag, Last)
            QS = Qsa * 1000
            PSV = 0
            Tag_des_Jahres_alt = Tag_des_Jahres
            Stagnation = 0

        else:
            T_koll_a_alt = T_koll_a
            T_koll_b_alt = T_koll_b
            Tgkoll_a_alt = Tgkoll_a
            Tgkoll_alt = Tgkoll
            Summe_PRV_alt = Summe_PRV
            Zieltemperatur_Solaranlage_alt = Zieltemperatur_Solaranlage
            Kollektorfeldertrag_alt = Kollektorfeldertrag

            # Define constants
            c1 = Koll_c1 * (Tm_a - Temperatur)
            c2 = Koll_c2 * (Tm_a - Temperatur) ** 2
            c3 = Koll_c3 * wcorr * Windgeschwindigkeit * (Tm_a - Temperatur)
            Eta0b_neu_K_beam_GbT = Eta0b_neu * K_beam * GbT
            Eta0b_neu_Kthetadiff_GdT_H_Dk = Eta0b_neu * Kthetadiff * GdT_H_Dk

            # Calculate lower storage tank temperature
            if QS/QSmax >= 0.8:
                TS_unten = RLT + DT_WT_Netz + (2/3 * (VLT - RLT) / 0.2 * QS/QSmax) + (1 / 3 * (VLT - RLT)) - (2/3 * (VLT - RLT) / 0.2 * QS/QSmax)
            else:
                TS_unten = RLT + DT_WT_Netz + (1 / 3 * (VLT - RLT) / 0.8) * QS/QSmax

            # Calculate solar target temperature and return line temperature
            Zieltemperatur_Solaranlage = TS_unten + Vorwärmung + DT_WT_Solar + DT_WT_Netz
            TRL_Solar = TS_unten + DT_WT_Solar

            # Calculate collector A power output and temperature
            Pkoll_a = max(0,
                          (Eta0b_neu_K_beam_GbT + Eta0b_neu_Kthetadiff_GdT_H_Dk - c1 - c2 - c3) * Bezugsfläche / 1000)
            T_koll_a = Temperatur - (Temperatur - Tgkoll_a_alt) * exp(-Koll_c1 / KollCeff_A * 3.6) + (Pkoll_a * 3600) / (
                        KollCeff_A * Bezugsfläche)

            # Calculate collector B power output and temperature
            c1 = Koll_c1 * (T_koll_b_alt - Temperatur)
            c2 = Koll_c2 * (T_koll_b_alt - Temperatur) ** 2
            c3 = Koll_c3 * wcorr * Windgeschwindigkeit * (T_koll_b_alt - Temperatur)
            Pkoll_b = max(0,
                          (Eta0b_neu_K_beam_GbT + Eta0b_neu_Kthetadiff_GdT_H_Dk - c1 - c2 - c3) * Bezugsfläche / 1000)
            T_koll_b = Temperatur - (Temperatur - Tgkoll_a_alt) * exp(-Koll_c1 / KollCeff_A * 3.6) + (Pkoll_b * 3600) / (
                        KollCeff_A * Bezugsfläche)

            # Calculate new collector A glycol temperature and average temperature
            Tgkoll_a = min(Zieltemperatur_Solaranlage, T_koll_a)
            Tm_a = (Zieltemperatur_Solaranlage + TRL_Solar) / 2

            # calculate average collector temperature
            Tm_koll_alt = (T_koll_a_alt + T_koll_b_alt) / 2
            Tm_koll = (T_koll_a + T_koll_b) / 2
            Tm_sys = (Zieltemperatur_Solaranlage + TRL_Solar) / 2
            if Tm_koll < Tm_sys and Tm_koll_alt < Tm_sys:
                Tm = Tm_koll
            else:
                Tm = Tm_sys

            # calculate collector power output
            c1 = Koll_c1 * (Tm - Temperatur)
            c2 = Koll_c2 * (Tm - Temperatur) ** 2
            c3 = Koll_c3 * wcorr * Windgeschwindigkeit * (Tm - Temperatur)
            Pkoll = max(0, (Eta0b_neu_K_beam_GbT + Eta0b_neu_Kthetadiff_GdT_H_Dk - c1
                            - c2 - c3) * Bezugsfläche / 1000)

            # calculate collector temperature surplus
            T_koll = Temperatur - (Temperatur - Tgkoll) * exp(-Koll_c1 / KollCeff_A * 3.6) + (Pkoll * 3600) / (
                        KollCeff_A * Bezugsfläche)
            Tgkoll = min(Zieltemperatur_Solaranlage, T_koll)

            # Verluste Verbindungsleitung
            TRV_bin_vl_alt = TRV_bin_vl
            TRV_bin_rl_alt = TRV_bin_rl

            # Variablen für wiederkehrende Bedingungen definieren
            ziel_erreich = Tgkoll >= Zieltemperatur_Solaranlage and Pkoll > 0
            ziel_erhöht = Zieltemperatur_Solaranlage >= Zieltemperatur_Solaranlage_alt

            # Berechnung von TRV_bin_vl und TRV_bin_rl
            if ziel_erreich:
                TRV_bin_vl = Zieltemperatur_Solaranlage
                TRV_bin_rl = TRL_Solar
            else:
                TRV_bin_vl = Temperatur - (Temperatur - TRV_bin_vl_alt) * exp(-Keq_RE / CRK)
                TRV_bin_rl = Temperatur - (Temperatur - TRV_bin_rl_alt) * exp(-Keq_RE / CRK)

            # Funktion zur Berechnung von P_RVT_bin_vl und P_RVT_bin_rl
            def calc_P_RVT_bin(TRV_bin_vl, TRV_bin_rl):
                return Lrbin_E / 1000 * ((TRV_bin_vl + TRV_bin_rl) / 2 - Temperatur) * 2 * pi * L_Erdreich * hs_RE

            # Berechnung von P_RVT_bin_vl und P_RVT_bin_rl
            P_RVT_bin_vl = calc_P_RVT_bin(TRV_bin_vl, TRV_bin_rl)
            P_RVT_bin_rl = calc_P_RVT_bin(TRV_bin_vl, TRV_bin_rl)

            # Berechnung von P_RVK_bin_vl und P_RVK_bin_rl
            if ziel_erhöht:
                P_RVK_bin_vl = max((TRV_bin_vl_alt - TRV_bin_vl) * VRV_bin * 3790 / 3600, 0)
                P_RVK_bin_rl = max((TRV_bin_rl_alt - TRV_bin_rl) * VRV_bin * 3790 / 3600, 0)
            else:
                P_RVK_bin_vl = 0
                P_RVK_bin_rl = 0

            # Verluste interne Rohrleitungen
            TRV_int_vl_alt = TRV_int_vl
            TRV_int_rl_alt = TRV_int_rl

            trv_int_vl_check = Tgkoll >= Zieltemperatur_Solaranlage and Pkoll > 0
            trv_int_rl_check = Tgkoll >= Zieltemperatur_Solaranlage and Pkoll > 0

            TRV_int_vl = Zieltemperatur_Solaranlage if trv_int_vl_check else Temperatur - (
                        Temperatur - TRV_int_vl) * exp(-KK / CKK)
            TRV_int_rl = TRL_Solar if trv_int_rl_check else Temperatur - (Temperatur - TRV_int_rl) * exp(-KK / CKK)

            P_RVT_int_vl = (TRV_int_vl - Temperatur) * KK * Bezugsfläche / 1000 / 2
            P_RVT_int_rl = (TRV_int_rl - Temperatur) * KK * Bezugsfläche / 1000 / 2

            if Zieltemperatur_Solaranlage < Zieltemperatur_Solaranlage_alt:
                P_RVK_int_vl = P_RVK_int_rl = 0
            else:
                P_RVK_int_vl = max((TRV_int_vl_alt - TRV_int_vl) * VRV * Bezugsfläche / 2 * 3790 / 3600, 0)
                P_RVK_int_rl = max((TRV_int_rl_alt - TRV_int_rl) * VRV * Bezugsfläche / 2 * 3790 / 3600, 0)

            PRV = max(P_RVT_bin_vl, P_RVK_bin_vl, 0) + max(P_RVT_int_vl, P_RVK_int_vl, 0) + max(P_RVT_bin_rl,
                                                                                                P_RVK_bin_rl, 0) + max(
                P_RVT_int_rl, P_RVK_int_rl, 0)  # Rohrleitungsverluste

            # Berechnung Kollektorfeldertrag
            if T_koll > Tgkoll_alt:
                if Tgkoll >= Zieltemperatur_Solaranlage:
                    value1 = (T_koll-Tgkoll)/(T_koll-Tgkoll_alt) * Pkoll
                else:
                    value1 = 0
                value2 = max(0, min(Pkoll, value1))

                if Stagnation <= 0:
                    value3 = 1
                else:
                    value3 = 0
                Kollektorfeldertrag = value2 * value3
            else:
                Kollektorfeldertrag = 0

            # Rohrleitungsverluste aufsummiert
            if (Kollektorfeldertrag == 0 and Kollektorfeldertrag_alt == 0) or Kollektorfeldertrag <= Summe_PRV_alt:
                Summe_PRV = PRV + Summe_PRV_alt - Kollektorfeldertrag
            else:
                Summe_PRV = PRV

            if Kollektorfeldertrag > Summe_PRV_alt:
                Zwischenwert = Kollektorfeldertrag - Summe_PRV_alt
            else:
                Zwischenwert = 0

            PSout = min(Zwischenwert + QS, Last) if Zwischenwert + QS > 0 else 0

            Zwischenwert_Stag_verl = max(0, QS - PSV + Zwischenwert - PSout - QSmax)

            Speicher_Wärmeinput_ohne_FS = Zwischenwert - Zwischenwert_Stag_verl
            PSin = Speicher_Wärmeinput_ohne_FS

            if QS - PSV + PSin - PSout > QSmax:
                QS = QSmax
            else:
                QS = QS - PSV + PSin - PSout

            # Berechnung Mitteltemperatur im Speicher
            value1 = QS/QSmax
            value2 = Zieltemperatur_Solaranlage - DT_WT_Solar
            if QS <= 0:
                ergebnis1 = value2
            else:
                value3 = (value2 - Tm_rl) / (Tsmax - Tm_rl)
                if value1 < value3:
                    ergebnis1 = VLT + DT_WT_Netz
                else:
                    ergebnis1 = Tsmax

            value4 = (1 - value1) * TS_unten
            Tms = value1 * ergebnis1 + value4

            PSV = 0.75 * (VS * 1000) ** 0.5 * 0.16 * (Tms - Temperatur) / 1000

            if Tag_des_Jahres == Tag_des_Jahres_alt:
                value1_stagnation = 0
                if Zwischenwert > Last and QS >= QSmax:
                    value1_stagnation = 1
                Stagnation = 1 if value1_stagnation + Stagnation > 0 else 0
            else:
                Stagnation = 0

            S_HFG = QS / QSmax  # Speicherfüllungsgrad

        Speicherladung_L.append(QS)
        Speicher_Wärmeoutput_L.append(PSout)
        Jahreswärmemenge += PSout / 1000

        Zähler += 1

    return Jahreswärmemenge, np.array(Speicher_Wärmeoutput_L)

# print(Berechnung_STA(600, 20, "Flachkollektor")[0], "Daten.csv")
# print(Berechnung_STA(600, 30, "Röhrenkollektor")[0], "Daten.csv")

# finanzielle Betrachtung
def WGK_STA(Bruttofläche_STA, VS, typ, filename):
    Jahreswärmemenge, Speicher_Wärmeoutput_L = Berechnung_STA(Bruttofläche_STA, VS, typ, filename)
    if Jahreswärmemenge == 0:
        return 0
    kosten_pro_typ = {
        "Flachkollektor": 440,
        "Vakuumröhrenkollektor": 650
    }
    Kosten_STA_spez = kosten_pro_typ[typ]  # €/m^2

    Kosten_Speicher_spez = 800  # €/m^3
    Anteil_Förderung_BEW = 0.4
    Eigenanteil = 1 - Anteil_Förderung_BEW
    Betriebskostenförderung = 10  # €/MWh 10 Jahre
    Betriebskostenförderung_Dauer = 10
    Nutzungsdauer = 20

    Investitionskosten_Speicher = VS * Kosten_Speicher_spez
    Investitionskosten_STA = Bruttofläche_STA * Kosten_STA_spez
    Investitionskosten_Gesamt = Investitionskosten_Speicher + Investitionskosten_STA
    Investitionskosten_Gesamt_BEW = Investitionskosten_Gesamt * Eigenanteil

    Betriebskosten_Jahr = Investitionskosten_Gesamt * 0.015
    Betriebskosten_Nutzungsdauer = Betriebskosten_Jahr * Nutzungsdauer

    # Inflationsrate = 2.33  # % - Mittelwert 2003 - 2023
    # Betriebskosten_Gesamt = np.sum(Betriebskosten_Jahr * np.power(1 + Inflationsrate / 100, np.arange(Nutzungsdauer)))
    # durchschnittliche_Betriebskosten_Jahr = Betriebskosten_Gesamt / Nutzungsdauer

    Gesamtkosten_Nutzungsdauer = Investitionskosten_Gesamt + Betriebskosten_Nutzungsdauer
    Gesamtkosten_Nutzungsdauer_BEW = Investitionskosten_Gesamt_BEW + Betriebskosten_Nutzungsdauer

    Betriebskostenförderung_Gesamt = Betriebskostenförderung * Betriebskostenförderung_Dauer * Jahreswärmemenge

    Wärmemenge_Nutzungsdauer = Jahreswärmemenge * Nutzungsdauer

    Wärmepreis = Gesamtkosten_Nutzungsdauer / Wärmemenge_Nutzungsdauer
    Wärmepreis_BEW = (Gesamtkosten_Nutzungsdauer_BEW - Betriebskostenförderung_Gesamt) / Wärmemenge_Nutzungsdauer

    return Wärmepreis

# print(WGK_STA(600, 20, "Flachkollektor"), "Daten.csv")
# print(WGK_STA(600, 30, "Röhrenkollektor"), "Daten.csv")

def Optimierung_WGK_STA(Typ, filename):
    results = [(WGK_STA(f, v, Typ, filename), f, v) for v in range(10, 100, 10) for f in range(100, 1000, 100)]
    min_WGK, optimum_Bruttofläche, optimum_VS = min(results)

    print("Die minimalen Wärmegestehungskosten der Solarthermieanlage betragen: " + str(min_WGK) + " €/MWh")
    print("Die Speichergröße beträgt: " + str(optimum_VS) + " m^3")
    print("Die Bruttokollektorfläche beträgt: " + str(optimum_Bruttofläche) + " m^2")

# Optimierung_WGK_STA("Flachkollektor", "Daten.csv")
# Optimierung_WGK_STA("Röhrenkollektor", "Daten.csv")
