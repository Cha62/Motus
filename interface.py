import tkinter as tk
from tkinter import scrolledtext

def soumettre_texte(label):
    texte_saisi = zone_texte.get("1.0", "end-1c")
    label.config(text="Texte soumis : " + texte_saisi)

def effacer_texte():
    zone_texte.delete("1.0", "end")

# Créer une fenêtre
fenetre = tk.Tk()
fenetre.title("Interface avancée")

# Créer une Frame pour contenir les widgets
frame = tk.Frame(fenetre)
frame.pack(padx=20, pady=20)

# Créer une zone de texte déroulante
zone_texte = scrolledtext.ScrolledText(frame, height=10, width=40, wrap=tk.WORD)
zone_texte.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Créer un bouton pour soumettre le texte
bouton_submit = tk.Button(frame, text="Soumettre", command=lambda: soumettre_texte(label_resultat))
bouton_submit.grid(row=1, column=0, padx=5, pady=5)

# Créer un bouton pour effacer le texte
bouton_effacer = tk.Button(frame, text="Effacer", command=effacer_texte)
bouton_effacer.grid(row=1, column=1, padx=5, pady=5)

# Créer une étiquette pour afficher le résultat
label_resultat = tk.Label(fenetre, text="Texte soumis : ")
label_resultat.pack(padx=20, pady=10)

# Lancer la boucle principale
fenetre.mainloop()
