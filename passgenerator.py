from alive_progress import alive_bar, config_handler
import random as r
import Debug as d
import string
import os


class Generator:
    def __init__(self):
        self.let = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        self.may = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        self.sim = ['!','@','#','$','%','¨','&','*','(',')','+','=','|','<','>',':',';','?']
        self.numb = ['0','1','2','3','4','5','6','7','8','9']
    
        self.cls = os.system("cls")
    
    def gerator(self, resp):
        config_handler.set_global(length=50)

        print(d.Margin)

        password = []
        fin = []
        num = resp[0]
        letter = resp[1]
        symb = resp[2]
        maius = resp[3]
        syze = resp[4]

        if num == True:
            for i in range(len(self.numb)):
                fin.append(self.numb[i])
        if letter == True:
            for i in range(len(self.let)):
                fin.append(self.let[i])
        if symb == True:
            for i in range(len(self.sim)):
                fin.append(self.sim[i])
        if maius == True:
            for i in range(len(self.may)):
                fin.append(self.may[i])
                
        with alive_bar(syze, title="Generating your password...") as bar:
            for i in range(syze):
                act = r.choice(fin)
                password.append(act)
                bar()
        fin_pass = ''.join(password)

        return fin_pass

if __name__ == "__main__":
    Generator = Generator()