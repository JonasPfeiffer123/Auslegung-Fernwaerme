import tkinter as tk
from customtkinter import CTkSlider as ctkSlider
from tkinter import ttk
from Berechnung_Fernwaerme import Berechnung_Erzeugermix

def GUI():
    def submit():
        filename = combo.get()
        Bruttofläche_STA = float(slider1.get())
        VS = float(slider2.get())
        Typ = combo1.get()
        Fläche = float(slider3.get())
        Bohrtiefe = float(slider4.get())
        f_P_GK = float(slider5.get())
        Gaspreis = float(slider6.get())
        Strompreis = float(slider7.get())
        Holzpreis = float(slider8.get())
        el_Leistung_BHKW = float(slider9.get())

        tech_order = ["Solarthermie", "Geothermie", "BHKW", "Biomassekessel", "Gaskessel"]

        result = Berechnung_Erzeugermix(Bruttofläche_STA, VS, Typ, Fläche, Bohrtiefe, f_P_GK, Gaspreis, Strompreis,
                                        Holzpreis, filename, tech_order, el_Leistung_BHKW)
        result_label.config(text=f"Wärmegestehungskosten: {result:.2f}")

    def update_label(*args):
        label1.config(text=str(var1.get()))
        label2.config(text=str(var2.get()))
        label3.config(text=str(var3.get()))
        label4.config(text=str(var4.get()))
        label5.config(text=str(var5.get()))
        label6.config(text=str(var6.get()))
        label7.config(text=str(var7.get()))
        label8.config(text=str(var8.get()))
        label9.config(text=str(var9.get()))

    root = tk.Tk()
    root.title("Optimierung WGK")

    var1 = tk.DoubleVar(root)
    var2 = tk.DoubleVar(root)
    var3 = tk.DoubleVar(root)
    var4 = tk.DoubleVar(root)
    var5 = tk.DoubleVar(root)
    var6 = tk.DoubleVar(root)
    var7 = tk.DoubleVar(root)
    var8 = tk.DoubleVar(root)
    var9 = tk.DoubleVar(root)

    var1.set(1000)
    var2.set(50)
    var3.set(2000)
    var4.set(200)
    var5.set(0.5)
    var6.set(100)
    var7.set(300)
    var8.set(75)
    var9.set(40)

    var1.trace("w", update_label)
    var2.trace("w", update_label)
    var3.trace("w", update_label)
    var4.trace("w", update_label)
    var5.trace("w", update_label)
    var6.trace("w", update_label)
    var7.trace("w", update_label)
    var8.trace("w", update_label)
    var9.trace("w", update_label)

    label_Daten = tk.Label(root, text="CSV-Dateiname mit den Daten")
    label_Daten.pack()
    combo = ttk.Combobox(root, values=["Daten.csv"])
    combo.pack()

    label_Bruttofläche_STA = tk.Label(root, text="Bruttofläche Solarthermieanlage in m²")
    label_Bruttofläche_STA.pack()
    slider1 = ctkSlider(root, from_=0, to=2000, variable=var1)
    slider1.pack()
    label1 = tk.Label(root, text="")
    label1.pack()

    label_VS = tk.Label(root, text="Volumen Solarspeicher in m³")
    label_VS.pack()
    slider2 = ctkSlider(root, from_=0, to=100, variable=var2)
    slider2.pack()
    label2 = tk.Label(root, text="")
    label2.pack()

    label_Kollektortyp = tk.Label(root, text="Kollektortyp")
    label_Kollektortyp.pack()
    combo1 = ttk.Combobox(root, values=["Flachkollektor", "Vakuumröhrenkollektor"])
    combo1.pack()

    label_Fläche = tk.Label(root, text="Fläche Erdsondenfeld in m²")
    label_Fläche.pack()
    slider3 = ctkSlider(root, from_=0, to=5000, variable=var3)
    slider3.pack()
    label3 = tk.Label(root, text="")
    label3.pack()

    label_Bohrtiefe = tk.Label(root, text="Bohrtiefe Erdsonden in m")
    label_Bohrtiefe.pack()
    slider4 = ctkSlider(root, from_=0, to=400, variable=var4)
    slider4.pack()
    label4 = tk.Label(root, text="")
    label4.pack()

    label_f_P_GK = tk.Label(root, text="Einschaltpunkt Gaskessel als Anteil an Maximallast")
    label_f_P_GK.pack()
    slider5 = ctkSlider(root, from_=0, to=1, variable=var5)
    slider5.pack()
    label5 = tk.Label(root, text="")
    label5.pack()

    label_Gaspreis = tk.Label(root, text="Gaspreis in €/MWh")
    label_Gaspreis.pack()
    slider6 = ctkSlider(root, from_=0, to=500, variable=var6)
    slider6.pack()
    label6 = tk.Label(root, text="")
    label6.pack()

    label_Strompreis = tk.Label(root, text="Strompreis in €/MWh")
    label_Strompreis.pack()
    slider7 = ctkSlider(root, from_=0, to=1000, variable=var7)
    slider7.pack()
    label7 = tk.Label(root, text="")
    label7.pack()

    label_Holzpreis = tk.Label(root, text="Holzpreis in €/MWh")
    label_Holzpreis.pack()
    slider8 = ctkSlider(root, from_=0, to=300, variable=var8)
    slider8.pack()
    label8 = tk.Label(root, text="")
    label8.pack()

    label_BHKW = tk.Label(root, text="elektrische Leistung BHKW")
    label_BHKW.pack()
    slider9 = ctkSlider(root, from_=0, to=1000, variable=var9)
    slider9.pack()
    label9 = tk.Label(root, text="")
    label9.pack()

    submit_button = tk.Button(root, text="Berechne", command=submit)
    submit_button.pack()

    result_label = tk.Label(root, text="")
    result_label.pack()

    root.mainloop()

GUI()