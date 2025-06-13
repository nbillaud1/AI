import customtkinter as ctk

# Envoie de la quesion
def send(event=None):
    question = entry.get()
    bot_resp = response(entry.get())
    if question.strip() != "":
        entry.delete(0, ctk.END)
        chat_history.configure(state="normal")
        chat_history.insert("end", f"Vous: {question}\n", "user")
        chat_history.insert("end", f"IA: {bot_resp}\n", "bot")
        chat_history.configure(state="disabled")

# Réponse
def response(user_input):
    nbWordsKnown = 0
    nbWordsKnownMax = 0
    rightQuestion = ""
    responses = {
        "bonjour": "Bonjour, ça va ?",
        "tu es une ia ?": "oui, mais selon certains je deviendrai vite meilleur que toi, sombre idiot !",
        "au revoir": "A plus !"
    }
    for knownQuestion in responses.keys():
        for word in user_input.strip():
            if word in knownQuestion:
                nbWordsKnown+=1
        if nbWordsKnown > nbWordsKnownMax:
            nbWordsKnownMax = nbWordsKnown
            rightQuestion = knownQuestion
        nbWordsKnown = 0

    if user_input.lower() in responses:
        return responses[rightQuestion]
    else:
        return "Désolé, je ne comprends pas votre demande."


# Création de l'app
app = ctk.CTk()
app.geometry("500x600")
app.title("IA")

# Création de l'en-tête
header = ctk.CTkLabel(app, text="Bienvenue !", font=("Calibri", 18, "bold"))
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