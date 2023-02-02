"""courses_dict.py Прочитать все файлы в каталоге

и создать из них единый словарь
"""
import json
import os
import sys

PATH = "stepik_courses"

# Change the current working directory
start_dir = os.getcwd()
os.chdir(f"{PATH}")
print("Input directory: {}".format(os.getcwd()))

pages = {}
not_found = []
cnt = 0
lencnt = {0: 0}
for filename in os.listdir():
    cnt += 1
    if not cnt % 500:
        print(cnt, file=sys.stderr)
    with open(filename, "r") as f:
        try:
            page = json.load(f)
        except (UnicodeDecodeError, json.decoder.JSONDecodeError):
            print("DecodeError:", filename)
            continue
    if "courses" not in page or not page["courses"]:
        lencnt[0] += 1
        not_found.append(filename)
    else:
        cntlen = len(page["courses"])
        lencnt[cntlen] = lencnt.get(cntlen, 0) + 1
        for course in page["courses"]:
            if course["id"] in pages:
                print(course["id"], "already in pages:", filename)
            else:
                pages[course["id"]] = course
    if "enrollments" in page and page["enrollments"]:
        print(filename)
        print(page["enrollments"])
        print()
print(cnt, "pages done.")

for k, v in sorted(lencnt.items()):
    print(f"{k}: {v}")
if not_found:
    print(
        "courses not found on pages:",
        *map(lambda x: "".join(d for d in x if d.isdecimal()), not_found),
        sep="\t",
    )

with open(os.path.join(start_dir, PATH + "_utf8.txt"), "w",
          encoding="utf-8") as f:
    json.dump(pages, f, indent=2, sort_keys=True, ensure_ascii=False)
with open(os.path.join(start_dir, PATH + "_ascii.txt"), "w") as f:
    json.dump(pages, f)
