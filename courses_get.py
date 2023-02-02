"""courses_get.py Проход по списку курсов из Stepik API

и запись каждой полученной через api json-страницы
отдельным файлом в подкаталог stepik_courses
"""
import datetime
import json
import os
import random
import requests
import sys
import time

TAB = "\n"  # \t
PATH = "stepik_courses"


def get_json(get_api):
    attempts, trying = 3, 0
    while trying < attempts:
        time.sleep(random.randint(3, 8) * 0.1)
        req = f"https://stepik.org/api/{get_api}"
        try:
            req = requests.get(req, timeout=20)
        except (
            ConnectionResetError,
            TimeoutError,
            requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectTimeout,
        ) as err:
            print(
                f"Stepik {repr(get_api)}: {err}",
                file=sys.stderr,
                end=TAB,
                flush=True,
            )
            trying += 1
        else:
            if req.status_code != 200:
                print(
                    f"ош. {req.status_code} {repr(get_api)}",
                    file=sys.stderr,
                    end=TAB,
                    flush=True,
                )
                return {}
            return req.json()
    else:
        return {}


def main():
    if not os.path.exists(PATH):
        os.makedirs(PATH)
        print(f"The new directory {PATH} is created!")

    # Change the current working directory
    os.chdir(f"{PATH}")
    print("Output directory: {}".format(os.getcwd()))

    meta = {"meta": {"page": 0, "has_next": True, "has_previous": False}}
    pk = int(input("Start page (1 by default)# ") or "1") - 1
    while meta["meta"]["has_next"]:
        pk += 1
        if pk % 10 == 1:
            print(pk, file=sys.stderr)
        with open(f"courses_page{pk:05d}.txt", "w", encoding="utf-8") as fp:
            meta = get_json(f"courses/?page={pk}")
            json.dump(meta, fp, indent=2, ensure_ascii=True)  # not False
            # it could be unable to json.load such file without ensure_ascii


if __name__ == "__main__":
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Ctrl+C detected. KeyboardInterrupt done.")

    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
