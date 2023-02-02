"""Проверка списка курсов на ош.403 404"""
import datetime
import random
import requests
import sys
import time

TAB = "\n"  # \t


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


def filename_ext(filename, ext=".txt"):
    dot = filename.rfind(".")
    if dot > 0:  # empty filename not allowed
        filename = filename[:dot]
    return filename + ext


def main(start_from):
    with open(filename_ext(__file__), encoding="utf-8") as plain, open(
        filename_ext(__file__, "_notfound.txt"), "a", encoding="utf-8"
    ) as ntfnd:
        plain.readline()
        cnt = 0
        for course in plain.read().strip().splitlines():
            if not course.strip():
                continue
            cnt += 1
            if " " in course:
                id, title = course.split(None, 1)
            else:
                id, title = course, ""
            if not id.isdecimal():
                print(repr(id), "not id format", file=sys.stderr)
            if id.isdecimal() and int(id) < start_from:
                continue
            if not cnt % 10:
                print(cnt, course, file=sys.stderr)
            ret = get_json(f"courses/{id}")
            if "courses" not in ret:
                print(id, title, flush=True, file=ntfnd)
            elif title and ret["courses"][0]["title"] != title:
                print(id, title, file=ntfnd)
                print(
                    "-" * (len(id) - 1) + ">",
                    ret["courses"][0]["title"],
                    flush=True,
                    file=ntfnd,
                )


if __name__ == "__main__":
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    try:
        main(int(input("Start from course # ") or "0"))
    except KeyboardInterrupt:
        sys.exit("Ctrl+C detected. KeyboardInterrupt done.")

    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
