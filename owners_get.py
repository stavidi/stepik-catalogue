"""stepik_owners_get.py Получить инфу об овнерах

Проход по списку владельцев курсов на Степике
из файла stepik_owners.txt 
и запись каждой полученной через api json-страницы
отдельным файлом в подкаталог stepik_owners
"""
import datetime
import json
import os
import random
import requests
import sys
import time

PATH = "stepik_owners"


def get_json(get_api):
    attempts, trying = 3, 0
    while trying < attempts:
        time.sleep(random.randint(3, 8) * 0.2)
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
                end="\n",
                flush=True,
            )
            trying += 1
        else:
            if req.status_code != 200:
                print(
                    f"ош. {req.status_code} {repr(get_api)}",
                    file=sys.stderr,
                    end="\n",
                    flush=True,
                )
                return {}
            return req.json()
    else:
        return {}


def main():
    owners = open('stepik_owners.txt').read().splitlines()

    if not os.path.exists(PATH):
        os.makedirs(PATH)
        print(f"The new directory {PATH} is created!")

    # Change the current working directory
    os.chdir(f"{PATH}")
    print("Output directory: {}".format(os.getcwd()))

    meta = {"meta": {"page": 0, "has_next": True, "has_previous": False}}
    start_page = int(input("Start page (1 by default) # ") or "1")
    page = 0
    for owner in owners:
        page += 1
        if page < start_page:
            continue
        if page % 10 == 1:
            print(page, file=sys.stderr)
        with open(f"user{int(owner):09d}.txt", "w",
                  encoding="utf-8") as fp:
            meta = get_json(f"users/{owner}")
            json.dump(meta, fp, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Ctrl+C detected. KeyboardInterrupt done.")

    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
