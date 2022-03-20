

# COMMANDS = ['migrate', 'init', 'upgrade',
#             'Ctrl+C (to breack)', 'run dev', 'rebuild', 'run prod', 'db',
#             'clean v', 'clean sys', 'seed', 'allmigrations', "heroku-push", "heroku-add"]

# Access .env file
from decouple import config
from os import path
import subprocess
DB_USERNAME = config("POSTGRES_USER_DEV")
DB = config("POSTGRES_DB_DEV")


# def runApp() -> str:
#     print("Please use the following commands to continue")
#     for command in COMMANDS:
#         print(f"{[command]}", sep=',', end=' ')
#     print("\n")
#     insert_input = input("[@nk]> ")

#     if insert_input in COMMANDS and insert_input == COMMANDS[1]:
#         print("It's the first time to run migration, \nPlease wait...")
#         subprocess.run(
#             "sudo docker-compose exec dev python3 manage.py db init", check=True,
#             shell=True, executable="/bin/bash"
#         )
#     elif insert_input in COMMANDS[0:3] and insert_input != COMMANDS[1]:
#         if path.isdir('services/app/migrations/') == True:
#             print(f"""** migrations ** folder already exists. \n""")
#             if insert_input == COMMANDS[0]:
#                 subprocess.run(
#                     "sudo sudo docker-compose exec dev python3 manage.py db migrate", check=True,
#                     shell=True, executable="/bin/bash"
#                 )
#             if insert_input == COMMANDS[2]:
#                 subprocess.run(
#                     "sudo sudo docker-compose exec dev python3 manage.py db upgrade", check=True,
#                     shell=True, executable="/bin/bash"
#                 )
#             elif insert_input == COMMANDS[10]:
#                 subprocess.run(
#                     "sudo docker-compose exec dev python3 manage.py db stamp head", check=True,
#                     shell=True, executable="/bin/bash"
#                 )
#     elif insert_input in COMMANDS:
#         if insert_input == COMMANDS[5]:
#             subprocess.run(
#                 "sudo docker-compose up --build dev", check=True,
#                 shell=True, executable="/bin/bash"
#             )
#         elif insert_input == COMMANDS[4]:
#             subprocess.run(
#                 "sudo docker-compose up dev", check=True,
#                 shell=True, executable="/bin/bash"
#             )
#         elif insert_input == COMMANDS[6]:
#             subprocess.run(
#                 "sudo docker-compose up prod", check=True,
#                 shell=True, executable="/bin/bash"
#             )
#         elif insert_input == COMMANDS[7]:
#             subprocess.run(
#                 f"sudo docker-compose exec db psql --username={DB_USERNAME} --dbname={DB}", check=True,
#                 shell=True, executable="/bin/bash"
#             )
#         elif insert_input == COMMANDS[8]:
#             subprocess.run(
#                 "sudo docker-compose down -v", check=True,
#                 shell=True, executable="/bin/bash"
#             )
#         elif insert_input == COMMANDS[9]:
#             subprocess.run(
#                 "sudo docker-compose down", check=True,
#                 shell=True, executable="/bin/bash"
#             )
#         elif insert_input == COMMANDS[10]:
#             subprocess.run(
#                 "sudo docker-compose exec dev python manage.py seed_db", check=True,
#                 shell=True, executable="/bin/bash"
#             )
#         elif insert_input == COMMANDS[12]:
#             subprocess.run(
#                 "git subtree add --prefix services/app", check=True,
#                 shell=True, executable="/bin/bash"
#             )
#         # git commit to heroku git  commit -am
#         # heroku open
#         # sudo heroku create fuko-backend
#         # sudo  heroku  git:remote -a fuko-backend
#         # sudo heroku run python3 manage.py db migrate -m "Initial migrations" --app fuko-backend
#         # sudo heroku run python3 manage.py db migrate --app fuko-backend
#         # sudo heroku run python3 manage.py db upgrade --app fuko-backend
#         # ----------------------------------------------------------------------------------------
#         # git push heroku ft-config-swagger:master
#         elif insert_input == COMMANDS[13]:
#             subprocess.run(
#                 "git subtree push --prefix services/app/ heroku master:main", check=True,
#                 shell=True, executable="/bin/bash"
#             )

#     else:
#         print("Command not found. \nProcess end.")


# def runApp():
#     while True:
#         getInput = input("Enter something: ")
#         if getInput in itemData:
#             print("Found it")
#             getInput
#         else:
#             print("Not found")
#         continue


class ManageInput:
    item_data: list = ['migrate', 'init', 'upgrade',
                       'Ctrl+C (to break)', 'run dev', 'rebuild', 'run prod', 'db',
                       'clean v', 'clean sys', 'seed', 'allmigrations', "heroku add"
                       "heroku-push", "heroku-add"]

    def __init__(self) -> None:
        self.get_command = self.commands()

    def commands(self) -> dict:

        return {
            "init":  "sudo docker-compose exec dev python3 manage.py db init",
            "migrate": "sudo sudo docker-compose exec dev python3 manage.py db migrate",
            "upgrade": "sudo sudo docker-compose exec dev python3 manage.py db upgrade",
            'run dev': "sudo docker-compose up dev",
            'rebuild': "sudo docker-compose up --build dev",
            'run prod': "sudo docker-compose up prod",
            'db': f"sudo docker-compose exec db psql --username={DB_USERNAME} --dbname={DB}",
            'clean v': "sudo docker-compose down -v",
            'clean sys': "sudo docker-compose down",
            'seed': "sudo docker-compose exec dev python manage.py seed_db",
            'allmigrations': "sudo docker-compose exec dev python3 manage.py db stamp head",
            # Heroku section
            "add": "git subtree add --prefix services/app",
            "com": f"git  commit -am ",
            "push": "git push heroku ft-config-swagger:main",
            "init-migrate": "sudo heroku run python3 manage.py db migrate -m 'Initial migrations' --app fuko-backend",
            "migrate-db": "sudo heroku run python3 manage.py db migrate --app fuko-backend",
            "upgrade-db": "sudo heroku run python3 manage.py db upgrade --app fuko-backend"
        }

    def getInput(self):
        try:
            while True:
                getInput = input("[@nk]> ")
                if getInput in self.get_command:
                    try:
                        subprocess.run(self.get_command[getInput],
                                       check=True, shell=True, executable="/bin/bash")
                        getInput
                    except subprocess.CalledProcessError:
                        getInput

                if getInput == "heroku":
                    print("Push the app on server.")
                    herInput = input("[@nk] heroku> ")
                    if herInput in self.get_command:
                        addOperation = input("Add branch or commit > ")
                        subprocess.run(f"{self.get_command[herInput]} '{addOperation}'",
                                       check=True, shell=True, executable="/bin/bash")
                        herInput
                    else:
                        print("Command Not found!")
                        herInput

                else:
                    print("Command Not found!")
                    getInput
                continue
        except KeyboardInterrupt:
            print("You left the system")


if __name__ == "__main__":
    import subprocess

    run_app = ManageInput()
    run_app.getInput()
