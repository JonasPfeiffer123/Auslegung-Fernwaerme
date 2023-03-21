from Berechnung_Solarthermie import Berechnung_STA as STA1
from Solarthermie_improvement import Berechnung_STA as STA2
from Berechnung_Fernwaerme import Berechnung_Erzeugermix
import timeit

def compare_execution_times(func1, num_runs=1):
    func1_name = func1.__name__
    func1_time = timeit.timeit(func1, number=num_runs)

    print(f"{func1_name} Laufzeit: {func1_time:.6f} Sekunden")

if __name__ == "__main__":
    # Verwenden Sie eine Lambda-Funktion, um die Parameter für Ihre Funktionen festzulegen
    func1_with_args = lambda: Berechnung_Erzeugermix(600, 20, "Flachkollektor", 2000, 200, 0.5, 100, 200, 50, "Daten.csv", ["Solarthermie", "Geothermie", "BHKW", "Biomassekessel", "Gaskessel"], 80)
    compare_execution_times(func1_with_args)