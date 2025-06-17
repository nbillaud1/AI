import customtkinter as ctk
import re
import wikipedia

#TODO reste à gérer les synonymes _('<')_/.
#                                /   |
#                                   / \

# Connaissances de base :
# bonjour:Bonjour, que puis-je faire pour vous ?
# au revoir:Au revoir !
# tu est une ia:une Infinie Alcoolique !
# ok:Y'a t'il autre chose que je peux faire pour vous ?
# accord:Y'a t'il autre chose que je peux faire pour vous ?
# merci:Y'a t'il autre chose que je peux faire pour vous ?
#
# Inutiles de base :
# le la les je tu il elle nous vous ils elles du de des au en d s c l ? !

class AppIA(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("700x700")
        #self.overrideredirect(True)
        self.title("IA (Infiniment Analphabète)")
        self.useless_words = []
        self.responses = {}
        self.updateKnowledge()
        self.last_question = ""
        self.awaiting = None
        self.internet_response = ""

        # Associer la touchee entrée à l'envoie du message
        self.bind("<Return>", self.send)

        # Création de l'en-tête
        self.header = ctk.CTkLabel(self, text="IA (Infiniment Analphabète) ! pour quitter entrez /q", font=("Calibri", 20, "bold"))
        self.header.pack(pady=10)

        # Création de l'affichage des messages
        self.chat_history = ctk.CTkTextbox(self, width=480, height=450, state="disabled")
        self.chat_history.pack(pady=10, padx=10, fill="both", expand=True)

        # Ajout des couleurs pour le bot et le user
        self.chat_history.tag_config("user", foreground="blue")
        self.chat_history.tag_config("bot", foreground="green")

        # Création du champs de saisie
        self.user_input = ctk.CTkFrame(self)
        self.user_input.pack(pady=10, padx=10, fill="x")

        self.entry = ctk.CTkEntry(self.user_input, placeholder_text="Entrez votre texte ici !", width=550)
        self.entry.pack(padx=5, side="left")

        self.sendButton = ctk.CTkButton(self.user_input, text="Send", cursor="hand2", command=self.send)
        self.sendButton.pack(side="right")


    def updateKnowledge(self, addInI=None, addInC=None):
        """addInI doit être une chaîne de caractère et addInC une liste de deux chaînes: [question,réponse]"""

        # Chargement des variables (lecture du fichier)
        with open("inutiles.txt", "r") as i:
                self.useless_words = i.read().split(' ')

        with open("connaissances.txt", "r") as c:
            for line in c:
                self.responses[line.split(":")[0]] = line.split(":")[1]

        # Ajout de connaissances dans les variables
        if addInI != None:
            self.useless_words.append(addInI)
        if addInC != None:
            self.responses[addInC[0]] = addInC[1]

        # Ecriture dans les fichiers
        with open("inutiles.txt", "w") as i:
            knowledge = ""
            for word in self.useless_words:
                knowledge += ' ' + word
            i.write(knowledge)

        with open("connaissances.txt", "w") as c:
            knowledge = ""
            for question in self.responses.keys():
                if not self.responses[question].endswith("\n"):
                    knowledge += question + ":" + self.responses[question].replace(":", "->") + "\n"
                else:
                    knowledge += question + ":" + self.responses[question].replace(":", "->")
            c.write(knowledge)

    def send(self, event=None):
        user_input = self.entry.get().strip()
        if not "/q" in user_input:
            if user_input == "":
                return

            self.show_user(user_input)

            if self.awaiting == "confirm":
                if user_input.lower() == "non":
                    self.show_bot("Dîtes moi donc ce que je dois répondre\n")
                    self.awaiting = "learn"
                elif user_input.lower() == "internet":
                    self.internet_response = self.learn_from_internet(self.last_question)
                    if self.internet_response not in ["Une erreur est survenue pendant la recherche.\n", "Je n'ai trouvé aucune page correspondante.\n"] and "Le sujet est trop vague. Vous pouvez préciser ?\n" not in self.internet_response:
                        self.show_bot(self.internet_response)
                        self.show_bot("Ai je bien répondu ? (oui / non)")
                        self.awaiting = "internet"
                    else:
                        self.show_bot(self.internet_response)
                        self.awaiting = None
                        return
                else:
                    self.show_bot("D'accord !\n")
                    self.awaiting = None
                return
            
            elif self.awaiting == "unknown":
                if user_input.lower() == "oui":
                    self.show_bot("Dîtes moi donc ce que je dois répondre\n")
                    self.awaiting = "learn"
                elif user_input.lower() == "internet":
                    self.internet_response = self.learn_from_internet(self.last_question)
                    if self.internet_response not in ["Une erreur est survenue pendant la recherche.\n", "Je n'ai trouvé aucune page correspondante.\n"] and "Le sujet est trop vague. Vous pouvez préciser ?\n" not in self.internet_response:
                        self.show_bot(self.internet_response)
                        self.show_bot("Ai je bien répondu ? (oui / non)")
                        self.awaiting = "internet"
                    else:
                        self.show_bot(self.internet_response)
                        self.awaiting = None
                        return

                else:
                    self.show_bot("D'accord !\n")
                    self.awaiting = None
                return
            
            elif self.awaiting == "internet":
                if user_input.lower() == "oui":
                    self.show_bot("D'accord ! J'enregistre donc la réponse !\n")
                    self.updateKnowledge(addInC=[self.last_question, self.internet_response])
                    self.awaiting = None
                else:
                    self.show_bot("Dîtes moi donc ce que je dois répondre\n")
                    self.awaiting = "learn"
                return

            elif self.awaiting == "learn":
                self.show_bot("Je prends ça en compte !\n")
                self.updateKnowledge(addInC=[self.last_question, user_input])
                self.awaiting = None
                return

            response = self.response(user_input.lower())
            self.last_question = user_input.lower()
            self.show_bot(response)

            if response == "Désolé, je ne comprends pas votre demande.\n":
                self.show_bot("Voulez-vous m'apprendre à répondre à ce type de question ? (oui / non / internet)\n")
                self.awaiting = "unknown"
            else:
                self.show_bot("Ai-je bien répondu ? (oui / non / internet)\n")
                self.awaiting = "confirm"
        else:
            self.updateKnowledge()
            self.destroy()

    def response(self, user_input):
        if "/q" not in user_input: 
            nbWordsKnown = 0
            nbWordsKnownMax = 0
            rightQuestion = ""
            for knownQuestion in self.responses.keys():
                for word in re.split(r"[ \'-]", user_input): # pour split selon plusieurs critères
                    if word.strip(".?!,") in knownQuestion and word.strip(".?!,") not in self.useless_words:
                        nbWordsKnown+=1
                if nbWordsKnown > nbWordsKnownMax:
                    nbWordsKnownMax = nbWordsKnown
                    rightQuestion = knownQuestion
                nbWordsKnown = 0

            if rightQuestion != "":
                return self.responses[rightQuestion]
            else:
                return "Désolé, je ne comprends pas votre demande.\n"
        else:
            self.updateKnowledge()
            self.destroy()

    def learn_from_internet(self, question):
        wikipedia.set_lang("fr")
        self.show_bot(f"Recherche sur Wikipédia pour : {question}...\n")
        resp = ""
        try:
            return wikipedia.summary(question, sentences=2, auto_suggest=False)
        except wikipedia.DisambiguationError as e:
            options = ", ".join(e.options[:5])  # Affiche quelques suggestions
            resp += "Le sujet est trop vague. Vous pouvez préciser ?\n"
            resp += f"Exemples possibles : {options}\n"
        except wikipedia.PageError:
            resp += "Je n'ai trouvé aucune page correspondante.\n"
        except Exception as e:
            resp += "Une erreur est survenue pendant la recherche.\n"
        return resp

    def show_user(self, text):
        self.chat_history.configure(state="normal", font=(("Calibri", 18, "normal")))
        self.chat_history.insert("end", f"Vous: {text}\n", "user")
        self.entry.delete(0, ctk.END)
        self.chat_history.configure(state="disabled")

    def show_bot(self, text):
        if not text.endswith("\n"):
            text += "\n"
        self.chat_history.configure(state="normal", font=(("Calibri", 18, "normal")))
        self.chat_history.insert("end", f"IA: {text}", "bot")
        self.chat_history.configure(state="disabled")

# Programme principal
self = AppIA()
self.mainloop()