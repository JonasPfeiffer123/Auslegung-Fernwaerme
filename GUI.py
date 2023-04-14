import tkinter as tk
from tkinter import ttk
from Berechnung_Fernwaerme import Berechnung_Erzeugermix
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def GUI():
    def submit(reihe):
        filename = combo.get()
        Bruttofläche_STA = float(entry1.get())
        VS = float(entry2.get())
        Typ = combo1.get()
        Fläche = float(entry3.get())
        Bohrtiefe = float(entry4.get())
        P_BMK = float(entry5.get())
        Gaspreis = float(entry6.get())
        Strompreis = float(entry7.get())
        Holzpreis = float(entry8.get())
        el_Leistung_BHKW = float(entry9.get())
        BEW = combo2.get()
        Kapitalzins = float(entry11.get())
        Preissteigerungsrate = float(entry12.get())
        Temperatur_Geothermie = float(entry13.get())
        Kühlleistung_Abwärme = float(entry14.get())
        Temperatur_Abwärme = float(entry15.get())
        Kühlleistung_AWW = float(entry16.get())
        Temperatur_AWW = float(entry17.get())

        tech_order = entry10.get().split(",")  # aus der Entry-Box auslesen und Liste erstellen

        WGK_Gesamt, Jahreswärmebedarf, Deckungsanteil, Last_L, data_L, data_labels_L, colors_L, Wärmemengen, WGK, \
            Anteile = Berechnung_Erzeugermix(Bruttofläche_STA, VS, Typ, Fläche, Bohrtiefe, Temperatur_Geothermie, P_BMK,
                                             Gaspreis, Strompreis, Holzpreis, filename, tech_order, BEW,
                                             el_Leistung_BHKW, Kühlleistung_Abwärme, Temperatur_Abwärme,
                                             Kühlleistung_AWW, Temperatur_AWW, Kapitalzins, Preissteigerungsrate)

        zeile = 1
        label = tk.Label(inner_frame, text=f"Jahreswärmebedarf:")
        label.grid(row=zeile, column=3, sticky="w")
        label = tk.Label(inner_frame, text=f"{Jahreswärmebedarf:.2f} MWh")
        label.grid(row=zeile, column=4, sticky="w")
        zeile += 1
        for t, wärmemenge, anteil, wgk in zip(tech_order, Wärmemengen, Anteile, WGK):
            label_result = tk.Label(inner_frame, text="Wärmemenge " + str(t) + ":")
            label_result.grid(row=zeile, column=3, sticky="w")
            label_result = tk.Label(inner_frame, text=f"{wärmemenge:.2f} MWh")
            label_result.grid(row=zeile, column=4, sticky="w")
            zeile += 1
            label_result = tk.Label(inner_frame, text="Wärmegestehungskosten " + str(t) + ":")
            label_result.grid(row=zeile, column=3, sticky="w")
            label_result = tk.Label(inner_frame, text=f"{wgk:.2f} €/MWh")
            label_result.grid(row=zeile, column=4, sticky="w")
            zeile += 1
            label_result = tk.Label(inner_frame, text="Anteil an Wärmeversorgung " + str(t) + ":")
            label_result.grid(row=zeile, column=3, sticky="w")
            label_result = tk.Label(inner_frame, text=f"{anteil:.2f}")
            label_result.grid(row=zeile, column=4, sticky="w")
            zeile += 1

        result_label2.config(text=f"{WGK_Gesamt:.2f} €/MWh")

        # Diagramm erstellen
        fig, ax = plt.subplots()

        ax.plot(range(1, 8761), Last_L, color="black", linewidth=0.5, label="Last in kW")
        ax.stackplot(range(1, 8761), data_L, labels=data_labels_L, colors=colors_L)
        ax.set_title("Lastgang und Erzeugung Wärmenetz")
        ax.set_xlabel("Jahresstunden")
        ax.set_ylabel("thermische Leistung in kW")
        ax.legend(loc='upper center')

        canvas = FigureCanvasTkAgg(fig, master=inner_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=reihe, column=0, columnspan=3)

        # Erstelle das Kreisdiagramm
        pie, ax1 = plt.subplots()
        ax1.pie(Anteile, labels=data_labels_L, colors=colors_L, autopct='%1.1f%%', startangle=90)
        ax1.set_title("Anteile Wärmeerzeugung")
        ax1.legend(loc='center right')
        ax1.axis("equal")
        canvas1 = FigureCanvasTkAgg(pie, master=inner_frame)
        canvas1.draw()
        canvas1.get_tk_widget().grid(row=reihe, column=3, columnspan=3)

    inner_frame = tk.Tk()
    inner_frame.geometry('1000x1000')
    inner_frame.title("Auslegung und wirtschaftliche Betrachtung von Wärmeerzeugern")

    main_frame = tk.Frame(inner_frame)
    main_frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(main_frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

    inner_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor='nw')

    überschrift = tk.font.Font(family="Helvetica", size=10, weight="bold")

    reihe = 0

    label_Daten = tk.Label(inner_frame, text="Dateneingabe Auslegung und Berechnung Wärmegestehungskosten", font=überschrift)
    label_Daten.grid(row=reihe, column=0, columnspan=2, sticky="w")
    reihe += 1

    label_Daten = tk.Label(inner_frame, text="CSV-Dateiname mit den Daten")
    label_Daten.grid(row=reihe, column=0)
    combo = ttk.Combobox(inner_frame, values=["Daten.csv", "Daten Görlitz.csv", "Daten Görlitz Beleg.csv"])
    combo.current(0)
    combo.grid(row=reihe, column=1)
    reihe += 1

    label_Daten = tk.Label(inner_frame, text="Betriebswirtschaftliche Rahmenbedingungen", font=überschrift)
    label_Daten.grid(row=reihe, column=0, columnspan=2, sticky="w")
    reihe += 1

    label_Gaspreis = tk.Label(inner_frame, text="Gaspreis in €/MWh")
    label_Gaspreis.grid(row=reihe, column=0)
    entry6 = tk.Entry(inner_frame)
    entry6.insert(0, "100")
    entry6.grid(row=reihe, column=1)
    reihe += 1

    label_Strompreis = tk.Label(inner_frame, text="Strompreis in €/MWh")
    label_Strompreis.grid(row=reihe, column=0)
    entry7 = tk.Entry(inner_frame)
    entry7.insert(0, "200")
    entry7.grid(row=reihe, column=1)
    reihe += 1

    label_Holzpreis = tk.Label(inner_frame, text="Holzpreis in €/MWh")
    label_Holzpreis.grid(row=reihe, column=0)
    entry8 = tk.Entry(inner_frame)
    entry8.insert(0, "50")
    entry8.grid(row=reihe, column=1)
    reihe += 1

    label_Kapitalzins = tk.Label(inner_frame, text="Kapitalzins in %")
    label_Kapitalzins.grid(row=reihe, column=0)
    entry11 = tk.Entry(inner_frame)
    entry11.insert(0, "5")
    entry11.grid(row=reihe, column=1)
    reihe += 1

    label_PSR = tk.Label(inner_frame, text="Preissteigerungsrate in %")
    label_PSR.grid(row=reihe, column=0)
    entry12 = tk.Entry(inner_frame)
    entry12.insert(0, "3")
    entry12.grid(row=reihe, column=1)
    reihe += 1

    label_BEW = tk.Label(inner_frame, text="Berücksichtigung Förderung nach BEW (Ja/Nein)")
    label_BEW.grid(row=reihe, column=0)
    combo2 = ttk.Combobox(inner_frame, values=["Nein", "Ja"])
    combo2.current(0)
    combo2.grid(row=reihe, column=1)
    reihe += 1

    label_Bruttofläche_STA = tk.Label(inner_frame, text="Anlagenspezifische Eingaben", font=überschrift)
    label_Bruttofläche_STA.grid(row=reihe, column=0, columnspan=2, sticky="w")
    reihe += 1

    label_Bruttofläche_STA = tk.Label(inner_frame, text="Eingaben Solarthermie", font=überschrift)
    label_Bruttofläche_STA.grid(row=reihe, column=0, columnspan=2, sticky="w")
    reihe += 1

    label_Bruttofläche_STA = tk.Label(inner_frame, text="Bruttofläche Solarthermieanlage in m²")
    label_Bruttofläche_STA.grid(row=reihe, column=0)
    entry1 = tk.Entry(inner_frame)
    entry1.insert(0, "1000")
    entry1.grid(row=reihe, column=1)
    reihe += 1

    label_VS = tk.Label(inner_frame, text="Volumen Solarspeicher in m³")
    label_VS.grid(row=reihe, column=0)
    entry2 = tk.Entry(inner_frame)
    entry2.insert(0, "50")
    entry2.grid(row=reihe, column=1)
    reihe += 1

    label_Kollektortyp = tk.Label(inner_frame, text="Kollektortyp")
    label_Kollektortyp.grid(row=reihe, column=0)
    combo1 = ttk.Combobox(inner_frame, values=["Flachkollektor", "Vakuumröhrenkollektor"])
    combo1.current(0)
    combo1.grid(row=reihe, column=1)
    reihe += 1

    label_Bruttofläche_STA = tk.Label(inner_frame, text="Eingaben Erdwärme", font=überschrift)
    label_Bruttofläche_STA.grid(row=reihe, column=0, columnspan=2, sticky="w")
    reihe += 1

    label_Fläche = tk.Label(inner_frame, text="Fläche Erdsondenfeld in m²")
    label_Fläche.grid(row=reihe, column=0)
    entry3 = tk.Entry(inner_frame)
    entry3.insert(0, "2000")
    entry3.grid(row=reihe, column=1)
    reihe += 1

    label_Bohrtiefe = tk.Label(inner_frame, text="Bohrtiefe Erdsonden in m")
    label_Bohrtiefe.grid(row=reihe, column=0)
    entry4 = tk.Entry(inner_frame)
    entry4.insert(0, "200")
    entry4.grid(row=reihe, column=1)
    reihe += 1

    label_Temperatur_ES = tk.Label(inner_frame, text="Quelltemperatur Erdsonden")
    label_Temperatur_ES.grid(row=reihe, column=0)
    entry13 = tk.Entry(inner_frame)
    entry13.insert(0, "15")
    entry13.grid(row=reihe, column=1)
    reihe += 1

    label_Bruttofläche_STA = tk.Label(inner_frame, text="Eingaben Abwärme", font=überschrift)
    label_Bruttofläche_STA.grid(row=reihe, column=0, columnspan=2, sticky="w")
    reihe += 1

    label_Kühlleistung_AW = tk.Label(inner_frame, text="Kühlleistung Abwärme")
    label_Kühlleistung_AW.grid(row=reihe, column=0)
    entry14 = tk.Entry(inner_frame)
    entry14.insert(0, "10")
    entry14.grid(row=reihe, column=1)
    reihe += 1

    label_Temperatur_AW = tk.Label(inner_frame, text="Quelltemperatur Abwärme")
    label_Temperatur_AW.grid(row=reihe, column=0)
    entry15 = tk.Entry(inner_frame)
    entry15.insert(0, "30")
    entry15.grid(row=reihe, column=1)
    reihe += 1

    label_Eingabe_AWW = tk.Label(inner_frame, text="Eingaben Abwasserwärme", font=überschrift)
    label_Eingabe_AWW.grid(row=reihe, column=0, columnspan=2, sticky="w")
    reihe += 1

    label_Kühlleistung_AWW = tk.Label(inner_frame, text="Kühlleistung Abwasserwärme")
    label_Kühlleistung_AWW.grid(row=reihe, column=0)
    entry16 = tk.Entry(inner_frame)
    entry16.insert(0, "30")
    entry16.grid(row=reihe, column=1)
    reihe += 1

    label_Temperatur_AWW = tk.Label(inner_frame, text="Quelltemperatur Abwasserwärme")
    label_Temperatur_AWW.grid(row=reihe, column=0)
    entry17 = tk.Entry(inner_frame)
    entry17.insert(0, "20")
    entry17.grid(row=reihe, column=1)
    reihe += 1

    label_Eingabe_BMK = tk.Label(inner_frame, text="Eingaben Biomassekessel", font=überschrift)
    label_Eingabe_BMK.grid(row=reihe, column=0, columnspan=2, sticky="w")
    reihe += 1

    label_P_BMK = tk.Label(inner_frame, text="thermische Leistung Biomassekessel")
    label_P_BMK.grid(row=reihe, column=0)
    entry5 = tk.Entry(inner_frame)
    entry5.insert(0, "200")
    entry5.grid(row=reihe, column=1)
    reihe += 1

    label_Eingabe_BHKW = tk.Label(inner_frame, text="Eingaben BHKW", font=überschrift)
    label_Eingabe_BHKW.grid(row=reihe, column=0, columnspan=2, sticky="w")
    reihe += 1

    label_BHKW = tk.Label(inner_frame, text="elektrische Leistung BHKW")
    label_BHKW.grid(row=reihe, column=0)
    entry9 = tk.Entry(inner_frame)
    entry9.insert(0, "50")
    entry9.grid(row=reihe, column=1)
    reihe += 1

    label_Eingabe_Anlagen = tk.Label(inner_frame, text="Eingaben Anlagen", font=überschrift)
    label_Eingabe_Anlagen.grid(row=reihe, column=0, columnspan=2, sticky="w")
    reihe += 1

    label_order_a = tk.Label(inner_frame, text="verfügbar: Solarthermie, Abwasserwärme, Abwärme, Geothermie, "
                                               "Holzgas-BHKW, BHKW, Biomassekessel, Gaskessel")
    label_order_a.grid(row=reihe, column=0, columnspan=2)
    reihe += 1

    label_order = tk.Label(inner_frame, text="Reihenfolge Technologie")
    label_order.grid(row=reihe, column=0)
    entry10 = tk.Entry(inner_frame, width=75)
    entry10.insert(0, "Solarthermie,Geothermie,BHKW,Biomassekessel,Gaskessel")
    entry10.grid(row=reihe, column=1)
    reihe += 1

    submit_button = tk.Button(inner_frame, text="Berechne", command=lambda: submit(reihe))
    submit_button.grid(row=reihe, column=1)
    reihe += 1

    result_label = tk.Label(inner_frame, text="Wärmegestehungskosten Gesamt:")
    result_label.grid(row=0, column=3, sticky="w")
    result_label2 = tk.Label(inner_frame, text="Berechnung notwendig!")
    result_label2.grid(row=0, column=4, sticky="w")

    inner_frame.mainloop()

GUI()

