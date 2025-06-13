import customtkinter as ctk
import re

useless_words = []
responses = {}

# Connaissances de base
# bonjour:Bonjour, que puis-je faire pour vous ?
# au revoir:Au revoir !
# tu est une ia:Absolument, une Infinie Alcoolique !
# ok:Y'a t'il autre chose que je peux faire pour vous ?
# accord:Y'a t'il autre chose que je peux faire pour vous ?
# merci:Y'a t'il autre chose que je peux faire pour vous ?

with open("inutiles.txt", "r") as i:
    useless_words = i.read().split()

with open("connaissances.txt", "r") as c:
    for line in c:
        responses[line.split(":")[0]] = line.split(":")[1]

def updateKnowledge():
    with open("inutiles.txt", "w") as i:
        knowledge = ""
        for word in useless_words:
            knowledge += ' ' + word
        i.write(knowledge)

    with open("connaissances.txt", "w") as c:
        knowledge = ""
        for question in responses.keys():
            if not responses[question].endswith("\n"):
                knowledge += question + ":" + responses[question] + "\n"
            else:
                knowledge += question + ":" + responses[question]
        c.write(knowledge)

# Envoie de la quesion
def send(event=None):
    question = entry.get()
    bot_resp = response(entry.get().lower())
    if question.strip() != "":
        entry.delete(0, ctk.END)
        chat_history.configure(state="normal", font=(("Calibri", 18, "normal")))
        chat_history.insert("end", f"Vous: {question}\n", "user")
        chat_history.insert("end", f"IA: {bot_resp}\n", "bot")
        chat_history.configure(state="disabled")

# Réponse
def response(user_input):
    if "/q" not in user_input: 
        nbWordsKnown = 0
        nbWordsKnownMax = 0
        rightQuestion = ""
        for knownQuestion in responses.keys():
            for word in re.split(r"[ \'-]", user_input): # pour split selon plusieurs critères
                if word in knownQuestion and word not in useless_words:
                    nbWordsKnown+=1
            if nbWordsKnown > nbWordsKnownMax:
                nbWordsKnownMax = nbWordsKnown
                rightQuestion = knownQuestion
            nbWordsKnown = 0

        if rightQuestion != "":
            return responses[rightQuestion]
        else:
            return "Désolé, je ne comprends pas votre demande."
    else:
        updateKnowledge()
        app.destroy()


# Création de l'app
app = ctk.CTk()
app.geometry("500x600")
app.overrideredirect(True)
app.title("IA (Infiniment Alcoolique)")

# Création de l'en-tête
header = ctk.CTkLabel(app, text="Bienvenue ! pour quitter entrez /q", font=("Calibri", 20, "bold"))
header.pack(pady=10)

# Création de l'affichage des messages
chat_history = ctk.CTkTextbox(app, width=480, height=450, state="disabled")
chat_history.pack(pady=10, padx=10, fill="both", expand=True)
# Ajout des couleurs pour le bot et le user
chat_history.tag_config("user", foreground="blue")
chat_history.tag_config("bot", foreground="red")

# Création du champs de saisie
user_input = ctk.CTkFrame(app)
user_input.pack(pady=10, padx=10, fill="x")

entry = ctk.CTkEntry(user_input, placeholder_text="Entrez votre texte ici !", width=400)
entry.pack(padx=5, side="left")

sendButton = ctk.CTkButton(user_input, text="Send", cursor="hand2", command=send)
sendButton.pack(side="right")

# Associer la touchee entrée à l'envoie du message
app.bind("<Return>", send)


app.mainloop()