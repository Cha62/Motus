import msvcrt

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def get_key():
    key = msvcrt.getch()
    if key == b'\r': # Enter
        return "Enter"
    elif key == b'\x08':  # backspace
        return "Back"
    else:
        return key.decode()

class Grid:
    def __init__(self,word):
        self.word=word
        self.nb_try=6 # nb d'essais par grille
        self.current_try=0
        self.position=1 #curseur indiquant la position de la prochaine lettre à écrire
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
        
    def display(self):
        for i in range(self.nb_try):
            for j in range(len(self.word)):
                print(self.grid[i][j],end='|')
            print('\n_______________')

    def validated_word(self):
        end = self.test_end()
        if end in [-1,1]:
            return end
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
            return 1
        if self.current_try==self.nb_try-1:
            self.LOSE = True
            return -1
        else :
            return 0


    def write(self,letter,position):
        '''
        return the new position of the letter in the word
        -1 = erreur
        '''
        if(letter=='Enter'):
            if(position==len(self.word)):
                self.validated_word()
                return 1
            else :
                return -1 #erreur
        elif(letter=='Back'):
            if position==1:
                return -1
            self.grid[self.current_try][position-1]='.'
            return position-1
        elif(letter.upper() in ALPHABET):
            print("position = {}, len(word)-1 = {} ".format(position,len(self.word)-1))
            if(position==len(self.word)):
                return -1
            self.grid[self.current_try][position]=letter.upper()
            return position+1
        return -1
    
    
    def jeu(self):
        while not (self.WIN or self.LOSE):
            pos_temp = self.position # variable pour sauvegarder la position courante
            self.display()
            letter=get_key()
            self.position=self.write(letter,self.position)
            while self.position==-1:
                letter=get_key()
                self.position=self.write(letter,pos_temp)
        if self.WIN :
             print("win")
        else:
            print("lose")


            
jeu=Grid("BLABLA")
jeu.jeu()