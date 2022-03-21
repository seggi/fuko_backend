
# Access .env file
from decouple import config
from os import path
import subprocess
DB_USERNAME = config("POSTGRES_USER_DEV")
DB = config("POSTGRES_DB_DEV")


class ManageInput:
    item_data: list = ['migrate', 'init', 'upgrade',
                       'Ctrl+C (to break)', 'run dev', 'rebuild', 'run prod', 'db',
                       'clean v', 'clean sys', 'seed', 'allmigrations', "heroku add"
                       "heroku-push", "heroku-add"]

    def __init__(self) -> None:

        print("Please use the following commands to continue")
        for command in self.item_data:
            print(f"{[command]}", sep=',', end=' ')
        print("\n")
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
            "push": "git push heroku ",
            "init-migrate": "sudo heroku run python3 manage.py db migrate -m 'Initial migrations' --app fuko-backend",
            "db-history": "sudo heroku run python3 manage.py db history --app fuko-backend",
            "stamp-db": "sudo heroku run python3 manage.py db stamp head --app fuko-backend",
            "migrate-db": "sudo heroku run python3 manage.py db migrate --app fuko-backend",
            "upgrade-db": "sudo heroku run python3 manage.py db upgrade --app fuko-backend",
            "heroku-db": "heroku pg:psql"
        }

    def display_input(self):
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
                if herInput in self.get_command and herInput == 'com':
                    addOperation = input("Add commit > ")
                    subprocess.run(f"{self.get_command[herInput]} '{addOperation}'",
                                   check=True, shell=True, executable="/bin/bash")
                    herInput
                elif herInput in self.get_command and herInput == 'push':
                    print("Add change like current-branch:main")
                    addOperation = input("Add branch > ")
                    subprocess.run(f"{self.get_command[herInput]} {addOperation}",
                                   check=True, shell=True, executable="/bin/bash")
                    herInput
                else:
                    print("Command Not found!")
                    herInput
            elif getInput == "back":
                getInput
            else:
                print("Command Not found!")
                getInput
            continue

    def getInput(self):
        try:
            self.display_input()
        except KeyboardInterrupt:
            print("Abort the system ?\n Enter y to cancel & n to continue: ")
            try:
                get_input = input("> ")
                if get_input == "n":
                    self.display_input()
                else:
                    print("You left...")
            except KeyboardInterrupt:
                print("Error...")


if __name__ == "__main__":
    import subprocess

    run_app = ManageInput()
    run_app.getInput()
