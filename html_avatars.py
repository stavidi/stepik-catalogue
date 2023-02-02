"""html_avatars.py аватарки всех владельцев курсов"""
import json
import sys


def main():
    with open("stepik_owners_avatars.html", "w",
              encoding="utf-8") as avatars_html:
        sys_stdout = sys.stdout
        sys.stdout = avatars_html
        print('<!doctype html><html><head>')
        print('<title>avatars owners stepik</title>')
        print('<meta charset="utf-8">')
        print('<style> ')
        print("""
figure {
  display: inline-block;
  border: thin silver solid;
  margin: 0.5em;
  padding: 0.5em;
  width: 160px; height: 250px;
  overflow-wrap: break-word;
  text-align: center;
  background-color: #efe;
  vertical-align: bottom;
} img { width: 100%; }
              """)
        print('</style></head><body>')
        print('<h2>stepik owners avatars</h2>')
        done = 0
        for owner, info in owners.items():
            if info["avatar"].startswith(
                    'https://stepik.org/media/users/'):
                done += 1
                print(end=f'''
<figure><a href="https://stepik.org/users/{owner}"><p
><img src={info["avatar"]} alt="{owner} "
><figcaption>{info['full_name']}</figcaption></p></a></figure>
'''.strip())
        print('<p>&nbsp;</p><p>', done, 'done.<p><p>&nbsp;</p>')
        print('</body></html>')
    sys.stdout = sys_stdout
    print(done, 'done.')


if __name__ == "__main__":
    with open("stepik_owners_utf8.txt", encoding="utf-8") as f:
        owners = json.load(f)
    print("owners:", len(owners), "loaded.")

    main()
