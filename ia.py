import customtkinter as ctk

#Réponse
def response(user_input):
    responses = {
        "Bonjour": "Bonjour, ça va ?",
        "tu es une IA ?": "oui, mais selon certains je deviendrai vite meilleur que toi, sombre idiot !",
        "Au revoir": "A plus !"
    }
    user_input = user_input.strip()
    if user_input in responses:
        return responses[user_input]
    else:
        return "Je ne comprends pas votre demande."


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
#Ajout des couleurs pour le bot et le user
chat_history.tag_config("user", foreground="blue")
chat_history.tag_config("bot", foreground="red")

# Création du champs de saisie
user_input = ctk.CTkFrame(app)
user_input.pack(pady=10, padx=10, fill="x")

entry = ctk.CTkEntry(user_input, placeholder_text="Entrez votre texte ici !", width=400)
entry.pack(padx=5, side="left")

send = ctk.CTkButton(user_input, text="Send", cursor="hand2")
send.pack(side="right")

app.mainloop()