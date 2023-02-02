"""stepik_authors.py Список всех курсов с авторами

или инструкторами (создателями и преподавателями)
списком в две колонки в stepik_authors.html

Проход по словарю курсов stepik_courses_utf8.txt
и вытаскивание из списков authors и instructors
тех создателей и преподавателей, 
что не упомянуты в stepik_owners_utf8.txt

20364 courses found.
14183 owners found.
2345 teachers found in 1685 courses.
"""
import json


def print_list(f):
    instructors = {int(owner) for owner in owners}
    authors = set()
    studies = {}
    for id, info in courses.items():
        cntr = False
        for teachers in ("authors", "instructors"):
            if teachers in info and info[teachers]:
                for teacher in info[teachers]:
                    if teacher not in instructors:
                        authors.add(teacher)
                        cntr = True
        if cntr:
            studies[info["id"]] = (f'<b>{info["title"]}</b>'
                                   if info["is_popular"] else info["title"])

    with open("stepik_authors.html", "w", encoding="utf-8") as prt:
        print(
            '<!doctype html><html><head>',
            '<title>courses with authors or instructors</title>',
            '<meta charset="utf-8">',
            '<style>',
            'ul {font-family: monospace; line-height: 1.75em; columns: 2;}',
            'li {margin-bottom:.225em;font-size:small;list-style-type:none;}',
            'li:nth-of-type(odd) {background-color: aliceblue; } ',
            'a {text-decoration: none; font-size: larger;}',
            'a:hover, a:active {text-decoration: underline;}',
            'ul + p {margin: 1em 2em 2em 2em}',
            '</style>',
            '</head><body>',
            '<h2>courses with authors or instructors</h2>',
            '<ul>',
            *[f'<li>{id} &nbsp; <a href="https://stepik.org/{id}">{title}'
              '</a></li>' for id, title in studies.items()],
            '',
            f'</ul><p>{len(studies)} courses listed.</p>',
            '</body></html>',
            file=prt, sep='\n',
        )

    print(*sorted(authors), sep='\n', file=f)
    print(len(authors), 'teachers found in', len(studies), 'courses.')


if __name__ == "__main__":
    with open("stepik_courses_utf8.txt", encoding="utf-8") as ff:
        courses = json.load(ff)
    print((lambda n: f'{n} course' + (
        "" if n == 1 else "s") + " found.")(len(courses)))

    with open("stepik_owners_utf8.txt", encoding="utf-8") as ff:
        owners = json.load(ff)
    print((lambda n: f'{n} owner' + (
        "" if n == 1 else "s") + " found.")(len(owners)))

    with open("stepik_authors.txt", "w", encoding="utf-8") as ff:
        print_list(ff)
