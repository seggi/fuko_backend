import subprocess
from os import path
from decouple import config

COMMANDS = ['migrate', 'init', 'upgrade',
            'Ctrl+C (to breack)', 'run dev', 'rebuild', 'run prod', 'db', 'clean v', 'clean sys', 'seed', 'allmigrations']

# Access .env file
DB_USERNAME = config("POSTGRES_USER_DEV")
DB = config("POSTGRES_DB_DEV")


def runApp() -> str:
    print("Please use the following commands to continue")
    for command in COMMANDS:
        print(f"{[command]}", sep=',', end=' ')
    print("\n")
    insert_input = input("[@nk]> ")

    if insert_input in COMMANDS and insert_input == COMMANDS[1]:
        print("It's the first time to run migration, \nPlease wait...")
        subprocess.run(
            "docker-compose exec dev python3 manage.py db init", check=True,
            shell=True, executable="/bin/bash"
        )
    elif insert_input in COMMANDS[0:3] and insert_input != COMMANDS[1]:
        if path.isdir('services/app/migrations/') == True:
            print(f"""** migrations ** folder already exists. \n""")
            if insert_input == COMMANDS[0]:
                subprocess.run(
                    "docker-compose exec dev python3 manage.py db migrate", check=True,
                    shell=True, executable="/bin/bash"
                )
            if insert_input == COMMANDS[2]:
                subprocess.run(
                    "docker-compose exec dev python3 manage.py db upgrade", check=True,
                    shell=True, executable="/bin/bash"
                )
            elif insert_input == COMMANDS[10]:
                subprocess.run(
                    "docker-compose exec dev python3 manage.py db stamp head", check=True,
                    shell=True, executable="/bin/bash"
                )
    elif insert_input in COMMANDS:
        if insert_input == COMMANDS[5]:
            subprocess.run(
                "docker-compose up --build dev", check=True,
                shell=True, executable="/bin/bash"
            )
        elif insert_input == COMMANDS[4]:
            subprocess.run(
                "docker-compose up dev", check=True,
                shell=True, executable="/bin/bash"
            )
        elif insert_input == COMMANDS[6]:
            subprocess.run(
                "docker-compose up prod", check=True,
                shell=True, executable="/bin/bash"
            )
        elif insert_input == COMMANDS[7]:
            subprocess.run(
                f"docker-compose exec db psql --username={DB_USERNAME} --dbname={DB}", check=True,
                shell=True, executable="/bin/bash"
            )
        elif insert_input == COMMANDS[8]:
            subprocess.run(
                "docker-compose down -v", check=True,
                shell=True, executable="/bin/bash"
            )
        elif insert_input == COMMANDS[9]:
            subprocess.run(
                "docker-compose down", check=True,
                shell=True, executable="/bin/bash"
            )
        elif insert_input == COMMANDS[10]:
            subprocess.run(
                "docker-compose exec dev python manage.py seed_db", check=True,
                shell=True, executable="/bin/bash"
            )

    else:
        print("Command not found. \nProcess end.")


if __name__ == "__main__":
    runApp()