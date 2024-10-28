import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class PersonalityWindow:
    def __init__(self, root ,personality_traits):
        # open window and get data
        self.root = root
        self.personality_traits = personality_traits

        # call chart function
        self.show_personality_chart()

    # create charts +
    def show_personality_chart(self):
        # popup windwos
        popup = tk.Toplevel(self.root, bg="#f4f1de")  # Verwende das root-Objekt der Klasse
        popup.title("Persönlichkeitsmerkmale Auswertung")
        popup.geometry("900x800")

        # create dimension chart, get data
        dimensionen_keys = list(self.personality_traits["dimensionen"].keys())
        dimensionen_values = list(self.personality_traits["dimensionen"].values())

        # colours for dimensions
        dimension_colors = {
            "Extraversion": "#023047",
            "Verträglichkeit": "#ffb703",
            "Gewissenhaftigkeit": "#219ebc",
            "Negative Emotionalität": "#fb8500",
            "Offenheit": "#8ecae6"
        }

        # formate chart
        fig, axes = plt.subplots(2, 1, figsize=(8, 10))

        # draw chart
        axes[0].barh(dimensionen_keys, dimensionen_values, color=[dimension_colors[dimension] for dimension in dimensionen_keys])
        axes[0].set_xlim(0, 100)
        axes[0].set_title("Ausprägungen Dimensionen")
        axes[0].set_xlabel("Prozent")

        # create facettte chart
        facetten_keys = list(self.personality_traits["facetten"].keys())
        facetten_values = list(self.personality_traits["facetten"].values())

        # get same colours for facette as their dimensions
        facetten_colors = [
            dimension_colors["Extraversion"], dimension_colors["Extraversion"], dimension_colors["Extraversion"],
            dimension_colors["Verträglichkeit"], dimension_colors["Verträglichkeit"],
            dimension_colors["Verträglichkeit"],
            dimension_colors["Gewissenhaftigkeit"], dimension_colors["Gewissenhaftigkeit"],
            dimension_colors["Gewissenhaftigkeit"],
            dimension_colors["Negative Emotionalität"], dimension_colors["Negative Emotionalität"],
            dimension_colors["Negative Emotionalität"],
            dimension_colors["Offenheit"], dimension_colors["Offenheit"], dimension_colors["Offenheit"]
        ]

        # draw chart
        axes[1].barh(facetten_keys, facetten_values, color=facetten_colors)
        axes[1].set_xlim(0, 100)
        axes[1].set_title("Ausprägungen Facetten")
        axes[1].set_xlabel("Prozent")

        # increase space between charts
        plt.subplots_adjust(hspace=1)
        plt.tight_layout()

        # get chart in tkinter windows
        canvas = FigureCanvasTkAgg(fig, master=popup)
        canvas.draw()
        canvas.get_tk_widget().pack()