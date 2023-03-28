import tkinter as tk
from tkinter import ttk
from Berechnung_Fernwaerme import Berechnung_Erzeugermix

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

        tech_order = ["Solarthermie", "Geothermie", "BHKW", "Biomassekessel", "Gaskessel"]

        result = Berechnung_Erzeugermix(Bruttofläche_STA, VS, Typ, Fläche, Bohrtiefe, f_P_GK, Gaspreis, Strompreis,
                                        Holzpreis, filename, tech_order)
        result_label.config(text=f"Wärmegestehungskosten: {result[0]:.2f}")

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

    submit_button = tk.Button(root, text="Berechne", command=submit)
    submit_button.grid(row=11, column=1)

    result_label = tk.Label(root, text="")
    result_label.grid(row=12, column=1)


    root.mainloop()

GUI()