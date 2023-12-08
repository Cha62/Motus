import msvcrt



ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def get_key():
    key = msvcrt.getch()
    if key == b'\r':
        return "Enter"
    elif key == b'\x08':  # Detection de la touche de suppression (Backspace)
        return "Back"
    else:
        return key.decode()

class Grid:
    def __init__(self,word):
        self.word=word
        self.nb_try=6
        self.current_try=0
        self.line=[]
        self.grid=[]
        for _ in range(self.nb_try):
            for _ in range(len(word)):
                self.line.append('.')
            self.grid.append(self.line)
            self.line=[]
        self.grid[0][0]=word[0]
        
    def display(self):
        for i in range(self.nb_try):
            for j in range(len(self.word)):
                print(self.grid[i][j],end='|')
            print('\n_______________')

    def validated_word(self):
        self.current_try+=1
        self.grid[0][self.current_try]=self.word[0]


    def write(letter,position):
        if(letter=='Enter'):
            if(position==len(self.word)-1):
                validated_word()
                return position
            else :
                return -1
        elif(letter=='Back'):
            self.grid[position-1][self.current_try]='.'
            return position-1
        elif(letter in ALPHABET):
            self.grid[position][self.current_try]=letter
            return position
        return -1

            
jeu=Grid("blabla")
jeu.display()