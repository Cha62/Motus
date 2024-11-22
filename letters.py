import msvcrt
import random as rd
import tkinter as tk
from tkinter import messagebox

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DATABASE_PATH = "Data\Dictionnaire.txt"

def get_key():
    key = msvcrt.getch()
    if key == b'\r': # Enter
        return "Enter"
    elif key == b'\x08':  # backspace
        return "Back"
    else:
        return key.decode()
    
def select_word(path):
    """
    pick a random word is in the DataBase located in path file
    """
    file = open(path)
    lines = file.readlines()
    file.close()
    return lines[rd.randint(0,len(lines)-1)][0:-1]

def is_present(word,path):
    """
    check if the word is in the DataBase located in path file
    """
    file = open(path)
    lines = file.readlines()
    file.close()
    word = word.upper()+"\n"
    return(word in lines)

def write_word(list):
    word=""
    for e in list:
        word = word+e
    return word

class GridInterface:
    def __init__(self,word):
        self.score=0
        self.word=word
        self.nb_try=6 # nb d'essais par grille
        self.current_try=0
        self.position=1 #curseur indiquant la position de la prochaine lettre à écrire
        self.colors = ["grey", "orange", "green","lightgrey"]
        self.WIN=False
        self.LOSE=False
        self.line=[]
        self.grid=[]
        for _ in range(self.nb_try):
            for _ in range(len(word)):
                self.line.append('.')
            self.grid.append(self.line)
            self.line=[]
        self.grid[0][0]=word[0]
        self.wd = self.create_window()
        self.message_label = self.create_message_area()
        self.display()

    def create_window(self, width = 800):
        wd = tk.Tk()
        wd.title("Motus Game")
        wd.config(background="lightblue")
        height = 800 #63*len(self.word)
        wd.geometry("{}x{}".format(height,width))
        wd.bind("<Key>", self.action_clavier)
        return wd
    
    def clear_interface(self):
        for widget in self.wd.winfo_children():
            widget.destroy()

    def close_window(self):
        print("Fin du jeu")
        self.wd.destroy()
        self.wd.quit()

    def continue_prochain_mot(self):
        self.WIN = False
        self.current_try=0
        self.position=1
        self.word=select_word(DATABASE_PATH)
        print(self.word)
        self.clear_interface()
        self.line=[]
        self.grid=[]
        for _ in range(self.nb_try):
            for _ in range(len(self.word)):
                self.line.append('.')
            self.grid.append(self.line)
            self.line=[]
        self.grid[0][0]=self.word[0]
        self.message_label = self.create_message_area()
        self.display()

        #self.wd.destroy()
        #self.wd.quit()

    def display(self):
        for i in range(self.current_try,self.nb_try):
            for j in range(len(self.word)):
                label = tk.Label(self.wd,text = self.grid[i][j],width=3, height=2, font=("Arial", 24), relief="solid")
                label.grid(row=i, column=j)

    def creer_button(self, texte, commande):
        return tk.Button(self.wd, text=texte, font=("Arial", 14, "bold"), bg="lightgrey", relief='raised',  command=commande)

    def create_message_area(self):
        """Crée une zone pour afficher les messages"""
        label = tk.Label(self.wd, text=f"Tente de trouver le bon mot {self.position}", font=("Arial", 16), bg="lightblue")
        label.grid(row=self.nb_try + 1, column=0, columnspan=len(self.word), sticky="w")
        return label

    def update_message(self, message):
        """Met à jour le message affiché en bas de la fenêtre."""
        if self.WIN : 
            self.message_label.config(text=message, fg = "green")
        elif self.LOSE: 
            self.message_label.config(text=message, fg = "red")
        else:
            self.message_label.config(text=message, fg = "black")

    def choose_color(self,line):
        ''' 
        modifie les couleurs de la ligne line après que le mot soit validé
        '''
        res = [0] * len(self.word)  
        occurrences = {letter: self.word.count(letter) for letter in set(self.word)} # compteur de lettres dans le mot

        # lettres bien placées
        for i in range(len(self.word)):
            if self.grid[line][i] == self.word[i]:
                res[i] = 2
                occurrences[self.word[i]] -= 1

        # lettres présentes mais mal placées
        for i in range(len(self.word)):
            if res[i] == 0 and self.grid[line][i] in self.word:
                letter = self.grid[line][i]
                if occurrences[letter] > 0:
                    res[i] = 1
                    occurrences[letter] -= 1
        
        for k in range(len(res)):
            label = tk.Label(self.wd, text=self.grid[line][k], width=3, height=2, font=("Arial", 24), relief="solid", background=self.colors[res[k]])
            label.grid(row=line, column=k)


    def validated_word(self): # lorsque le mot a été entré
        end = self.test_end()
        if end in [-1,1]:
            return end
        self.choose_color(self.current_try)
        self.current_try+=1
        self.grid[self.current_try][0]=self.word[0]
        return 0 # The game continue

    def test_end(self):
        '''
        0 -> The game is not finished\n
        -1 -> Defeat\n
        1  -> Victory
        '''
        condition = True
        for i in range(len(self.word)):
            if self.grid[self.current_try][i]=='.':
                return 0
            if self.grid[self.current_try][i]!=self.word[i]:
                condition = False
        if condition :
            self.WIN = True
            self.score += len(self.word) * (7-self.current_try)
            self.update_message(f"Victory !! score actuel = {self.score}")
            button = self.creer_button("Prochain mot", self.continue_prochain_mot)
            button.grid(row=self.nb_try + 2, column=0, columnspan=len(self.word))
            return 1
        if self.current_try==self.nb_try-1:
            self.LOSE = True
            self.update_message("Defeat ... The correct word was : {} \n Score final = {}".format(self.word, self.score))
            button = self.creer_button("Quitter", self.close_window)
            button.grid(row=self.nb_try + 2, column=0, columnspan=len(self.word))
            return -1
        else :
            return 0
        
    def action_clavier(self, event):
        key = event.char.upper() if event.char.isalpha() else event.keysym
        self.position = self.write(key, self.position)
        self.display()

    def write(self,letter,position):
        '''
        return the new position of the letter in the word
        -1 = erreur
        '''
        if(letter=='Return'):
            if(position==len(self.word)):
                if(not is_present(write_word(self.grid[self.current_try]),DATABASE_PATH)):
                    self.update_message(f"This word doesn't exist,\n try another one... {position}")
                    return position #erreur
                self.validated_word()# == 0 à modifier + tard
                res = 1
            else :
                self.update_message(f"This word is too short,\n try another one...{position}")
                res = position #erreur
        elif(letter=='BackSpace'):
            if position==1:
                return 1
            for i in range(position -1, len(self.word)):
                self.grid[self.current_try][i] = '.'
            res = position-1
        elif(letter.upper() in ALPHABET):
            if(position >= len(self.word)):
                self.update_message(f"The maximum length has\n been reached, validate this\n word or try another one{position}")
                self.grid[self.current_try][len(self.word)-1 ]=letter.upper()
                return len(self.word)-1  #erreur
            self.grid[self.current_try][position]=letter.upper()
            res = position+1
        else :
            res = position # erreur
        return res
    
    def jeu(self):
        print("Mot sélectionné :", self.word)
        self.wd.mainloop()

jeu=GridInterface(select_word(DATABASE_PATH))
jeu.jeu()
