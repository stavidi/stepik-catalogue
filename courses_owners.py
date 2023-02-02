"""courses_owners.py Список владельцев курсов

По всем собранным в json-словарь через API курсам
из файла stepik_courses_utf8.txt
создаётся список владельцев
каждый id отдельной строкой в файле
stepik_owners.txt
"""
import datetime
import json

TODAY = datetime.datetime.today()


def print_list(f):
    owners = {}
    no_lessons = cnt = 0
    for id, info in courses.items():

        if info["owner"] is None:
            no_lessons += 1
            print(info["id"], info["title"])
        else:
            cnt += 1
            owners.setdefault(info["owner"], []).append(
                (info["id"], info["title"]))

    print(*sorted(owners), sep="\n", file=f)

    cntr = __import__("collections").Counter(map(len, owners.values()))
    print(
        json.dumps(dict(
            sorted(cntr.items(), key=lambda x: x[1], reverse=True)), indent=2
        )
    )

    print()
    print(no_lessons, "course" + ("" if no_lessons == 1 else "s"),
          "skipped.")
    print(cnt, "owner" if cnt == 1 else "owners", "set.")
    print(len(owners), "owner" if len(owners) == 1 else "owners",
          "listed.")
    print()


if __name__ == "__main__":
    with open("stepik_courses_utf8.txt", encoding="utf-8") as f:
        courses = json.load(f)

    print(
        (lambda n: f"{n} course" + ("" if n == 1 else "s") + " found.")(
            len(courses)
        )
    )
    print()
    with open("stepik_owners.txt", "w", encoding="utf-8") as f:
        print_list(f)
