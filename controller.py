from model import Model

class Controller:
    def __init__(self) -> None:
        # Inicializa um objeto Model na instância do Controller
        self.m = Model()

    def start(self):
        # Inicia a instância do Model (não faz nada substancial no código fornecido)
        self.m
        return True

    def credencialADD(self, login, password, passwordConfirm):
        # Chama a função credencialADD do Model e retorna o resultado
        return self.m.credencialADD(login, password, passwordConfirm)

    def cad(self, login, password):
        # Chama a função cad do Model e retorna o resultado
        return self.m.cad(login, password)

    def veryLogin(self, login):
        # Chama a função verifyLogin do Model e retorna o resultado
        return self.m.verifyLogin(login)

    def verify(self, login, password):
        # Chama a função verify do Model e retorna o resultado
        return self.m.verify(login, password)

    def erase(self, id):
        # Chama a função erase do Model e retorna o resultado
        return self.m.erase(id)

    def edit(self, id, parameter, new):
        # Chama a função edit do Model e rotorna o resultado
        return self.m.edit(id, parameter, new)

    def valid(self, login, password):
        # Chama a função valid do Model e retorna o resultado
        return self.m.valid(login, password)
    
    def same(self, id, paramter, new):
        # Chama a função isNew do Model e retorna o resultado
        return self.m.isNew(id, paramter, new)

if __name__ == "__main__":
    # Cria uma instância do Controller para testar a classe
    controller = Controller()
