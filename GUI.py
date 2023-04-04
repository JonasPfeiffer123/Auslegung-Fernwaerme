import tkinter as tk
from tkinter import ttk
from Berechnung_Fernwaerme import Berechnung_Erzeugermix
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def GUI():
    def submit():
        filename = combo.get()
        Bruttofläche_STA = float(entry1.get())
        VS = float(entry2.get())
        Typ = combo1.get()
        Fläche = float(entry3.get())
        Bohrtiefe = float(entry4.get())
        f_P_GK = float(entry5.get())
        Gaspreis = float(entry6.get())
        Strompreis = float(entry7.get())
        Holzpreis = float(entry8.get())
        el_Leistung_BHKW = float(entry9.get())

        tech_order = entry10.get().split(",")  # aus der Entry-Box auslesen und Liste erstellen

        WGK_Gesamt, Jahreswärmebedarf, Deckungsanteil, Last_L, data_L, data_labels_L, colors_L, Wärmemengen, WGK, Anteile = Berechnung_Erzeugermix(Bruttofläche_STA, VS, Typ, Fläche, Bohrtiefe, f_P_GK, Gaspreis, Strompreis,
                                     Holzpreis,filename, tech_order)

        zeile = 1
        label = tk.Label(root, text=f"Jahreswärmebedarf: {Jahreswärmebedarf:.2f} MWh")
        label.grid(row=zeile, column=3)
        zeile += 1
        for t, wärmemenge, anteil, wgk in zip(tech_order, Wärmemengen, Anteile, WGK):
            label_result = tk.Label(root, text="Wärmemenge " + str(t) + f": {wärmemenge:.2f} MWh")
            label_result.grid(row=zeile, column=3)
            zeile += 1
            label_result = tk.Label(root, text="Wärmegestehungskosten " + str(t) + f": {wgk:.2f} €/MWh")
            label_result.grid(row=zeile, column=3)
            zeile += 1
            label_result = tk.Label(root, text="Anteil an Wärmeversorgung " + str(t) + f": {anteil*100:.2f} %")
            label_result.grid(row=zeile, column=3)
            zeile += 1

        result_label.config(text=f"Wärmegestehungskosten: {WGK_Gesamt:.2f} €/MWh")

        # Diagramm erstellen
        fig, ax = plt.subplots()
        ax.plot(range(1, 8761), Last_L, color="black", linewidth=1, label="Last in kW")
        ax.stackplot(range(1, 8761), data_L, labels=data_labels_L, colors=colors_L)
        ax.set_title("Lastgang und Erzeugung Wärmenetz")
        ax.set_xlabel("Jahresstunden")
        ax.set_ylabel("thermische Leistung in kW")
        ax.legend(loc='upper center')

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=zeile, column=0, columnspan=3)

        # Erstelle das Kreisdiagramm
        pie, ax1 = plt.subplots()
        ax1.pie(Anteile, labels=data_labels_L, colors=colors_L, autopct='%1.1f%%', startangle=90)
        ax1.set_title("Anteile Wärmeerzeugung")
        ax1.legend(loc='upper right')
        ax1.axis("equal")
        canvas1 = FigureCanvasTkAgg(pie, master=root)
        canvas1.draw()
        canvas1.get_tk_widget().grid(row=zeile, column=3, columnspan=3)

    root = tk.Tk()
    root.title("Optimierung WGK")

    label_Daten = tk.Label(root, text="CSV-Dateiname mit den Daten")
    label_Daten.grid(row=0, column=0)
    combo = ttk.Combobox(root, values=["Daten.csv", "Daten Görlitz.csv", "Daten Görlitz Beleg.csv"])
    combo.current(0)
    combo.grid(row=0, column=1)

    label_Bruttofläche_STA = tk.Label(root, text="Bruttofläche Solarthermieanlage in m²")
    label_Bruttofläche_STA.grid(row=1, column=0)
    entry1 = tk.Entry(root)
    entry1.insert(0, "1000")
    entry1.grid(row=1, column=1)

    label_VS = tk.Label(root, text="Volumen Solarspeicher in m³")
    label_VS.grid(row=2, column=0)
    entry2 = tk.Entry(root)
    entry2.insert(0, "50")
    entry2.grid(row=2, column=1)

    label_Kollektortyp = tk.Label(root, text="Kollektortyp")
    label_Kollektortyp.grid(row=3, column=0)
    combo1 = ttk.Combobox(root, values=["Flachkollektor", "Vakuumröhrenkollektor"])
    combo1.current(0)
    combo1.grid(row=3, column=1)

    label_Fläche = tk.Label(root, text="Fläche Erdsondenfeld in m²")
    label_Fläche.grid(row=4, column=0)
    entry3 = tk.Entry(root)
    entry3.insert(0, "2000")
    entry3.grid(row=4, column=1)

    label_Bohrtiefe = tk.Label(root, text="Bohrtiefe Erdsonden in m")
    label_Bohrtiefe.grid(row=5, column=0)
    entry4 = tk.Entry(root)
    entry4.insert(0, "200")
    entry4.grid(row=5, column=1)

    label_f_P_GK = tk.Label(root, text="Einschaltpunkt Gaskessel als Anteil an Maximallast")
    label_f_P_GK.grid(row=6, column=0)
    entry5 = tk.Entry(root)
    entry5.insert(0, "0.5")
    entry5.grid(row=6, column=1)

    label_Gaspreis = tk.Label(root, text="Gaspreis in €/MWh")
    label_Gaspreis.grid(row=7, column=0)
    entry6 = tk.Entry(root)
    entry6.insert(0, "100")
    entry6.grid(row=7, column=1)

    label_Strompreis = tk.Label(root, text="Strompreis in €/MWh")
    label_Strompreis.grid(row=8, column=0)
    entry7 = tk.Entry(root)
    entry7.insert(0, "200")
    entry7.grid(row=8, column=1)

    label_Holzpreis = tk.Label(root, text="Holzpreis in €/MWh")
    label_Holzpreis.grid(row=9, column=0)
    entry8 = tk.Entry(root)
    entry8.insert(0, "50")
    entry8.grid(row=9, column=1)

    label_BHKW = tk.Label(root, text="elektrische Leistung BHKW")
    label_BHKW.grid(row=10, column=0)
    entry9 = tk.Entry(root)
    entry9.insert(0, "50")
    entry9.grid(row=10, column=1)

    label_order_a = tk.Label(root, text="verfügbar: Solarthermie, Abwasserwärme, "
                                       "Abwärme, Geothermie, Holzgas-BHKW, BHKW, Biomassekessel, Gaskessel")
    label_order_a.grid(row=11, column=0, columnspan=2)

    label_order = tk.Label(root, text="Reihenfolge Technologie")
    label_order.grid(row=12, column=0)
    entry10 = tk.Entry(root)
    entry10.insert(0, "Solarthermie,Geothermie,BHKW,Biomassekessel,Gaskessel")
    entry10.grid(row=12, column=1)

    submit_button = tk.Button(root, text="Berechne", command=submit)
    submit_button.grid(row=13, column=1)

    result_label = tk.Label(root, text="Wärmegestehungskosten Gesamt: Berechung notwendig!")
    result_label.grid(row=0, column=3)

    root.mainloop()

GUI()