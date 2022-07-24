from datetime import date
import datetime

CURRENT_YEAR = date.today().year


MONTHS_LIST: list = [
    {"name": "January", "number": 1},
    {"name": "February", "number": 2},
    {"name": "March", "number": 3},
    {"name": "April", "number": 4},
    {"name": "May", "number": 5},
    {"name": "June", "number": 6},
    {"name": "July", "number": 7},
    {"name": "August", "number": 8},
    {"name": "September", "number": 9},
    {"name": "October", "number": 10},
    {"name": "November", "number": 11},
    {"name": "December", "number": 12}
]

YEARS_LIST = [
    {
        "year": 2021,
    }, {
        "year": 2022,
    }, {
        "year": 2023,
    }, {
        "year": 2024,
    }, {
        "year": 2025,
    }, {
        "year": 2026,
    }, {
        "year": 2027,
    }, {
        "year": 2028,
    }, {
        "year": 2030,
    }
]

# To Be Manage


def generate_year_list() -> list:
    from datetime import date
    CURRENT_YEAR = date.today().year

    start = datetime.datetime.strptime("2014", "%Y")
    end = datetime.datetime.strptime(str(CURRENT_YEAR), "%Y")

    date_generated = [
        start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

    new_year_list = []

    for date in date_generated:
        new_year_list.append(date.strftime("%Y"))

    new_year_list.append(str(CURRENT_YEAR))

    final_date_list = list(set(new_year_list))

    for x in final_date_list.sort():
        print(x)

    return final_date_list
