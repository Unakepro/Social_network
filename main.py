import time
from datetime import datetime
import re
import json

now = datetime.now()
date_time = now.strftime("%Y-%m-%d")

with open('data_file.json') as f:
    data = json.load(f)


class Register:

    def __init__(self, username, password, password_c):
        self._username = username
        self._password = password
        self._password_c = password_c

    @property
    def getter(self):
        return self._username, self._password, self._password_c

    def check_username(self):

        try:
            return data['accounts'][self._username]
        except KeyError:

            if 5 > len(self._username) or len(self._username) > 12:
                print("Invalid Nick")
            elif not re.search("[a-z]", self._username):
                print("Invalid Nick")
                pass
            elif not re.search("[A-Z]", self._username):
                print("Invalid Nick")
                pass
            else:
                Register.check_password(self)

    def check_password(self):

        if 5 > len(self._password) or len(self._password) > 12:
            print("Invalid Pass")
            pass
        elif not re.search("[a-z]", self._password):
            print("Invalid Pass")
            pass
        elif not re.search("[0-9]", self._password):
            print("Invalid Pass")
            pass
        elif not re.search("[A-Z]", self._password):
            print("Invalid Pass")
            pass
        else:
            Register.confirm_password(self)

    def confirm_password(self):
        if self._password == self._password_c:

            print("You have registered!!!!!")
            data['accounts'][self._username] = [self._password, date_time]
            Authorization.your_name = self._username
            with open("data_file.json", "w") as write_file:
                json.dump(data, write_file)

        else:
            print("You have entered 2 different passwords\n")


class Authorization:
    your_name = None

    def __init__(self, user, password):
        self._user = user
        self._password = password

    @property
    def getter(self):
        return self._user, self._password

    def authorize(self):
        if self._user in data['accounts'].keys():
            if self._password == data['accounts'][self._user][0]:
                print("You have logged in")
                Authorization.your_name = self._user
            else:
                print("Wrong pass, please check spelling")
        else:
            print("\nUsername does not exist")


class Choice:
    stop = None

    def __init__(self, way, message):
        self._way = way
        self._message = message

    @property
    def getter(self):
        return self._way, self._message

    @staticmethod
    def start_text():
        print("\nHello this is Social_network_in_terminal what do you want: ")
        time.sleep(1.5)
        print("1: login, 2: register")

    @staticmethod
    def start_admin():
        print("\nAs admin you can do this:")
        time.sleep(1)
        print("1: View all posts, 2: See users and registration time, 3: Add post, 4: Exit")

    @staticmethod
    def start_user():
        print(f"\nHello {Authorization.your_name} you can do this:")
        time.sleep(1.5)
        print("1: Add post,2: View post, 3: Exit")

    def do_user(self):

        if self._way == 1:
            try:
                data["posts"][Authorization.your_name].append(self._message)
                data["posts"][Authorization.your_name].append(date_time)
            except KeyError:
                data["posts"][Authorization.your_name] = [self._message, date_time]
                with open("data_file.json", "w") as write_file:
                    json.dump(data, write_file)

            print("Successful \n")

        elif self._way == 2:
            try:
                print(data["posts"][Authorization.your_name])
            except KeyError:
                print("You haven't got any posts")

        else:
            Choice.stop = 0

    def do_admin(self):
        if self._way == 1:
            for keys, values in data['posts'].items():
                print(f"\n{keys}  : {values}\n")

        elif self._way == 2:
            for values, keys in data['accounts'].items():
                print(values + " : " + keys[1] + "\n")

        elif self._way == 3:
            data["posts"]["admin"].append(self._message)
            data["posts"]["admin"].append(date_time)

        else:
            Choice.stop = 0


while True:
    Authorization.your_name = None
    Choice.stop = 1

    Choice.start_text()

    try:
        choice = int(input("Type 1 or 2: "))
    except ValueError:
        continue

    if choice == 1:
        Username = input("Enter username: ")
        Password = input("Enter password: ")

        Authorization(Username, Password).authorize()

    else:
        Username = input("Enter username: ")
        Password = input("Enter password: ")
        C_password = input("Confirm password: ")

        Register(Username, Password, C_password).check_username()
    if Authorization.your_name is None:
        continue

    while Choice.stop == 1:
        if Authorization.your_name == "admin":
            Choice.start_admin()

            try:
                ask = int(input("Type number: "))
                if ask == 3:
                    post = input("Type your post: ")
                    Choice(ask, post).do_admin()
                else:
                    Choice(ask, None).do_admin()

            except ValueError:
                pass

        else:
            Choice.start_user()

            try:
                ask = int(input("Type number: "))
                if ask == 1:
                    post = input("Type your post: ")
                    Choice(ask, post).do_user()
                else:
                    Choice(ask, None).do_user()
            except ValueError:
                pass
