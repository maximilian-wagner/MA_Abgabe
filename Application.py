import os
import tempfile
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
from openai import OpenAI
import json
from gtts import gTTS


from QuestionWindow import QuestionWindow
from PersonalityWindow import PersonalityWindow


class Application:
    def __init__(self, root):
        # main window
        self.root = root
        self.root.title("AAC Prototyp")
        # size
        root.geometry("1600x900")

        # call function for creating full gui of main window
        self.create_gui()

        # Startmessage
        self.root.after(1000, lambda: messagebox.showinfo("Hinweis", "Vor Nutzung Profil laden oder erstellen!"))

        # GPT Api initialisation
        self.client = OpenAI(
            # This is the default and can be omitted
            api_key="!!!HIER API KEY EINFÜGEN!!!",          # API KEY
        )
        # model selection
        self.model = "gpt-4o"

        # last user input
        self.last_user_input = ""
        # last generated normal sentence
        self.last_generated_sentence = ""
        # last generated suffixes
        self.last_generated_suffixes = ""
        #  last generated personalised sentence
        self.last_generated_sentence_personalized = ""

        # profile data
        # answers for questions
        self.fragebogen_antworten = {}
        # dimension and facette data
        self.personality_traits = {}

    # create full gui of the main window +
    def create_gui(self):
        # configure grid
        self.root.grid_rowconfigure(0, weight=0)  # Oberer Bereich
        self.root.grid_rowconfigure(1, weight=1)  # Symbolbereich
        self.root.grid_columnconfigure(0, weight=1)  # Fülle den gesamten Platz

        # call function for gui in the upper segment
        self.create_upper_gui()

        # grid for lower segment of symbol buttons
        symbol_frame = tk.Frame(self.root, bg="#f4f1de")
        symbol_frame.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")

        # column 1
        self.create_symbol_button(symbol_frame, "Wann", "pictures/Wann.png", 0, 0)
        self.create_symbol_button(symbol_frame, "Warum", "pictures/warum.png", 1, 0)
        self.create_symbol_button(symbol_frame, "Was", "pictures/was.png", 2, 0)
        self.create_symbol_button(symbol_frame, "Wer", "pictures/wer.png", 3, 0)
        self.create_symbol_button(symbol_frame, "Wie", "pictures/wie.png", 4, 0)
        self.create_symbol_button(symbol_frame, "Wo", "pictures/Wo.png", 5, 0)


        # column 2
        self.create_symbol_button(symbol_frame, "Ich", "pictures/ich.png", 0, 1)
        self.create_symbol_button(symbol_frame, "Du", "pictures/du.png", 1, 1)
        self.create_symbol_button(symbol_frame, "Er", "pictures/er.png", 2, 1)
        self.create_symbol_button(symbol_frame, "Sie", "pictures/sie.png", 3, 1)
        self.create_symbol_button(symbol_frame, "Es", "pictures/es.png", 4, 1)
        self.create_symbol_button(symbol_frame, "Wir", "pictures/wir.png", 5, 1)

        # column 3
        self.create_symbol_button(symbol_frame, "ihr (Plural)", "pictures/ihr (Plural).png", 0, 2)
        self.create_symbol_button(symbol_frame, "mein", "pictures/mein.png", 1, 2)
        self.create_symbol_button(symbol_frame, "dein", "pictures/dein.png", 2, 2)
        self.create_symbol_button(symbol_frame, "sein", "pictures/sein.png", 3, 2)
        self.create_symbol_button(symbol_frame, "ihr", "pictures/ihr.png", 4, 2)
        self.create_symbol_button(symbol_frame, "unser", "pictures/unser.png", 5, 2)

        # column 4
        self.create_symbol_button(symbol_frame, "euer", "pictures/euer.png", 0, 3)
        self.create_symbol_button(symbol_frame, "kommen", "pictures/kommen.png", 1, 3)
        self.create_symbol_button(symbol_frame, "können", "pictures/können.png", 2, 3)
        self.create_symbol_button(symbol_frame, "machen", "pictures/machen.png", 3, 3)
        self.create_symbol_button(symbol_frame, "möchten", "pictures/möchten.png", 4, 3)
        self.create_symbol_button(symbol_frame, "bin / sein", "pictures/bin sein.png", 5, 3)

        # column 5
        self.create_symbol_button(symbol_frame, "fragen", "pictures/fragen.png", 0, 4)
        self.create_symbol_button(symbol_frame, "geben", "pictures/geben.png", 1, 4)
        self.create_symbol_button(symbol_frame, "haben", "pictures/haben.png", 2, 4)
        self.create_symbol_button(symbol_frame, "sagen", "pictures/sagen.png", 3, 4)
        self.create_symbol_button(symbol_frame, "sehen", "pictures/sehen.png", 4, 4)
        self.create_symbol_button(symbol_frame, "helfen", "pictures/Hilfe.png", 5, 4)

        # column 6
        self.create_symbol_button(symbol_frame, "gehen", "pictures/gehen.png", 0, 5)
        self.create_symbol_button(symbol_frame, "fühlen", "pictures/fühlen.png", 1, 5)
        self.create_symbol_button(symbol_frame, "wissen", "pictures/wissen.png", 2, 5)
        self.create_symbol_button(symbol_frame, "lernen", "pictures/lernen.png", 3, 5)
        self.create_symbol_button(symbol_frame, "gefallen", "pictures/gefallen.png", 4, 5)
        self.create_symbol_button(symbol_frame, "denken", "pictures/denken.png", 5, 5)

        # column 7
        self.create_symbol_button(symbol_frame, "essen", "pictures/essen.png", 0, 6)
        self.create_symbol_button(symbol_frame, "weniger", "pictures/weniger.png", 1, 6)
        self.create_symbol_button(symbol_frame, "mehr", "pictures/mehr.png", 2, 6)
        self.create_symbol_button(symbol_frame, "oder", "pictures/oder.png", 3, 6)
        self.create_symbol_button(symbol_frame, "und", "pictures/und.png", 4, 6)

        # column 8
        self.create_symbol_button(symbol_frame, "Bitte", "pictures/Bitte.png", 0, 7)
        self.create_symbol_button(symbol_frame, "Danke", "pictures/danke.png", 1, 7)
        self.create_symbol_button(symbol_frame, "?", "pictures/Fragezeichen.png", 2, 7)
        self.create_symbol_button(symbol_frame, "Ja", "pictures/Ja.png", 3, 7)
        self.create_symbol_button(symbol_frame, "Nein", "pictures/nein.png", 4, 7)
        self.create_symbol_button(symbol_frame, "Verneinung", "pictures/Verneinung.png", 5, 7)

        # column 9
        self.create_symbol_button(symbol_frame, "vorher", "pictures/vorher.png", 0, 8)
        self.create_symbol_button(symbol_frame, "danach", "pictures/danach.png", 1, 8)
        self.create_symbol_button(symbol_frame, "in", "pictures/in.png", 2, 8)
        self.create_symbol_button(symbol_frame, "zu", "pictures/zu.png", 3, 8)
        self.create_symbol_button(symbol_frame, "mit", "pictures/mit.png", 4, 8)
        self.create_symbol_button(symbol_frame, "ohne", "pictures/ohne.png", 5, 8)

        # column 10
        self.create_symbol_button(symbol_frame, "gut", "pictures/gut.png", 0, 9)
        self.create_symbol_button(symbol_frame, "sehr gut", "pictures/sehr gut.png", 1, 9)
        self.create_symbol_button(symbol_frame, "schlecht", "pictures/schlecht.png", 2, 9)
        self.create_symbol_button(symbol_frame, "wenn", "pictures/wenn.png", 3, 9)
        self.create_symbol_button(symbol_frame, "weil", "pictures/weil.png", 4, 9)
        self.create_symbol_button(symbol_frame, "kein", "pictures/kein.png", 5, 9)

        # column 11
        self.create_symbol_button(symbol_frame, "Heute", "pictures/heute.png", 0, 11)
        self.create_symbol_button(symbol_frame, "Gestern", "pictures/gestern.png", 1, 11)
        self.create_symbol_button(symbol_frame, "Morgen", "pictures/morgen.png", 2, 11)
        self.create_symbol_button(symbol_frame, "Begrüßung", "pictures/Begrüßung.png", 3, 11)
        self.create_symbol_button(symbol_frame, "Verabschiedung", "pictures/Verabschiedung.png", 4, 11)

        # collections of symbol buttons
        # Lebensmittel
        group_dict_lebensmittel = {
            "Apfel": "pictures/Lebensmittel/Apfel.png",
            "Banane": "pictures/Lebensmittel/Banane.png",
            "Bier": "pictures/Lebensmittel/Bier.png",
            "Bretzel": "pictures/Lebensmittel/Bretzel.png",
            "Cola": "pictures/Lebensmittel/Cola.png",
            "Cornflakes": "pictures/Lebensmittel/Cornflakes.png",
            "Eisbecher": "pictures/Lebensmittel/Eisbecher.png",
            "Eistee": "pictures/Lebensmittel/Eistee.png",
            "Entrecôte": "pictures/Lebensmittel/Entrecôte.png",
            "Fleisch": "pictures/Lebensmittel/Fleisch.png",
            "Gemüse": "pictures/Lebensmittel/Gemüse.png",
            "Kaffee": "pictures/Lebensmittel/Kaffee.png",
            "Kebab": "pictures/Lebensmittel/Kebab.png",
            "Kuchen": "pictures/Lebensmittel/Kuchen.png",
            "Nudeln": "pictures/Lebensmittel/Nudeln.png",
            "salzig": "pictures/Lebensmittel/salzig.png",
            "Sandwich": "pictures/Lebensmittel/Sandwich.png",
            "sauer": "pictures/Lebensmittel/sauer.png",
            "scharf": "pictures/Lebensmittel/scharf.png",
            "Schokolade": "pictures/Lebensmittel/Schokolade.png",
            "Spaghetti": "pictures/Lebensmittel/Spaghetti.png",
            "süß": "pictures/Lebensmittel/süß.png",
            "Toastbrot": "pictures/Lebensmittel/Toastbrot.png",
            "Wasser": "pictures/Lebensmittel/Wasser.png",
            "Wassermelone": "pictures/Lebensmittel/Wassermelone.png"}
        self.create_group_button(symbol_frame, "Lebensmittel [+]", "pictures/Lebensmittel.png", 0, 10, group_dict_lebensmittel)

        # Freizeit
        group_dict_freizeit = {
            "Gaming": "pictures/Freizeit/Gaming.png",
            "Konzert": "pictures/Freizeit/Konzert.png",
            "Lesen": "pictures/Freizeit/Lesen.png",
            "Lotto": "pictures/Freizeit/Lotto.png",
            "malen": "pictures/Freizeit/malen.png",
            "Musik hören": "pictures/Freizeit/Musik hören.png",
            "Sport": "pictures/Freizeit/Sport.png"
        }
        self.create_group_button(symbol_frame, "Freizeit [+]", "pictures/Freizeit.png", 1, 10, group_dict_freizeit)

        # Orte
        group_dict_orte = {
            "Apotheke": "pictures/Orte/Apotheke.png",
            "Arzt": "pictures/Orte/Arzt.png",
            "Badezimmer": "pictures/Orte/Badezimmer.png",
            "Bank": "pictures/Orte/Bank.png",
            "Buchladen": "pictures/Orte/Buchladen.png",
            "Arbeit": "pictures/Orte/Bürogebäude.png",
            "Computergeschäft": "pictures/Orte/Computergeschäft.png",
            "Einkaufszentrum": "pictures/Orte/Einkaufszentrum.png",
            "Küche": "pictures/Orte/Küche.png",
            "Ort": "pictures/Orte/Ort.png",
            "Schlafzimmer": "pictures/Orte/Schlafzimmer.png",
            "Schule": "pictures/Orte/Schule.png",
            "Supermarkt": "pictures/Orte/Supermarkt.png",
            "Universität": "pictures/Orte/Universität.png",
            "Wohnzimmer": "pictures/Orte/Wohnzimmer.png",
            "Zahnarzt": "pictures/Orte/Zahnarzt.png",
            "Zuhause": "pictures/Orte/Zuhause.png"
        }
        self.create_group_button(symbol_frame, "Orte [+]", "pictures/Orte.png", 2, 10, group_dict_orte)

        # Arbeit
        group_dict_arbeit = {
            "arbeiten": "pictures/Arbeit/arbeiten.png",
            "Aufgaben": "pictures/Arbeit/Aufgaben.png",
            "Büro": "pictures/Arbeit/Büro.png",
            "Informationen": "pictures/Arbeit/informationen.png",
            "Kunde": "pictures/Arbeit/Kunde.png",
            "Meeting": "pictures/Arbeit/Meeting.png",
            "organisieren": "pictures/Arbeit/organisieren.png",
            "planen": "pictures/Arbeit/planen.png",
            "Projekt": "pictures/Arbeit/projekt.png",
            "Team": "pictures/Arbeit/Team.png"
        }
        self.create_group_button(symbol_frame, "Arbeit [+]", "pictures/Orte/Bürogebäude.png", 3, 10, group_dict_arbeit)

        # Emotionen
        group_dict_emotionen = {
            "angeekelt": "pictures/Emotionen/angeekelt.png",
            "besorgt": "pictures/Emotionen/besorgt.png",
            "dankbar": "pictures/Emotionen/dankbar.png",
            "entspannt": "pictures/Emotionen/entspannt.png",
            "entzückt": "pictures/Emotionen/entzückt.png",
            "ernst": "pictures/Emotionen/ernst.png",
            "erschrocken": "pictures/Emotionen/erschrocken.png",
            "gehässig": "pictures/Emotionen/gehässig.png",
            "gelangweilt": "pictures/Emotionen/gelangweilt.png",
            "glücklich": "pictures/Emotionen/glücklich.png",
            "hoffnungsvoll": "pictures/Emotionen/hoffnungsvoll.png",
            "hungrig": "pictures/Emotionen/hungrig.png",
            "mutig": "pictures/Emotionen/mutig.png",
            "müde": "pictures/Emotionen/müde.png",
            "neidisch": "pictures/Emotionen/neidisch.png",
            "nervös": "pictures/Emotionen/nervös.png",
            "neugierig": "pictures/Emotionen/neugierig.png",
            "nostalgisch": "pictures/Emotionen/nostalgisch.png",
            "sauer": "pictures/Emotionen/sauer.png",
            "traurig": "pictures/Emotionen/traurig.png",
            "verlegen": "pictures/Emotionen/verlegen.png",
            "verliebt": "pictures/Emotionen/verliebt.png",
            "verrückt": "pictures/Emotionen/verrückt.png",
            "verwirrt": "pictures/Emotionen/verwirrt.png",
            "zufrieden": "pictures/Emotionen/zufrieden.png",
            "ängstlich": "pictures/Emotionen/ängstlich.png",
            "überfordert": "pictures/Emotionen/überfordert.png",
            "überrascht": "pictures/Emotionen/überrascht.png"
        }
        self.create_group_button(symbol_frame, "Emotionen [+]", "pictures/Emotionen.png", 4, 10, group_dict_emotionen)

        # Personen
        group_dict_personen = {
            "Markus": "pictures/Personen/Mann.png",
            "Susi": "pictures/Personen/Frau.png"
        }
        self.create_group_button(symbol_frame, "Personen [+]", "pictures/Personen/Mann.png", 5, 10, group_dict_personen)

    # create the upper part of gui +
    def create_upper_gui(self):
        # frame for upper part
        upper_frame = tk.Frame(self.root, bg="#e07a5f")
        upper_frame.grid(row=0, column=0, padx=0, pady=0, sticky="ew")

        # configure grid
        upper_frame.columnconfigure(0, weight=1)
        upper_frame.columnconfigure(1, weight=1)
        upper_frame.columnconfigure(2, weight=3)
        upper_frame.columnconfigure(3, weight=1)
        upper_frame.columnconfigure(4, weight=1)

        # buttons on left side
        button_l1 = tk.Button(upper_frame, text="Profil exportieren", width=10, height=3, bg="#3d405b", fg="#f4f1de",
                              font="bold", command=self.export_profile)
        button_l1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        button_l2 = tk.Button(upper_frame, text="Persönlichkeit abfragen", width=10, height=3, bg="#3d405b", fg="#f4f1de",
                              font="bold", command=lambda: self.open_fragebogen())
        button_l2.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        button_l3 = tk.Button(upper_frame, text="Profil importieren", width=10, height=3, bg="#3d405b", fg="#f4f1de",
                              font="bold", command=self.import_profile)
        button_l3.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        button_l4 = tk.Button(upper_frame, text="Auswertung Persönlichkeit", width=10, height=3, bg="#3d405b", fg="#f4f1de",
                              font="bold", command=self.show_personality_window)
        button_l4.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        # textfield
        self.textfeld = tk.Text(upper_frame, height=5, width=50, bg="#f4f1de", fg="#000000", wrap="word")
        self.textfeld.grid(row=0, column=2, rowspan=2, padx=10, pady=10, sticky="nsew")

        # buttons on right side
        button_r1 = tk.Button(upper_frame, text="Generiere\nunpersonalisierten Satz", width=10, height=3, bg="#3d405b", fg="#f4f1de",
                              font="bold", command=lambda: self.generate_normal_sentence())
        button_r1.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")

        button_r2 = tk.Button(upper_frame, text="Lösche Eingabe", width=10, height=3, bg="#3d405b", fg="#f4f1de",
                              font="bold", command=lambda: self.clear_text())
        button_r2.grid(row=0, column=4, padx=5, pady=5, sticky="nsew")

        button_r3 = tk.Button(upper_frame, text="Generiere\npersonalisierten Satz", width=10, height=3, bg="#3d405b", fg="#f4f1de",
                              font="bold", command=lambda: self.generate_personalised_sentence())
        button_r3.grid(row=1, column=3, padx=5, pady=5, sticky="nsew")

        button_r4 = tk.Button(upper_frame, text="Sprachausgabe", width=10, height=3, bg="#3d405b", fg="#f4f1de",
                              font="bold", command=self.text_to_speech)
        button_r4.grid(row=1, column=4, padx=5, pady=5, sticky="nsew")

    # give textfield name if click on symbol button +
    def click_symbol_button(self, text):
        # get text of textfield
        old_text = self.textfeld.get("1.0", tk.END).strip()
        new_text =""

        # check if empty if not add text
        if old_text.strip() == "":
            new_text = text
        else:
            new_text = old_text + ' + ' + text

        # get new text in field
        self.insert_text_in_textfield(new_text)

    # function for click on group button +
    def click_group_button(self, group_name, group_dict):
        # create new window
        popup = tk.Toplevel(self.root, bg="#f4f1de")
        popup.title(group_name)
        popup.geometry("830x500")

        # variables for rows and column because of size
        max_rows = 4
        max_columns = 7

        # fill grid with buttons from Dict
        for index, (text, pic_path) in enumerate(group_dict.items()):
            # calculate row and column to fill the grid
            row_index = index % max_rows
            column_index = index // max_rows

            if column_index < max_columns:
                # create button and put it on grid
                self.create_symbol_button(popup, text, pic_path, row_index, column_index)
            # if to much buttons in dict
            else: print("Zuviele Elemente für die Gruppe!")

    # create button for collection of symbol buttons +
    def create_group_button(self, root, text, pic_path, row, column, group_dict):

        # resize picture
        image_group_picture = self.resize_button_image(pic_path)
        # create button
        group_button = tk.Button(root, text=text, image=image_group_picture, compound="top", width=100, height=100, command=lambda: self.click_group_button(text, group_dict))
        # assign image
        group_button.image = image_group_picture
        # put on grid
        group_button.grid(row=row, column=column, padx=5, pady=5)

    # create aac symbol button +
    def create_symbol_button(self, root, text, pic_path, row, column):

        # resize picture
        image_resized = self.resize_button_image(pic_path)

        # create button
        button = tk.Button(root, text=text, image=image_resized, compound="top", width=100, height=100, command=lambda: self.click_symbol_button(text))
        # assign image
        button.image = image_resized
        # put on grid
        button.grid(row=row, column=column, padx=5, pady=5)

        return button

    # convert pictures in right size for buttons +
    def resize_button_image(self, pic_path):
        image = Image.open(pic_path)
        image = image.resize((80, 80))
        image_ready = ImageTk.PhotoImage(image)

        return image_ready

    # clears the textfield +
    def clear_text(self):
        self.textfeld.delete("1.0", tk.END)

    # insert text into textfield +
    def insert_text_in_textfield(self, text):
        # delete text
        self.clear_text()
        # input new text
        self.textfeld.insert(tk.END, text)

    # open window for big five questions +
    def open_fragebogen(self):
        # open
        self.fragebogen = QuestionWindow(self.root, self.fragebogen_antworten)

        # wait until finished
        self.root.wait_window(self.fragebogen.popup)

        # save answers
        self.fragebogen_antworten = self.fragebogen.saved_answers

        # call function to calculate personality
        self.calculate_personality_traits()

    # calculate personality of answered questions +
    def calculate_personality_traits(self):

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

        # dict for dimensions and facettes
        dimensionen = {
            "Extraversion": 0,
            "Verträglichkeit": 0,
            "Gewissenhaftigkeit": 0,
            "Negative Emotionalität": 0,
            "Offenheit": 0
        }

        facetten = {
            "Geselligkeit": 0,
            "Durchsetzungsfähigkeit": 0,
            "Aktivität": 0,
            "Mitgefühl": 0,
            "Höflichkeit": 0,
            "Zwischenmenschliches Vertrauen": 0,
            "Ordnungsliebe": 0,
            "Fleiß": 0,
            "Verlässlichkeit": 0,
            "Ängstlichkeit": 0,
            "Niedergeschlagenheit": 0,
            "Unbeständigkeit der Gefühle": 0,
            "Ästhetisches Empfinden": 0,
            "Intellektuelle Neugierde": 0,
            "Kreativer Einfallsreichtum": 0
        }

        # calculate Dimension-values
        # get all values
        for item in big_five_inventory:
            # get score from user rating
            score = self.fragebogen_antworten[item.get("Nummer")]
            # invert score if inverted question
            if item.get("Dimension R-Schlüssel") == "Ja":
                score = self.likert_skala_umkehren(score)
            # add score to right dimension
            dimensionen[item.get("Dimension")] += score

        # value normalisation
        # each Dimension has 12 questions, five is the highest possible score
        max_score_dimensionen = 12 * 5
        # normalise: value / maximum value * 100
        for key, value in dimensionen.items():
            dimensionen[key] = round((value / max_score_dimensionen) * 100, 1)

        # calculate Facetten-values
        # get scores
        for item in big_five_inventory:
            # score
            score = self.fragebogen_antworten[item.get("Nummer")]
            # invert score if inverted question
            if item.get("Facetten R-Schlüssel") == "Ja":
                score = self.likert_skala_umkehren(score)
            # add score to right Facette
            facetten[item.get("Facette")] += score

        # value normalisation
        # each Dimension has 4 questions, five is the highest possible score
        max_score_facetten = 4 * 5
        # normalise: value / maximum value * 100
        for key, value in facetten.items():
            facetten[key] = round((value / max_score_facetten) * 100, 1)

        # save data in user profile variables
        self.personality_traits = {
            "dimensionen": dimensionen,
            "facetten": facetten,
        }

    # function for inverted question +
    def likert_skala_umkehren(self, rating):
        match rating:
            case 1:
                return 5
            case 2:
                return 4
            case 3:
                return 3
            case 4:
                return 2
            case 5:
                return 1
            case 0:
                return 0
            case _:
                return None

    # open personality window with graphs +
    def show_personality_window(self):
        # check if there is personality data
        if self.personality_traits:
            # open
            self.auswertung_fenster = PersonalityWindow(self.root, self.personality_traits)
        else:
            messagebox.showinfo("Hinweis", "Keine Persönlichkeit hinterlegt!")

    # export user profile +
    def export_profile(self):
        # bundle user data
        profile_data = {
            "fragebogen_antworten": self.fragebogen_antworten,
            "personality_traits": self.personality_traits
        }

        # save location
        file_path = tk.filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])

        if file_path:
            try:
                # save
                with open(file_path, 'w') as file:
                    json.dump(profile_data, file, indent=4)
                # message if successful
                messagebox.showinfo("Hinweis", "Profil gespeichert!")
            # if error
            except Exception as e:
                print(f"Fehler: {e}")

    # import user profile +
    def import_profile(self):
        # select file
        file_path = tk.filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])

        if file_path:
            try:
                # load file
                with open(file_path, 'r') as file:
                    combined_data = json.load(file)

                # get data in variables
                self.fragebogen_antworten = combined_data.get("fragebogen_antworten")
                self.personality_traits = combined_data.get("personality_traits")

                # Convert the keys in self.questionnaire_answers back to int (JSON can only use strings as keys)
                # current keys as a list
                current_keys = list(self.fragebogen_antworten.keys())
                # iterate
                for string_key in current_keys:
                    # change to int
                    int_key = int(string_key)
                    # save value
                    answer_value = self.fragebogen_antworten.pop(string_key)
                    # add new int key with value again
                    self.fragebogen_antworten[int_key] = answer_value
                # show message
                messagebox.showinfo("Hinweis", "Profil geladen!")
            # if error
            except Exception as e:
                print(f"Fehler: {e}")

    # convert AAC symbols into sentence +
    def generate_normal_sentence(self):

        # get input text
        user_input = self.textfeld.get("1.0", tk.END).strip()

        # save in last user input
        self.last_user_input = user_input

        # Prompt-Text
        prompt_anweisung = "Du bist ein Assistenzsystem für eine Person, die nicht sprechen kann. Die Person kann Symbolknöpfe drücken, deren Begriffe du übergeben bekommst. Dabei sind mehrere Wörter mit einem Plus verknüpft. Deine Aufgabe ist es die Begriffe in einen kommunikativen Satz umzuwandeln, die der Nutzer so sagen könnte. Beachte die Reihenfolge der Begriffe und korrigiere dabei nur die Grammatik, um einen guten Satz zu bilden. Schreibe nur in der Ich-Perspektive. Achte ganz genau darauf welche Begriffe enthalten sind und welche nicht um keine falschen Sätze zu bilden. Der Begriff 'bin / sein' hat je nach Anwendungsfall verschiedene Bedeutungen. Zum Beispiel: 'ich + sein' soll zu 'Ich bin' werden, 'du + sein' soll zu 'Du bist' werden, und 'er + sein' soll zu 'Er ist' werden. Andersrum wird 'sein + ich' zu 'ich bin' und so weiter. Achte besonders auf das Personalpronomen als wer das Subjektiv im Satz ist, um keine Fehler zu machen. Zusätzlich generiere bei dem Begriff 'Begrüßung' eine Begrüßungsatz und bei 'Verabschiedung' einen Verabschiedungssatz. Hier findest du Beispiele:"
        beispiele = {
            "Ich + gehen + Supermarkt": "Ich gehe zum Supermarkt.",
            "Du + möchten + kommen + mit": "Möchtest du mitkommen?",
            "Wir + gehen + danach + essen": "Wir gehen danach essen.",
            "Sie + bin / sein + müde + und + möchte + Schlafzimmer": "Sie ist müde und möchte ins Schlafzimmer.",
            "Ich + wissen + Verneinung + warum": "Ich weiß nicht warum.",
            "Er + können + Verneinung + kommen": "Er kann nicht kommen.",
            "Wann + wir + gehen + lernen": "Wann gehen wir lernen?",
            "Ich + möchten + Sandwich + und + Cola": "Ich hätte gerne ein Sandwich und eine Cola.",
            "Du + helfen + mir": "Du musst mir helfen.",
            "Was + Du + denken + ?": "Was denkst du darüber?",
            "Wir + machen + Es + Zukunft": "Wir machen das später.",
            "Sie + Verneinung + sagen": "Sie sagt nichts.",
            "Er + fragen + Du + kommen": "Er fragt, ob du kommst.",
            "Ich + bin / sein + hungrig + und + möchten + essen": "Ich bin hungrig und möchte essen.",
            "Sie + bin / sein + glücklich + weil + Meeting": "Sie ist glücklich, wegen des Meetings.",
            "Warum + du + gehen + ohne + Ich": "Warum gehst du ohne mich?",
            "Was + wir + machen + danach": "Was machen wir danach?",
            "Ich + fühlen + Ich + Verneinung + gut": "Ich fühle mich nicht gut.",
            "Du + möchten + malen + mit + uns": "Willst du mit uns malen?",
            "Er + bin / sein + sauer + weil + Du + Verneinung + kommen + Vergangenheit": "Er ist sauer, weil du nicht 	gekommen bist.",
            "Wir + können + arbeiten + mit + Projekt": "Wir können zusammen arbeiten am Projekt.",
            "Ich + bin / sein + neugierig + Konzert": "Ich bin neugierig auf das Konzert.",
            "Du + möchten + Schokolade + ?": "Magst du Schokolade?",
            "Wann + Du + gehen + Zuhause": "Wann gehst du nach Hause?",
            "Ich + denken + Du + machen + sehr gut": "Ich denke, du machst das sehr gut.",
            "Wir + Verneinung + haben + Kunde": "Wir haben keinen Kunden.",
            "Du + können + helfen + Ich + Zukunft": "Wirst du mir helfen können?",
            "Sie + lernen + Universität": "Sie lernt für die Universität.",
            "Du + fragen + Ich + warum + Ich + glücklich": "Du fragst mich, warum ich glücklich bin.",
            "Wir + möchten + gehen + zu + Konzert": "Wir möchten zum Konzert gehen.",
            "Was + Du + machen + danach + arbeiten": "Was machst du nach der Arbeit?",
            "Warum + Er + Verneinung + kommen": "Warum kommt er nicht?",
            "Vergangenheit + Du + in + Kino + ?": "Warst du im Kino?",
            "helfen + Du + Ich + Bitte": "Hilf mir bitte.",
            "bin / sein + Du + danach + Arbeit + ?": "Bist du danach in der Arbeit?"
        }
        system_message_aac_to_speech = prompt_anweisung + str(beispiele)

        # send to api
        chat_completion = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_message_aac_to_speech},
                {"role": "user", "content": user_input},
            ],
            model=self.model,
            max_completion_tokens=150

        )
        # get output
        output = chat_completion.choices[0].message.content
        self.last_generated_sentence = output

        # insert output in textfield
        self.insert_text_in_textfield(output)

        print("1. Nutzereingabe : " + user_input)
        print("2. normaler Satz: " + output)

    # creates suffixes for the sentence personalisation +
    def generate_suffixes(self):

            # get the last generated sentence and user personality
            satz = self.last_generated_sentence
            nutzer_profil = self.personality_traits


            suffix_beispiele = {
                "dimensionen": {
                    "Extraversion": {
                        "beschreibung": "Wie gesellig, energisch und durchsetzungsfähig eine Person ist.",
                        "suffixe": {
                            "hoch": ["energisch", "gesellig"],
                            "mittel": ["zugänglich", "bedacht"],
                            "niedrig": ["ruhig", "zurückhaltend"]
                        },
                        "facetten": {
                            "Geselligkeit": {
                                "hoch": ["gesprächig", "kontaktfreudig"],
                                "niedrig": ["ruhig", "reserviert"]
                            },
                            "Durchsetzungsfähigkeit": {
                                "hoch": ["selbstbewusst", "entschlossen"],
                                "niedrig": ["zurückhaltend", "passiv"]
                            },
                            "Aktivität": {
                                "hoch": ["dynamisch", "tatkräftig"],
                                "niedrig": ["gemütlich", "bedächtig"]
                            }
                        }
                    },
                    "Verträglichkeit": {
                        "beschreibung": "Wie freundlich, hilfsbereit und kooperativ jemand ist.",
                        "suffixe": {
                            "hoch": ["freundlich", "hilfsbereit"],
                            "mittel": ["respektvoll", "kollegial"],
                            "niedrig": ["direkt", "unabhängig"]
                        },
                        "facetten": {
                            "Mitgefühl": {
                                "hoch": ["empathisch", "fürsorglich"],
                                "niedrig": ["rational", "distanziert"]
                            },
                            "Höflichkeit": {
                                "hoch": ["höflich", "zuvorkommend"],
                                "niedrig": ["direkt", "sachlich"]
                            },
                            "Zwischenmenschliches Vertrauen": {
                                "hoch": ["vertrauensvoll", "offen"],
                                "niedrig": ["skeptisch", "vorsichtig"]
                            }
                        }
                    },
                    "Gewissenhaftigkeit": {
                        "beschreibung": "Wie organisiert, zuverlässig und sorgfältig jemand ist.",
                        "suffixe": {
                            "hoch": ["organisiert", "verlässlich"],
                            "mittel": ["flexibel", "pragmatisch"],
                            "niedrig": ["spontan", "locker"]
                        },
                        "facetten": {
                            "Ordnungsliebe": {
                                "hoch": ["sehr strukturiert", "ordentlich"],
                                "niedrig": ["spontan", "unstrukturiert"]
                            },
                            "Fleiß": {
                                "hoch": ["fleißig", "ehrgeizig"],
                                "niedrig": ["gemütlich", "entspannt"]
                            },
                            "Verlässlichkeit": {
                                "hoch": ["zuverlässig", "verantwortungsbewusst"],
                                "niedrig": ["weniger verantwortungsbewusst", "locker"]
                            }
                        }
                    },
                    "Negative Emotionalität": {
                        "beschreibung": "Wie anfällig jemand für Stress, Ängstlichkeit oder Traurigkeit ist.",
                        "suffixe": {
                            "hoch": ["besorgt", "vorsichtig"],
                            "mittel": ["emotional stabil"],
                            "niedrig": ["entspannt", "sorgenfrei"]
                        },
                        "facetten": {
                            "Ängstlichkeit": {
                                "hoch": ["vorsichtig", "besorgt"],
                                "niedrig": ["zuversichtlich", "ruhig"]
                            },
                            "Niedergeschlagenheit": {
                                "hoch": ["nachdenklich", "melancholisch"],
                                "niedrig": ["optimistisch", "fröhlich"]
                            },
                            "Unbeständigkeit der Gefühle": {
                                "hoch": ["emotional", "sensibel"],
                                "niedrig": ["stabil", "gelassen"]
                            }
                        }
                    },
                    "Offenheit": {
                        "beschreibung": "Wie offen jemand für neue Erfahrungen, Ideen und Kreativität ist.",
                        "suffixe": {
                            "hoch": ["kreativ", "offen für Neues"],
                            "mittel": ["neugierig", "pragmatisch"],
                            "niedrig": ["konservativ", "traditionsbewusst"]
                        },
                        "facetten": {
                            "Ästhetisches Empfinden": {
                                "hoch": ["kunstliebend", "feinfühlig"],
                                "niedrig": ["pragmatisch", "schlicht"]
                            },
                            "Intellektuelle Neugierde": {
                                "hoch": ["wissbegierig", "reflektiert"],
                                "niedrig": ["praktisch", "direkt"]
                            },
                            "Kreativer Einfallsreichtum": {
                                "hoch": ["innovativ", "erfinderisch"],
                                "niedrig": ["konservativ", "bodenständig"]
                            }
                        }
                    }
                }
            }

            ausgabe_beispiel = [
                "freundlich",
                "offen",
                "einfühlsam",
                "respektvoll"
            ]

            # Prompt instruction
            prompt_beschreibung = "Du bist ein Assistenzsystem, welches hilft einen Text auf Basis eines Persönlichkeitsprofils zu personalisieren. Deine Aufgabe ist es, die für diesen Satz relevantesten Persönlichkeitseigenschaften aus dem Profil zu identifizieren und dafür passende Suffixe zu erstellen, welche Ton,Stil und Ausdruck der Persönlich des Nutzers beschreiben.\n\n"

            # Prompt context
            context_beschreibung = (f"Kontext:\n\n"
                                   f"Das ist der Satz, auf den du dich konzentrieren sollst: {satz}\n\n"
                                   f"Hier ist das Persönlichkeitsprofil des Nutzers bestehend aus den Big-5 Dimension und Facetten. Jedes davon ist mit einem Prozentwert beschrieben, zu wie viel Prozent diese Eigenschaft zu dem Nutzer passt: {nutzer_profil}\n\n")
            # Prompt task description
            aufgaben_beschreibung = (f"Aufgabe:\n\n"
                                     f"1. Deine erste Aufgabe ist es die wichtigsten Dimensionen und Facetten basieren auf den gegebenen Satz und den Profilwerten des Nutzers zu identifizieren."
                                     f"Berücksichtige dabei die Relevanz der Dimensionen und Facetten für den Nutzer anhand der Prozentwerte und beachte, dass die Auswahl zum Kontext des Satzes passen soll. Außerdem sind das Sätze die vom Nutzer an eine andere Person gerichtet sind.\n\n"
                                     f"2. Darauf folgend sollst du Suffixe für die ausgewählten Dimensionen und Facetten bilden. Verwende  dabei passende Suffixe, die den Stil und Ton der ausgewählten Dimension oder Facette wiedergeben und den Grad der Ausprägung im Persönlichkeitsprofil wiederspiegeln."
                                     f"Hier findest du noch Beispiele, wie Suffixe zu den jeweiligen Dimensionen und Facetten aussehen können. Dabei ist je nach Ausprägung der Dimension oder Facette, also niedrig, mittel oder hoch, eine Auswahl von zwei Suffixen gegeben: {suffix_beispiele} Wichtig: die Suffixe sind einzeln zu betrachten du sollst nicht einfach beide nehmen!\n\n")

            # Prompt Output description
            ausgabe_beschreibung = (f"Ausgabe: Gib **ausschließlich** eine Liste der Suffixe zurück, die aus den relevanten Dimensionen und Facetten generiert wurden. Beschränke es auf die drei am besten passenden Suffixe. Beispiel für das Ausgabeformat: {ausgabe_beispiel}")

            # combine all prompts to one
            prompt = prompt_beschreibung + context_beschreibung + aufgaben_beschreibung + ausgabe_beschreibung

            # send to api
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": prompt}
                ],
                model=self.model,
            )

            # ssave generated suffixes
            self.last_generated_suffixes = chat_completion.choices[0].message.content

            print("3. generierte Suffixe: " + self.last_generated_suffixes)

    # create a personalised sentence +
    def generate_personalised_sentence(self):
        # check if the normal generation was already triggert or if greeting or goodbye
        current_text = self.textfeld.get("1.0", tk.END).strip()
        if "+" in current_text or current_text == "Begrüßung" or current_text == "Verabschiedung":
            # call normal sentence generation
            self.generate_normal_sentence()

        # call generate suffixes function
        self.generate_suffixes()

        # remove special characters
        suffixes_combined = self.last_generated_suffixes.strip("[]").replace("'", "")
        print("4. Suffixe bearbeitet: " + suffixes_combined)

        # get generated unpersonalised sentence
        satz = self.last_generated_sentence

        # Description Prompt
        prompt_beschreibung = (f"Du bist ein Sprachmodell, welches auf Basis von Persönlichkeitseigenschaften Sätze personalisiert. In einem vorherigen Schritt wurden schon Suffixe identifiziert, welche für die Anpassung des Satzes wichtig sind."
                              f" Du sollst folgenden Satz damit anreichern, damit ein Satz entsteht wie es in einer normalen Konversation vorkommen würde: {satz}\n\n"
                               f"Verwende folgende Suffixe um den Satz umzuformulieren, Achte darauf, dass der Stil und Ton des Satzes den Suffixen entspricht: {suffixes_combined}\n\n"
                               f"Es darf auf keinen Fall eine Antwort auf den Satz sein, sondern du sollst ihn nur umformulieren und personalisiert anreichern!"
                               f"Er soll außerdem maximal 1,5mal so lang sein wie der Ausgangssatz und es soll nur geduzt werden!"
                               f"Gib **ausschließlich** den umformulierten Satz zurück")

        # send to api
        chat_completion = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": prompt_beschreibung}
            ],
            model=self.model,
        )

        # save generated personalised sentence
        self.last_generated_sentence_personalized = chat_completion.choices[0].message.content

        # display it on textfiled
        self.insert_text_in_textfield(self.last_generated_sentence_personalized)

        print("5. personalisierter Satz: " + self.last_generated_sentence_personalized)

    # text to speech function
    def text_to_speech(self, lang='de'):
        # get text from textfield
        text = self.textfeld.get("1.0", tk.END)

        # create mp3
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_mp3:
            tts = gTTS(text=text, lang=lang)
            tts.write_to_fp(temp_mp3)

        # play mp3
        os.system(f'start "" "{temp_mp3.name}"')



if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
