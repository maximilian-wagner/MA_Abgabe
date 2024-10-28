import tkinter as tk
from tkinter import messagebox


# Klasse für den Fragebogen
class QuestionWindow:
    def __init__(self, root, saved_answers=None):
        # formate window
        self.popup = tk.Toplevel(root, bg="#f4f1de")
        self.popup.title("Perönlichkeitsfragebogen")
        self.popup.geometry("1200x400")

        # mechanism so that it is still saved when closing :)
        self.popup.protocol("WM_DELETE_WINDOW", self.on_closing)

        # formate grid
        # formate columns
        for col in range(8):
            # alle gleich groß
            self.popup.grid_columnconfigure(col, weight=1)

        # formate rows
        self.popup.grid_rowconfigure(0, weight=1)  # Frage
        self.popup.grid_rowconfigure(1, weight=1)  # Skala
        self.popup.grid_rowconfigure(2, weight=1)  # Beschriftungen
        self.popup.grid_rowconfigure(3, weight=1)  # Zähler
        self.popup.grid_rowconfigure(4, weight=1)  # Weiter, Zurück
        self.popup.grid_rowconfigure(5, weight=1)  # Speichern

        # dict for questions
        self.fragen_liste = {}
        # JSON des B5I
        big_five_inventory = [
            {
                "Nummer": 1,
                "Frage": "Ich gehe aus mir heraus, bin gesellig.",
                "Einstufung": "",
                "Dimension": "Extraversion",
                "Dimension R-Schlüssel": "Nein",
                "Facette": "Geselligkeit",
                "Facetten R-Schlüssel": "Nein"
            },
            {
                "Nummer": 2,
                "Frage": "Ich bin einfühlsam, warmherzig.",
                "Einstufung": "",
                "Dimension": "Verträglichkeit",
                "Dimension R-Schlüssel": "Nein",
                "Facette": "Mitgefühl",
                "Facetten R-Schlüssel": "Nein"
            },
            {
                "Nummer": 3,
                "Frage": "Ich bin eher unordentlich.",
                "Einstufung": "",
                "Dimension": "Gewissenhaftigkeit",
                "Dimension R-Schlüssel": "Ja",
                "Facette": "Ordnungsliebe",
                "Facetten R-Schlüssel": "Ja"
            },
            {
                "Nummer": 4,
                "Frage": "Ich bleibe auch in stressigen Situationen gelassen.",
                "Einstufung": "",
                "Dimension": "Negative Emotionalität",
                "Dimension R-Schlüssel": "Ja",
                "Facette": "Ängstlichkeit",
                "Facetten R-Schlüssel": "Ja"
            },
            {
                "Nummer": 5,
                "Frage": "Ich bin nicht sonderlich kunstinteressiert.",
                "Einstufung": "",
                "Dimension": "Offenheit",
                "Dimension R-Schlüssel": "Ja",
                "Facette": "Ästhetisches Empfinden",
                "Facetten R-Schlüssel": "Ja"
            },
            {
                "Nummer": 6,
                "Frage": "Ich bin durchsetzungsfähig, energisch.",
                "Einstufung": "",
                "Dimension": "Extraversion",
                "Dimension R-Schlüssel": "Nein",
                "Facette": "Durchsetzungsfähigkeit",
                "Facetten R-Schlüssel": "Nein"
            },
            {
                "Nummer": 7,
                "Frage": "Ich begegne anderen mit Respekt.",
                "Einstufung": "",
                "Dimension": "Verträglichkeit",
                "Dimension R-Schlüssel": "Nein",
                "Facette": "Höflichkeit",
                "Facetten R-Schlüssel": "Nein"
            },
            {
                "Nummer": 8,
                "Frage": "Ich bin bequem, neige zu Faulheit.",
                "Einstufung": "",
                "Dimension": "Gewissenhaftigkeit",
                "Dimension R-Schlüssel": "Ja",
                "Facette": "Fleiß",
                "Facetten R-Schlüssel": "Ja"
            },
            {
                "Nummer": 9,
                "Frage": "Ich bleibe auch bei Rückschlägen zuversichtlich.",
                "Einstufung": "",
                "Dimension": "Negative Emotionalität",
                "Dimension R-Schlüssel": "Ja",
                "Facette": "Niedergeschlagenheit",
                "Facetten R-Schlüssel": "Ja"
            },
            {
                "Nummer": 10,
                "Frage": "Ich bin vielseitig interessiert.",
                "Einstufung": "",
                "Dimension": "Offenheit",
                "Dimension R-Schlüssel": "Nein",
                "Facette": "Intellektuelle Neugierde",
                "Facetten R-Schlüssel": "Nein"
            },
            {
                "Nummer": 11,
                "Frage": "Ich schäume selten vor Begeisterung über.",
                "Einstufung": "",
                "Dimension": "Extraversion",
                "Dimension R-Schlüssel": "Ja",
                "Facette": "Aktivität",
                "Facetten R-Schlüssel": "Ja"
            },
            {
                "Nummer": 12,
                "Frage": "Ich neige dazu, andere zu kritisieren.",
                "Einstufung": "",
                "Dimension": "Verträglichkeit",
                "Dimension R-Schlüssel": "Ja",
                "Facette": "Zwischenmenschliches Vertrauen",
                "Facetten R-Schlüssel": "Ja"
            },
            {
                "Nummer": 13,
                "Frage": "Ich bin stetig, beständig.",
                "Einstufung": "",
                "Dimension": "Gewissenhaftigkeit",
                "Dimension R-Schlüssel": "Nein",
                "Facette": "Verlässlichkeit",
                "Facetten R-Schlüssel": "Nein"
            },
            {
                "Nummer": 14,
                "Frage": "Ich kann launisch sein, habe schwankende Stimmungen.",
                "Einstufung": "",
                "Dimension": "Negative Emotionalität",
                "Dimension R-Schlüssel": "Nein",
                "Facette": "Unbeständigkeit der Gefühle",
                "Facetten R-Schlüssel": "Nein"
            },
            {
                "Nummer": 15,
                "Frage": "Ich bin erfinderisch, mir fallen raffinierte Lösungen ein.",
                "Einstufung": "",
                "Dimension": "Offenheit",
                "Dimension R-Schlüssel": "Nein",
                "Facette": "Kreativer Einfallsreichtum",
                "Facetten R-Schlüssel": "Nein"
            },
            {
                "Nummer": 16,
                "Frage": "Ich bin eher ruhig.",
                "Einstufung": "",
                "Dimension": "Extraversion",
                "Dimension R-Schlüssel": "Ja",
                "Facette": "Geselligkeit",
                "Facetten R-Schlüssel": "Ja"
            },
            {
                "Nummer": 17,
                "Frage": "Ich habe mit anderen wenig Mitgefühl.",
                "Einstufung": "",
                "Dimension": "Verträglichkeit",
                "Dimension R-Schlüssel": "Ja",
                "Facette": "Mitgefühl",
                "Facetten R-Schlüssel": "Ja"
            },
            {
                "Nummer": 18,
                "Frage": "Ich bin systematisch, halte meine Sachen in Ordnung.",
                "Einstufung": "",
                "Dimension": "Gewissenhaftigkeit",
                "Dimension R-Schlüssel": "Nein",
                "Facette": "Ordnungsliebe",
                "Facetten R-Schlüssel": "Nein"
            },
            {
                "Nummer": 19,
                "Frage": "Ich reagiere leicht angespannt.",
                "Einstufung": "",
                "Dimension": "Negative Emotionalität",
                "Dimension R-Schlüssel": "Nein",
                "Facette": "Ängstlichkeit",
                "Facetten R-Schlüssel": "Nein"
            },
            {
                "Nummer": 20,
                "Frage": "Ich kann mich für Kunst, Musik und Literatur begeistern.",
                "Einstufung": "",
                "Dimension": "Offenheit",
                "Dimension R-Schlüssel": "Nein",
                "Facette": "Ästhetisches Empfinden",
                "Facetten R-Schlüssel": "Nein"
            },
            {
                "Nummer": 21,
                "Frage": "Ich neige dazu, die Führung zu übernehmen.",
                "Einstufung": "",
                "Dimension": "Extraversion",
                "Dimension R-Schlüssel": "Nein",
                "Facette": "Durchsetzungsfähigkeit",
                "Facetten R-Schlüssel": "Nein"
            },
            {
                "Nummer": 22,
                "Frage": "Ich habe oft Streit mit anderen.",
                "Einstufung": "",
                "Dimension": "Verträglichkeit",
                "Dimension R-Schlüssel": "Ja",
                "Facette": "Höflichkeit",
                "Facetten R-Schlüssel": "Ja"
            },
            {
                "Nummer": 23,
                "Frage": "Ich neige dazu, Aufgaben vor mir herzuschieben.",
                "Einstufung": "",
                "Dimension": "Gewissenhaftigkeit",
                "Dimension R-Schlüssel": "Ja",
                "Facette": "Fleiß",
                "Facetten R-Schlüssel": "Ja"
            },
            {
                "Nummer": 24,
                "Frage": "Ich bin selbstsicher, mit mir zufrieden.",
                "Einstufung": "",
                "Dimension": "Negative Emotionalität",
                "Dimension R-Schlüssel": "Ja",
                "Facette": "Niedergeschlagenheit",
                "Facetten R-Schlüssel": "Ja"
            },
            {
                "Nummer": 25,
                "Frage": "Ich meide philosophische Diskussionen.",
                "Einstufung": "",
                "Dimension": "Offenheit",
                "Dimension R-Schlüssel": "Ja",
                "Facette": "Intellektuelle Neugierde",
                "Facetten R-Schlüssel": "Ja"
            },
            {
                "Nummer": 26,
                "Frage": "Ich bin weniger aktiv und unternehmungslustig als andere.",
                "Einstufung": "",
                "Dimension": "Extraversion",
                "Dimension R-Schlüssel": "Ja",
                "Facette": "Aktivität",
                "Facetten R-Schlüssel": "Ja"
            },
            {
                "Nummer": 27,
                "Frage": "Ich bin nachsichtig, vergebe anderen leicht.",
                "Einstufung": "",
                "Dimension": "Verträglichkeit",
                "Dimension R-Schlüssel": "Nein",
                "Facette": "Zwischenmenschliches Vertrauen",
                "Facetten R-Schlüssel": "Nein"
            },
            {
                "Nummer": 28,
                "Frage": "Ich bin manchmal ziemlich nachlässig.",
                "Einstufung": "",
                "Dimension": "Gewissenhaftigkeit",
                "Dimension R-Schlüssel": "Ja",
                "Facette": "Verlässlichkeit",
                "Facetten R-Schlüssel": "Ja"
            },
            {
                "Nummer": 29,
                "Frage": "Ich bin ausgeglichen, nicht leicht aus der Ruhe zu bringen.",
                "Einstufung": "",
                "Dimension": "Negative Emotionalität",
                "Dimension R-Schlüssel": "Ja",
                "Facette": "Unbeständigkeit der Gefühle",
                "Facetten R-Schlüssel": "Ja"
            },
            {
                "Nummer": 30,
                "Frage": "Ich bin nicht besonders einfallsreich.",
                "Einstufung": "",
                "Dimension": "Offenheit",
                "Dimension R-Schlüssel": "Ja",
                "Facette": "Kreativer Einfallsreichtum",
                "Facetten R-Schlüssel": "Ja"
            },
            {
                "Nummer": 31,
                "Frage": "Ich bin eher schüchtern.",
                "Einstufung": "",
                "Dimension": "Extraversion",
                "Dimension R-Schlüssel": "Ja",
                "Facette": "Geselligkeit",
                "Facetten R-Schlüssel": "Ja"
            },
            {
                "Nummer": 32,
                "Frage": "Ich bin hilfsbereit und selbstlos.",
                "Einstufung": "",
                "Dimension": "Verträglichkeit",
                "Dimension R-Schlüssel": "Nein",
                "Facette": "Mitgefühl",
                "Facetten R-Schlüssel": "Nein"
            },
            {
                "Nummer": 33,
                "Frage": "Ich mag es sauber und aufgeräumt.",
                "Einstufung": "",
                "Dimension": "Gewissenhaftigkeit",
                "Dimension R-Schlüssel": "Nein",
                "Facette": "Ordnungsliebe",
                "Facetten R-Schlüssel": "Nein"
            },
            {
                "Nummer": 34,
                "Frage": "Ich mache mir oft Sorgen.",
                "Einstufung": "",
                "Dimension": "Negative Emotionalität",
                "Dimension R-Schlüssel": "Nein",
                "Facette": "Ängstlichkeit",
                "Facetten R-Schlüssel": "Nein"
            },
            {
                "Nummer": 35,
                "Frage": "Ich weiß Kunst und Schönheit zu schätzen.",
                "Einstufung": "",
                "Dimension": "Offenheit",
                "Dimension R-Schlüssel": "Nein",
                "Facette": "Ästhetisches Empfinden",
                "Facetten R-Schlüssel": "Nein"
            },
            {
                "Nummer": 36,
                "Frage": "Mir fällt es schwer, andere zu beeinflussen.",
                "Einstufung": "",
                "Dimension": "Extraversion",
                "Dimension R-Schlüssel": "Ja",
                "Facette": "Durchsetzungsfähigkeit",
                "Facetten R-Schlüssel": "Ja"
            },
            {
                "Nummer": 37,
                "Frage": "Ich bin manchmal unhöflich und schroff.",
                "Einstufung": "",
                "Dimension": "Verträglichkeit",
                "Dimension R-Schlüssel": "Ja",
                "Facette": "Höflichkeit",
                "Facetten R-Schlüssel": "Ja"
            },
            {
                "Nummer": 38,
                "Frage": "Ich bin effizient, erledige Dinge schnell.",
                "Einstufung": "",
                "Dimension": "Gewissenhaftigkeit",
                "Dimension R-Schlüssel": "Nein",
                "Facette": "Fleiß",
                "Facetten R-Schlüssel": "Nein"
            },
            {
                "Nummer": 39,
                "Frage": "Ich fühle mich oft bedrückt, freudlos.",
                "Einstufung": "",
                "Dimension": "Negative Emotionalität",
                "Dimension R-Schlüssel": "Nein",
                "Facette": "Niedergeschlagenheit",
                "Facetten R-Schlüssel": "Nein"
            },
            {
                "Nummer": 40,
                "Frage": "Es macht mir Spaß, gründlich über komplexe Dinge nachzudenken und sie zu verstehen.",
                "Einstufung": "",
                "Dimension": "Offenheit",
                "Dimension R-Schlüssel": "Nein",
                "Facette": "Intellektuelle Neugierde",
                "Facetten R-Schlüssel": "Nein"
            },
            {
                "Nummer": 41,
                "Frage": "Ich bin voller Energie und Tatendrang.",
                "Einstufung": "",
                "Dimension": "Extraversion",
                "Dimension R-Schlüssel": "Nein",
                "Facette": "Aktivität",
                "Facetten R-Schlüssel": "Nein"
            },
            {
                "Nummer": 42,
                "Frage": "Ich bin anderen gegenüber misstrauisch.",
                "Einstufung": "",
                "Dimension": "Verträglichkeit",
                "Dimension R-Schlüssel": "Ja",
                "Facette": "Zwischenmenschliches Vertrauen",
                "Facetten R-Schlüssel": "Ja"
            },
            {
                "Nummer": 43,
                "Frage": "Ich bin verlässlich, auf mich kann man zählen.",
                "Einstufung": "",
                "Dimension": "Gewissenhaftigkeit",
                "Dimension R-Schlüssel": "Nein",
                "Facette": "Verlässlichkeit",
                "Facetten R-Schlüssel": "Nein"
            },
            {
                "Nummer": 44,
                "Frage": "Ich habe meine Gefühle unter Kontrolle, werde selten wütend.",
                "Einstufung": "",
                "Dimension": "Negative Emotionalität",
                "Dimension R-Schlüssel": "Ja",
                "Facette": "Unbeständigkeit der Gefühle",
                "Facetten R-Schlüssel": "Ja"
            },
            {
                "Nummer": 45,
                "Frage": "Ich bin nicht sonderlich fantasievoll.",
                "Einstufung": "",
                "Dimension": "Offenheit",
                "Dimension R-Schlüssel": "Ja",
                "Facette": "Kreativer Einfallsreichtum",
                "Facetten R-Schlüssel": "Ja"
            },
            {
                "Nummer": 46,
                "Frage": "Ich bin gesprächig.",
                "Einstufung": "",
                "Dimension": "Extraversion",
                "Dimension R-Schlüssel": "Nein",
                "Facette": "Geselligkeit",
                "Facetten R-Schlüssel": "Nein"
            },
            {
                "Nummer": 47,
                "Frage": "Andere sind mir eher gleichgültig, egal.",
                "Einstufung": "",
                "Dimension": "Verträglichkeit",
                "Dimension R-Schlüssel": "Ja",
                "Facette": "Mitgefühl",
                "Facetten R-Schlüssel": "Ja"
            },
            {
                "Nummer": 48,
                "Frage": "Ich bin eher der chaotische Typ, mache selten sauber.",
                "Einstufung": "",
                "Dimension": "Gewissenhaftigkeit",
                "Dimension R-Schlüssel": "Ja",
                "Facette": "Ordnungsliebe",
                "Facetten R-Schlüssel": "Ja"
            },
            {
                "Nummer": 49,
                "Frage": "Ich werde selten nervös und unsicher.",
                "Einstufung": "",
                "Dimension": "Negative Emotionalität",
                "Dimension R-Schlüssel": "Ja",
                "Facette": "Ängstlichkeit",
                "Facetten R-Schlüssel": "Ja"
            },
            {
                "Nummer": 50,
                "Frage": "Ich finde Gedichte und Theaterstücke langweilig.",
                "Einstufung": "",
                "Dimension": "Offenheit",
                "Dimension R-Schlüssel": "Ja",
                "Facette": "Ästhetisches Empfinden",
                "Facetten R-Schlüssel": "Ja"
            },
            {
                "Nummer": 51,
                "Frage": "In einer Gruppe überlasse ich lieber anderen die Entscheidung.",
                "Einstufung": "",
                "Dimension": "Extraversion",
                "Dimension R-Schlüssel": "Ja",
                "Facette": "Durchsetzungsfähigkeit",
                "Facetten R-Schlüssel": "Ja"
            },
            {
                "Nummer": 52,
                "Frage": "Ich bin höflich und zuvorkommend.",
                "Einstufung": "",
                "Dimension": "Verträglichkeit",
                "Dimension R-Schlüssel": "Nein",
                "Facette": "Höflichkeit",
                "Facetten R-Schlüssel": "Nein"
            },
            {
                "Nummer": 53,
                "Frage": "Ich bleibe an einer Aufgabe dran, bis sie erledigt ist.",
                "Einstufung": "",
                "Dimension": "Gewissenhaftigkeit",
                "Dimension R-Schlüssel": "Nein",
                "Facette": "Fleiß",
                "Facetten R-Schlüssel": "Nein"
            },
            {
                "Nummer": 54,
                "Frage": "Ich bin oft deprimiert, niedergeschlagen.",
                "Einstufung": "",
                "Dimension": "Negative Emotionalität",
                "Dimension R-Schlüssel": "Nein",
                "Facette": "Niedergeschlagenheit",
                "Facetten R-Schlüssel": "Nein"
            },
            {
                "Nummer": 55,
                "Frage": "Mich interessieren abstrakte Überlegungen wenig.",
                "Einstufung": "",
                "Dimension": "Offenheit",
                "Dimension R-Schlüssel": "Ja",
                "Facette": "Intellektuelle Neugierde",
                "Facetten R-Schlüssel": "Ja"
            },
            {
                "Nummer": 56,
                "Frage": "Ich bin begeisterungsfähig und kann andere leicht mitreißen.",
                "Einstufung": "",
                "Dimension": "Extraversion",
                "Dimension R-Schlüssel": "Nein",
                "Facette": "Aktivität",
                "Facetten R-Schlüssel": "Nein"
            },
            {
                "Nummer": 57,
                "Frage": "Ich schenke anderen leicht Vertrauen, glaube an das Gute im Menschen.",
                "Einstufung": "",
                "Dimension": "Verträglichkeit",
                "Dimension R-Schlüssel": "Nein",
                "Facette": "Zwischenmenschliches Vertrauen",
                "Facetten R-Schlüssel": "Nein"
            },
            {
                "Nummer": 58,
                "Frage": "Manchmal verhalte ich mich verantwortungslos, leichtsinnig.",
                "Einstufung": "",
                "Dimension": "Gewissenhaftigkeit",
                "Dimension R-Schlüssel": "Ja",
                "Facette": "Verlässlichkeit",
                "Facetten R-Schlüssel": "Ja"
            },
            {
                "Nummer": 59,
                "Frage": "Ich reagiere schnell gereizt oder genervt.",
                "Einstufung": "",
                "Dimension": "Negative Emotionalität",
                "Dimension R-Schlüssel": "Nein",
                "Facette": "Unbeständigkeit der Gefühle",
                "Facetten R-Schlüssel": "Nein"
            },
            {
                "Nummer": 60,
                "Frage": "Ich bin originell, entwickle neue Ideen.",
                "Einstufung": "",
                "Dimension": "Offenheit",
                "Dimension R-Schlüssel": "Nein",
                "Facette": "Kreativer Einfallsreichtum",
                "Facetten R-Schlüssel": "Nein"
            }
        ]

        # get questions and numbers in dict
        for question in big_five_inventory:
            # save number and question
            self.fragen_liste[question["Nummer"]] = question["Frage"]
        # counter for current question
        self.aktuelle_frage = 1

        # variable for answers
        # check if there are already answers from profile
        if saved_answers is not None:
            self.saved_answers = saved_answers
        # if not create empty dict
        else:
            self.saved_answers = {}

        # Transfer old results to IntVar (for RadioButtons)
        self.vars_answers = {}
        for index in self.fragen_liste.keys():
            # take old answer, if not there then 0
            value = self.saved_answers.get(index, 0)
            self.vars_answers[index] = tk.IntVar(value=value)

        # label for question
        self.question_label = tk.Label(self.popup, text="", wraplength=1000, font=("Arial", 16), bg="#f4f1de")
        self.question_label.grid(row=0, column=1, columnspan=6, pady=50, sticky="n")

        # label for counter
        self.counter_label = tk.Label(self.popup, text="", font=("Arial", 12), bg="#f4f1de")
        self.counter_label.grid(row=3, column=1, columnspan=6, pady=10)

        # buttons for forward and backward
        self.prev_button = tk.Button(self.popup, text="Zurück", command=self.previous_question)
        self.prev_button.grid(row=4, column=0, padx=10, pady=10, sticky="e")

        self.next_button = tk.Button(self.popup, text="Weiter", command=self.next_question)
        self.next_button.grid(row=4, column=7, padx=10, pady=10, sticky="w")

        # save button
        self.save_button = tk.Button(self.popup, text="Speichern", command=self.save_answers)
        self.save_button.grid(row=5, column=1, columnspan=6, pady=20)

        # create view with first question
        self.show_question()

    # updates the view of the question, scale and counter +
    def show_question(self):
        # get the number and text of the current question
        frage_text = str(self.aktuelle_frage) + ". " + self.fragen_liste[self.aktuelle_frage]

        # change the question label in the window
        self.question_label.config(text=frage_text)

        # Refresh Likert scale
        self.create_likert_skala()

        # update counter
        counter_text = str(self.aktuelle_frage) + "/" + str(len(self.fragen_liste))
        self.counter_label.config(text=counter_text)

    # switch to the next question +
    def next_question(self):
        # if not at the end of list, increase index by 1
        if self.aktuelle_frage < len(self.fragen_liste):
            self.aktuelle_frage += 1

            # update view
            self.show_question()

    # switch to previous question +
    def previous_question(self):
        # if not at the start of list, increase index by 1
        if self.aktuelle_frage > 1:
            self.aktuelle_frage -= 1

            # update view
            self.show_question()

    # create radio buttons for likert skala +
    def create_likert_skala(self):

        # remove current radio buttons in the row
        for widget in self.popup.grid_slaves(row=1):
            widget.grid_forget()

        # create radiobuttons
        tk.Radiobutton(self.popup, variable=self.vars_answers[self.aktuelle_frage], value=1).grid(row=1, column=2, padx=5, pady=5, sticky="n")
        tk.Radiobutton(self.popup, variable=self.vars_answers[self.aktuelle_frage], value=2).grid(row=1, column=3, padx=5, pady=5, sticky="n")
        tk.Radiobutton(self.popup, variable=self.vars_answers[self.aktuelle_frage], value=3).grid(row=1, column=4, padx=5, pady=5, sticky="n")
        tk.Radiobutton(self.popup, variable=self.vars_answers[self.aktuelle_frage], value=4).grid(row=1, column=5,  padx=5, pady=5, sticky="n")
        tk.Radiobutton(self.popup, variable=self.vars_answers[self.aktuelle_frage], value=5).grid(row=1, column=6, padx=5, pady=5, sticky="n")

        # Labels for description
        tk.Label(self.popup, text="Stimme überhaupt nicht zu").grid(row=2, column=2, padx=5, pady=5, sticky="n")
        tk.Label(self.popup, text="Stimme eher nicht zu").grid(row=2, column=3, padx=5, pady=5, sticky="n")
        tk.Label(self.popup, text="Weder noch / Neutral").grid(row=2, column=4, padx=5, pady=5, sticky="n")
        tk.Label(self.popup, text="Stimme eher zu").grid(row=2, column=5, padx=5, pady=5, sticky="n")
        tk.Label(self.popup, text="Stimme voll und ganz zu").grid(row=2, column=6, padx=5, pady=5, sticky="n")

    # save the answers permanently for access from app class +
    def save_answers(self):

        # transfer answers
        for index in self.fragen_liste.keys():
            self.saved_answers[index] = self.vars_answers[index].get()


        # saved info
        messagebox.showinfo("Hinweis", "Antworten wurde gespeichert!")

        # close window
        self.popup.destroy()

    # if closed on X save anyway +
    def on_closing(self):
        self.save_answers()

