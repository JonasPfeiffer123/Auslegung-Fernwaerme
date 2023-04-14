import matplotlib.pyplot as plt

Typtage = ["ÜWH", "ÜWB", "ÜSH", "ÜSB", "SWX", "SSX", "WWH", "WWB", "WSH", "WSB"]

TRY = {"Bestandsgebäude": {"TRY9": {"ÜWH": {"Anzahl Tage": 55, "mittlere Außentemperatur": 11.1, "F_Heiz_TT": 0.0018758, "F_TWE_TT": 0.000012185},
                                    "ÜWB": {"Anzahl Tage": 64, "mittlere Außentemperatur": 10.5, "F_Heiz_TT": 0.0021459, "F_TWE_TT": 0.0000032642},
                                    "ÜSH": {"Anzahl Tage": 8, "mittlere Außentemperatur": 10.2, "F_Heiz_TT": 0.0019351, "F_TWE_TT": 0.0000032642},
                                    "ÜSB": {"Anzahl Tage": 18, "mittlere Außentemperatur": 9.6, "F_Heiz_TT": 0.0020129, "F_TWE_TT": 0.000016150},
                                    "SWX": {"Anzahl Tage": 71, "mittlere Außentemperatur": 17.7, "F_Heiz_TT": 0.00021418, "F_TWE_TT": -0.000054225},
                                    "SSX": {"Anzahl Tage": 16, "mittlere Außentemperatur": 17.2, "F_Heiz_TT": 0.00025124, "F_TWE_TT": -0.000045304},
                                    "WWH": {"Anzahl Tage": 28, "mittlere Außentemperatur": 0.6, "F_Heiz_TT": 0.0056018, "F_TWE_TT": 0.000028044},
                                    "WWB": {"Anzahl Tage": 84, "mittlere Außentemperatur": 1.3, "F_Heiz_TT": 0.0051558, "F_TWE_TT": 0.000027053},
                                    "WSH": {"Anzahl Tage": 4, "mittlere Außentemperatur": -0.1, "F_Heiz_TT": 0.0059297, "F_TWE_TT": 0.000020115},
                                    "WSB": {"Anzahl Tage": 17, "mittlere Außentemperatur": 1.6, "F_Heiz_TT": 0.0044059, "F_TWE_TT": 0.000014167}},
                                    "Heiztage": 278},
       "Niedrigenergiehaus": {"TRY9": {"ÜWH": {"Anzahl Tage": 29, "mittlere Außentemperatur": 9.0},
                                    "ÜWB": {"Anzahl Tage": 41, "mittlere Außentemperatur": 8.5},
                                    "ÜSH": {"Anzahl Tage": 7, "mittlere Außentemperatur": 9.9},
                                    "ÜSB": {"Anzahl Tage": 13, "mittlere Außentemperatur": 8.0},
                                    "SWX": {"Anzahl Tage": 120, "mittlere Außentemperatur": 16.1},
                                    "SSX": {"Anzahl Tage": 22, "mittlere Außentemperatur": 16.2},
                                    "WWH": {"Anzahl Tage": 28, "mittlere Außentemperatur": 0.6},
                                    "WWB": {"Anzahl Tage": 84, "mittlere Außentemperatur": 1.3},
                                    "WSH": {"Anzahl Tage": 4, "mittlere Außentemperatur": -0.1},
                                    "WSB": {"Anzahl Tage": 17, "mittlere Außentemperatur": 1.6}},
                                    "Heiztage": 223}}

# Zapfprofile in %
Zapfprofile_TWE = {"Einfamilienhäuser": [1.8, 1, 0.6, 0.3, 0.4, 0.6, 2.4, 4.7, 6.8, 5.7, 6.1, 6.1, 6.3, 6.4, 5.1, 4.4,
                                         4.3, 4.7, 5.7, 6.5, 6.6, 5.8, 4.5, 3.1],
                   "Wohnungen": [1, 1, 1, 0, 0, 1, 3, 6, 8, 6, 5, 5, 6, 6, 5, 4, 4, 5, 6, 7, 7, 6, 5, 2]}

# Ermittlung Tagesenergiebedarfe
# Jahreswärmebedarfe
MFH1 = 579700  # kWh
MFH2 = 547320  # kWh
MFH3 = 357550  # kWh

# MFH1 = MFH1/4  # kWh
# MFH2 = MFH2/4  # kWh
# MFH3 = MFH3/4  # kWh

N_Pers_WE = 2

MFHges = MFH1 + MFH2 + MFH3
Anteil_WW = 0.15

Q_Heiz_a = MFHges * (1-Anteil_WW)  # Jahresheizwärmebedarf in kWh
Q_TWE_a = MFHges * Anteil_WW  # Jahrestrinkwarmwasserbedarf in kWh

Jahresdauerlinie_Q_Heiz_TT = []
Jahresdauerlinie_Q_TWE_TT = []
Jahresdauerlinie_Q_TWE_TT_ZP = []
Jahresdauerlinie = []
Jahresdauerlinie_ZP = []

for i in Typtage:
    Q_Heiz_TT = Q_Heiz_a * TRY["Bestandsgebäude"]["TRY9"][i]["F_Heiz_TT"]  # Heizwärmebedarf an einem bestimmten Typtag
    Q_TWE_TT = Q_TWE_a * (1 / 365 + N_Pers_WE * TRY["Bestandsgebäude"]["TRY9"][i]["F_TWE_TT"])
    print(i + ":", "Tagesheizwärmebedarf:", round(Q_Heiz_TT, 2), "kWh", "Tageswarmwasserbedarf:", round(Q_TWE_TT, 2), "kWh")

    for t in range(TRY["Bestandsgebäude"]["TRY9"][i]["Anzahl Tage"]):
        for h, p in zip(range(24), Zapfprofile_TWE["Wohnungen"]):
            Jahresdauerlinie_Q_Heiz_TT.append(Q_Heiz_TT/24)
            Jahresdauerlinie_Q_TWE_TT.append(Q_TWE_TT/24)
            Jahresdauerlinie_Q_TWE_TT_ZP.append(Q_TWE_TT*(p/100))
            Jahresdauerlinie.append(Q_Heiz_TT/24+Q_TWE_TT/24)
            Jahresdauerlinie_ZP.append(Q_Heiz_TT/24+Q_TWE_TT*(p/100))

Jahresdauerlinie_Q_Heiz_TT.sort(reverse=True)
Jahresdauerlinie_Q_TWE_TT.sort(reverse=True)
Jahresdauerlinie_Q_TWE_TT_ZP.sort(reverse=True)
Jahresdauerlinie.sort(reverse=True)
Jahresdauerlinie_ZP.sort(reverse=True)

print(len(Jahresdauerlinie))

plt.plot(range(len(Jahresdauerlinie_Q_Heiz_TT)), Jahresdauerlinie_Q_Heiz_TT)
plt.plot(range(len(Jahresdauerlinie_Q_TWE_TT)), Jahresdauerlinie_Q_TWE_TT)
#plt.plot(range(len(Jahresdauerlinie_Q_TWE_TT_ZP)), Jahresdauerlinie_Q_TWE_TT_ZP)
plt.plot(range(len(Jahresdauerlinie)), Jahresdauerlinie)
#plt.plot(range(len(Jahresdauerlinie_ZP)), Jahresdauerlinie_ZP)
plt.show()


# W_a = 4000  # Jahresstrombedarf in kWh
# W_TT = W_a*(1/365+N_Pers_WE*F_el_TT)  # Strombedarf an einem bestimmten Typtag
