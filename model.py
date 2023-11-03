from pymongo import MongoClient


class Model:
    def __init__(self):
        self.root = "LeoGotardo"
        self.password = "GUDP6TDvj9vdzGEH"
        self.CONNECTION_STRING = f"mongodb+srv://{self.root}:{self.password}@cluster0.gcolnp2.mongodb.net/"

        self.client = MongoClient(self.CONNECTION_STRING)
        self.bd = self.client["Belle"]
        self.Login = self.bd["Logins"]

        self.error = []

        print(self.client['user_shopping_list'])


    def cad(self, login, Password):
        User = {
            "login": login,
            "Password": Password
        }

        self.Login.insert_one(User)

        return id
    

    def verifyLogin(self, login):
        has = self.has(login)
        
        if has != []:
            return True
        else:
            return False
        

    def valid(self, login, password):
        if self.verifyLogin(login, "Login") == False:
            self.validPass(password)


    
    def has(self, Name, ):
        every = self.Login.find({"login":Name})
        self.logins = []
        self.coll = None

        for result in every:
            self.logins.append(result["login"])
        return self.logins
    

    def credencialADD(self, login, password, passwordCondirm):
        if self.credencialValid(login, password, passwordCondirm) == True:
            self.cad(login, password)
            return "Valid Cadaster"
        else:
            return self.error


    def credencialValid(self, login, password, passwordConfirm):
        if self.loginValid(login) == True:
            if self.passValid(password, passwordConfirm) == True:
                validPass = True
                return validPass
            else:
                self.error.append("Invalid Passoword")
                return False
        else:
            self.error.append("Invalid Login")
            return False


    def verify(self, login, password):
        if self.verifyLogin(login) == False:
            if self.validPass(password) == True:
                ret = self.findID(login)
                id = ret[1]
                valid = ret[0]
                if valid == True:
                    return id
            else:
                return self.error.append("Invalid Password")
        else:
            self.error.append("Invalid Login")
            return self.error
        

    def loginValid(self, login):
        if self.verifyLogin(login) == True or login != "":
            return True
        else:
            return False


    def passValid(self, password, passwordConfirm):
        if password == passwordConfirm:
            return True
        elif password == "" or passwordConfirm == "":
            return False
        else:
            self.error.append("Invalid Passoword")


    def validPass(self, login, password):
        login = self.Login.find({"login":login} and {"Password":password})
        
        if login == []:
            return False
        else:
            return True 


    def edit(self, id, paramter):
        self.Login.update_one({})


    def findID(self, login):
        id = self.Login.find({"login":login})
        return id


    def erase(self, id):
        self.Login.delete_one({id})


if __name__ == "__main__":
    model = Model()
