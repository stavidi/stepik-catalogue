"""owners_dict.py Словарь инфы о владельцах курсов

Прочитать все файлы в каталоге stepik_owners
создать из них единый словарь владельцев курсов
и записать его в json-файл stepik_owners_utf8.txt 
"""
import json
import os
import sys

PATH = "stepik_owners"

# Change the current working directory
start_dir = os.getcwd()
os.chdir(f"{PATH}")
print("Input directory: {}".format(os.getcwd()))

pages = {}
not_found = []
cnt = 0
for filename in os.listdir():
    cnt += 1
    if not cnt % 500:
        print(cnt, file=sys.stderr)
    with open(filename, "r", encoding="utf-8") as f:
        try:
            page = json.load(f)
        except (UnicodeDecodeError, json.decoder.JSONDecodeError):
            print("DecodeError:", filename)
            continue
    if "users" not in page or not page["users"]:
        not_found.append(filename)
    else:
        for user in page["users"]:
            if user["id"] in pages:
                print(user["id"], "already in pages:", filename)
            else:
                pages[user["id"]] = user
    if "enrollments" in page and page["enrollments"]:
        print(filename)
        print(page["enrollments"])
        print()
print(cnt, "pages done.")

if not_found:
    print(
        "users not found on pages:",
        *map(lambda x: "".join(d for d in x if d.isdecimal()), not_found),
        sep="\t",
    )

with open(os.path.join(start_dir, PATH + "_utf8.txt"), "w",
          encoding="utf-8") as f:
    json.dump(pages, f, indent=2, sort_keys=True, ensure_ascii=False)
