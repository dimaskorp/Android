import datetime


class DataBase:
    def __init__(self, filename):
        self.filename = filename
        self.users = None
        self.file = None
        self.load()

    def load(self):
        self.file = open(self.filename, "r")
        self.users = {}

        for line in self.file:
            name, password, created = line.strip().split(";")
            self.users[name] = (password, created)

        self.file.close()

    def get_user(self, login):
        if login in self.users:
            return self.users[login]
        else:
            return -1

    def add_user(self, name, password, ):
        if name.strip() not in self.users:
            self.users[name.strip()] = (password.strip(), DataBase.get_date())
            self.save()
            return 1
        else:
            print("Данный номер уже существует")
            return -1

    def validate(self, login, password):
        if self.get_user(login) != -1:
            return self.users[login][0] == password
        else:
            return False

    def save(self):
        with open(self.filename, "w", ) as f:
            for user in self.users:
                f.write(user + ";" + self.users[user][0] + ";" + self.users[user][1] + "\n")

    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]