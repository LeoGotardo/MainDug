from pymongo import MongoClient
import Debug as d
import os


class Model:
    def __init__(self):
        os.system("cls")
        # Configuração de conexão com o MongoDB
        self.root = "LeoGotardo"
        self.password = "GUDP6TDvj9vdzGEH"
        self.CONNECTION_STRING = f"mongodb+srv://{self.root}:{self.password}@cluster0.gcolnp2.mongodb.net/"
        self.client = MongoClient(self.CONNECTION_STRING)
        self.bd = self.client["Belle"]
        self.Logins = self.bd["Logins"]


        # Lista para armazenar mensagens de erro
        self.error = []

        # Debug: exibe o conteúdo da coleção.
        print(f"{d.Margin}Connection String:{MongoClient(self.CONNECTION_STRING)}{d.Margin}")

    def cad(self, login, Password):
        # Adiciona um novo usuário à coleção 'Logins'
        User = {
            "Login": login,
            "Password": Password
        }
        self.Logins.insert_one(User)

        return id  # Retorna o ID do usuário (não está implementado corretamente)


    def verifyLogin(self, login):
        # Verifica se um login específico existe na coleção 'Logins'
        hasLogin = self.has(login)

        if hasLogin == False: 
            print(d.Margin,"Has Login:",hasLogin, d.Margin)
            return True
        else:
            print(d.Margin,"Has Login:",hasLogin, d.Margin)
            return False


    def valid(self, login, password):
        # Verifica se um login e senha são válidos
        if self.verifyLogin(login, "Login") == False:
            self.validPass(login,password)


    def has(self, Name):
        # Retorna uma lista de todos os logins na coleção 'Logins'
        every = self.Logins.find({"Login": Name})
        logins = []

        for result in every:
            logins.append(result["Login"])
            
        if len(logins) == 0:
            logins.append(1)

        if type(logins[0]) == 'bson.objectid.ObjectId':
            self.error[0] = "Login alrady exists"
            return self.error
        else:
            return False



    def credencialADD(self, login, password, passwordCondirm):
        # Adiciona credenciais se válidas, caso contrário, retorna uma mensagem de error
        if self.passValid(password, passwordCondirm) == True:
            if self.has == False:
                self.cad(login, password)
                self.error[0] = "Valid Login"
                return self.error
            else:
                self.error[0] = "This user alredy exists."
                return self.error
        else:
            self.error[0] = "Passwords do not metch"
            return self.error


    def verify(self, login, password):
        # Verifica se um login e senha são válidos e retorna o ID do usuário
        if self.verifyLogin(login) == False:
            if self.validPass(login, password) == True:
                ret = self.findID(login, password)

                ret.append(None)
                
                if ret[1] == True:
                    return ret
            else:
                ret = [False, None, "Invalid Login"]
                
                return ret
        else:  
            ret = [False, None, "Invalid Login"]

            print(d.Margin, ret, d.Margin)
            return ret



    def loginValid(self, login):
        # Verifica se um login é válido
        if self.verifyLogin(login) == True and login != "":
            return True
        else:
            return False


    def passValid(self, password, passwordConfirm):
        # Verifica se uma senha é válida
        if password == passwordConfirm and password == "" or passwordConfirm == "":
            self.error[0] = "Invalid Password"
            return False
        else:
            self.error[0] = "Invalid Password"
            return False


    def validPass(self, login, password):
        # Verifica se um login e senha são válidos
        login = self.Logins.find({"$and": [{"Login": login}, {"Password": password}]})
        
        if login != []:
            return True
        else:
            return False 
        

    def isNew(self, id, paramter, new):
        if paramter == "login":
            login = self.Logins.find({'_id': id}, {'Login': new})
            logins = []

            for result in login:
                logins.append(result["Login"])
            if type(logins[0]) == 'bson.objectid.ObjectId':
                self.error[1] = f"Login is alredy {new}"
                print(f"{d.Margin}login:{login}\nlogins: {logins}\nlogin type = {type(logins[0])}{d.Margin}")
                return "notNew"
            else:
                print(f"{d.Margin}login:{login}\nlogins: {logins}\nlogin type = {type(logins[0])}{d.Margin}")
                return "new"
            
        elif paramter == "password":
            password = self.Logins.find({'_id': id}, {'Password': new})
            passwords = []

            for result in password:
                passwords.append(result["Password"])
            print(f"{d.Margin}Passwords: {passwords}{d.Margin}")
            if type(passwords[0]) == 'bson.objectid.ObjectId':
                self.error[1] = f"Password is alredy {new}"
                print(f"{d.Margin}Password:{password}\nPasswords: {passwords} {d.Margin}")
                return "notNew"
            else:
                print(f"{d.Margin}Password:{password}\nPasswords: {passwords} {d.Margin}")
                return "new"
            
        else:
            return "Invalid Paramter"


    def edit(self, user_id, parameter, newPar):
        # Atualiza informações de um usuário na coleção 'Logins'
        if parameter == "login":
            self.Logins.update_one({'_id': user_id} ,{'$set': {"Login":newPar}})
            done = f"Login of {user_id} updated to {newPar}"
            return done
        elif parameter == "password":
            self.Logins.update_one({'_id': user_id} ,{'$set': {"Password":newPar}})
            done = f"Password updated to {newPar}"
            return done
        else:
            self.error[1] = "Paramter_Error"
            return self.error



    def findID(self, login, password):
        # Encontra o ID de um usuário com base no login e a senha
        ret = []

        id = self.Logins.find({"$and": [{"Login": login}, {"Password": password}]})

        for result in id:
            ret.append(result["_id"])  
        if len(ret) == 0:
            ret.append(None)

        print(d.Margin, "Findded ID:", d.Red,ret, "Id Type = ", type(ret[0]), d.Margin)

        if type(id) != []:
            ret.append(True)
        else:
            ret.append(False)

        print(f"{d.Margin}{d.Red}{ret}{d.Margin}")
        return ret


    def erase(self, id):
        # Exclui um usuário com base no ID
        self.Logins.delete_one({'_id':id})
        print(f"{d.Margin}Sucsses.{d.Margin}")
        return True


if __name__ == "__main__":
    # Instância um objeto Model para testar a classe
    model = Model()
