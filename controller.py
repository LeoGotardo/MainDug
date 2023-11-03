from model import Model

class Controller:
    def __init__(self) -> None:
        self.m = Model()
        

    def start(self):
        self.m
        return True
    

    def credencialADD(self, login, password, passwordConfirm):
        return self.m.credencialADD(login, password, passwordConfirm)


    def cad(self, login, password):
        return self.m.cad(login, password)


    def veryLogin(self, login):
        return self.m.verifyLogin(login)
        

    def verify(self, login, password):
        itens = self.m.verify(login, password)
        return itens
        

    def erase(self, id):
        return self.m.erase(id)
        

    def valid(self, login, password):
        return self.m.valid(login, password)

if __name__ == "__main__":
    controller = Controller()
