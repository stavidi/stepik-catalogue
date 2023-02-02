"""html_lists.py Все курсы по их владельцу

По собранным в словари через API курсам и владельцам
выводятся короткие и полные списки.

courses: 20364 loaded.
owners: 14183 loaded.
"""
import datetime
import json

PATH = "stepik_courses"
LIST = ("stepik_courses_utf8.txt", "stepik_owners_utf8.txt")
MAX = 2  # 10
TODAY = datetime.datetime.today()


def print_list(f, summary, title):
    print(
        "<!doctype html><html><head>",
        f"<title>{summary} Stepik courses list</title>",

        '<meta charset="utf-8"><style>',
        "body{font-family:sans-serif;line-height:150%;}",
        "a{text-decoration:none;}li{clear:both;}",
        "a:hover,a:active{text-decoration:underline;}",
        ".ulol>li:nth-of-type(odd){background-color:#eee;}",
        "li>code:first-of-type{display:inline-block;min-width:5em;",
        "font-family:monospace;text-align:right;padding-right:1em;}",
        "li>i{display:inline-block;float:right;}",
        "samp{font-family:monospace; font-size:133%;}",
        ".summary{display:inline-block;margin: .25em 1em 1em 5em;"
        + "overflow-wrap: break-word;inline-size:84%;}",
        "sub{color:#cd0000;}sup{color:#0000cd;}",
        "sup[title]{cursor:help;font-style:normal;}",
        "dd span { white-space: pre; } ",
        ".red { color: red; } .grey { color: grey; } ",
        "em a { font-family: monospace; letter-spacing: .125em; } ",
        ".small { font-size: small; } .small b { color: #cd0000; } ",
        "em b a { font-variant: small-caps; font-size: 125%;",
        " letter-spacing: .175em; } ",
        "small.red, small.grey, small.none {",
        " display: inline-block; min-width: 3em; } ",
        "</style></head><body>",

        f"<h2>{title}</h2>",
        "<table><tbody><tr><td colspan=2>",
        "<dl style='line-height:175%;'><dt style='background-color:#eee;'>"
        + "&nbsp; как понимать: &nbsp; <i>789&nbsp;  <sub>142</sub> "
        + "<sup>  203   +310 </sup> "
        + ' &nbsp;<sup title="  обычный: 150  с отличием: 185  баллов ">'
        + "&nbsp;💌&nbsp;</sup><b>44&nbsp;</b>&nbsp;</i></dt></td>"
        + "<td rowspan=2>",

        "<p>Всего найдено курсов: ",
        len(courses),
        "</p>",

        '<Ul><li><a href="#platn">платные курсы&nbsp;⬇</a></li>',
        '<LI><a href="#paid">paid courses&nbsp;⬇</a></LI>',
        '<Li><a href="#bespl"><b>бесплатные курсы&nbsp;⬇</b></a></Li>',
        '<lI><a href="#free">free courses&nbsp;⬇</a></lI>',
        '<li><a href="#other">на&nbsp;других языках&nbsp;⬇</a></li></Ul>',

        "</td></tr><tr><td>",
        "<dd><i>789</i> <span>\t учащихся на курсе</span></dd>",
        "<dd><i><sub>142</sub></i> <span>\t урока на курсе</span></dd>",
        "<dd><i><sup>  201 +310 </sup></i> <span>\t количество тестов"
        + " (квизов)</span></dd>",
        "<dd style='line-height:.75em;'> <span>\t <sup><b>+</b>"
        + "  задачи на программирование,"
        "<br> &nbsp;  &nbsp; &nbsp; SQL, данные, Linux</sup></span></dd>",
        "<dd>💌 &nbsp; &nbsp; выдаётся сертификат </dd>"
        + "<dd style='line-height:.75em;'><span>\t"
        + " <sup>(во всплывающей подсказке — <br>"
        + "количество баллов для обычного и с отличием)</sup> </span></dd>",
        "<dd><i><b>44&nbsp;</b></i>", 
        "<span> &nbsp; &nbsp; выдано сертификатов</span></dd></dl>",
        "</td><td>",
        (
            "<dl><dt class=small><b>374 ~~ 20 | 111</b></dt>"
            + "<dd class=small><b>374</b> выдано сертификатов <b>~~</b> </dd>"
            + "<dd class=small><b>20</b> создано курсов <b>|</b> </dd>"
            + "<dd class=small><b>111</b> создано уроков</dd></dl>"
        )
        if summary == 3
        else "",
        "<dl><dt>начало ‒ окончание курса:<br><em>" +
        "<nobr>год-месяц-день ‒</nobr> <nobr>2022-12-31</nobr></em></dt>",
        '<dt style="padding-bottom:.5em;">&nbsp; &nbsp; '
        + '<span style="color:#cd0000;">50%</span> готовность курса</dt>',
        "<dt>сортировка по</dt>",
        "<dd>сертификатам, датам и&nbsp;<b>%</b>&nbsp;готовности,</dd>",
        "<dd>количеству учащихся, уроков и&nbsp;тестов,</dd>",
        "<dd>названию курса.</dd>",
        "</dl></td></tr></tbody></table>",
        file=f,
        sep="\n",
    )

    author = no_lessons = 0
    for h3, func, ulol, aname in (
        (
            "платные курсы",
            lambda x: x[1]["is_paid"] and x[1]["language"] == "ru",
            "ul",  # "ol",
            "platn",
        ),
        (
            "paid courses",
            lambda x: x[1]["is_paid"] and x[1]["language"] == "en",
            "ul",  # "ol",
            "paid",
        ),
        (
            "бесплатные курсы",
            lambda x: not x[1]["is_paid"] and x[1]["language"] == "ru",
            "ul",
            "bespl",
        ),
        (
            "free courses",
            lambda x: not x[1]["is_paid"] and x[1]["language"] == "en",
            "ul",
            "free",
        ),
        (
            "на других языках",
            lambda x: x[1]["language"] not in ("ru", "en"),
            "ul",
            "other",
        ),
    ):
        print(f'<a name="{aname}"></a><h3>{h3}</h3><{ulol} class="ulol">',
              file=f)
        cnt = 0
        for id, info in sorted(
            filter(
                func,
                sorted(courses.items(),
                       key=lambda x: (x[1]["title"].strip())),
            ),
            reverse=True,
            # key=lambda x: (x[1]["learners_count"], x[1]["title"])):
            key=lambda x: (
                (
                    lambda owner: (
                        owner["is_organization"],
                        owner["issued_certificates_count"],
                        owner["created_courses_count"],
                        owner["created_lessons_count"],
                        [ord("ё") - ord(c) for c in owner["full_name"]],
                    )
                )(owners[str(x[1]["owner"])])
                if summary == 3 and owners.get(str(x[1]["owner"]), "")
                else tuple(),
                x[1]["with_certificate"],
                x[1]["certificates_count"],
                (
                    lambda d, e: d is not None
                    and TODAY <= datetime.datetime.strptime(
                        d[:10], "%Y-%m-%d")
                    or e is not None
                )(x[1]["begin_date"], x[1]["end_date"]),
                x[1]["readiness"],
                x[1]["learners_count"],
                x[1]["lessons_count"],
                x[1]["quizzes_count"],
                x[1]["challenges_count"],
            ),
        ):
            if (
                not summary
                and not info["is_unsuitable"]
                or summary
                and info["is_unsuitable"]
                or (
                    info["lessons_count"] < MAX
                    or info["learners_count"] < MAX
                    or info["is_popular"]
                )
                and summary == 1
                or (info["lessons_count"] < 1 or info["learners_count"] < 1)
                and summary == 2
            ):
                no_lessons += 1
            else:
                cnt += 1
                owner = owners.get(str(info["owner"]), {})
                xxx = int(owner.get("issued_certificates_count", "0"))
                xyz = int(owner.get("created_courses_count", "0"))
                xyx = int(owner.get("created_lessons_count", "0"))
                iso = bool(owner.get("is_organization", "0"))

                if summary == 3 and author != info["owner"]:
                    full_name = owners.get(str(info["owner"]), {}).get(
                        "full_name", f'uid={info["id"]}'
                    )
                    cert_count = ""
                    if xxx:
                        cert_count = " 💌 <sub><sup>" + str(xxx) + "</sup></sub>"
                    ccc = owners.get(str(author), {}).get(
                        "created_courses_count", 0)
                    zyx = (
                        author
                        and ccc == 2
                        and xyz == 1
                        and not xxx
                    )
                    if zyx:
                        full_name = "и другие..."
                    if not author or xyz > 1 or zyx:
                        short_bio = owners.get(
                            str(info['owner']), {}).get('short_bio', '')
                        print(
                            "\n<li><div align=center><big>"
                            + "<a href='https://stepik.org/users/"
                            + f"{info.get('owner', 0)}'>"
                            + f"{full_name}</a> {cert_count}</big></div>"
                            + (
                                f"<small class=summary>{short_bio}</small>"
                                if owners.get(str(info["owner"]), {})
                                .get("short_bio", "")
                                .strip()
                                and full_name
                                and xyz > 1
                                else ""
                            )
                            + "</li>",
                            file=f,
                        )
                    author = info["owner"]

                emoji = "💌" if info["with_certificate"] else ""
                begin_end_date = ""
                if info["end_date"] is not None:
                    begin_end_date = (
                        (
                            info["begin_date"][:10]
                            if info["begin_date"] is not None
                            else ""
                        )
                        + "&nbsp;‒&nbsp;"
                        + info["end_date"][:10]
                    )
                elif info["begin_date"] is not None:
                    if TODAY <= datetime.datetime.strptime(
                        info["begin_date"][:10], "%Y-%m-%d"
                    ):
                        begin_end_date = info["begin_date"][:10] + "&nbsp;‒"
                owner_full_name = owners.get(str(info["owner"]), {}).get(
                    "full_name", "uid=" + str(info["owner"])
                )
                print(
                    f"\n<li> ",
                    f'<i>{info["learners_count"]}&nbsp; ',
                    f'<sub>{info["lessons_count"]}</sub> <sup>',
                    f' {info["quizzes_count"]} '
                    if info["quizzes_count"] else "",
                    f' {info["challenges_count"]:+d}'
                    if info["challenges_count"]
                    else "",
                    "</sup>",
                    (
                        ' &nbsp;<sup title=" '
                        + (
                            " обычный: " +
                            f'{info["certificate_regular_threshold"]} '
                            if info["certificate_regular_threshold"]
                            else " "
                        )
                        + (
                            " с отличием: "
                            + f'{info["certificate_distinction_threshold"]} '
                            if info["certificate_distinction_threshold"]
                            else " "
                        )
                        + ' баллов ">&nbsp;'
                        + (emoji)
                        + "&nbsp;</sup>"
                        if emoji
                        else " "
                    )
                    + (
                        f'<b>{info["certificates_count"]}&nbsp;</b>'
                        if info["certificates_count"]
                        else ""
                    )
                    + "&nbsp;</i>",
                    "&nbsp;"
                    + f"<code>{id}</code>"
                    + "<sub>&nbsp;</sub>&nbsp;<sup>&nbsp;</sup>"
                    + (
                        f"<em>"
                        + ("<b>" if iso else "")
                        + "<a href='https://stepik.org/users/"
                        + f"{info['owner']}'>"
                        + f"{owner_full_name}</a>"
                        + (
                            " &nbsp; <sup> <sub>"
                            + (f"{xxx} ~~ " if xxx else "")
                            + f"{xyz} | {xyx}</sub> </sup> "
                            if summary == 3
                            else ""
                        )
                        +
                        # and (xyz > 1 or xyx > 99) #
                        ("</b>" if iso else "") + "</em><br>"
                        if summary >= 2
                        else ""
                    )
                    + (
                        ' <small class="red">&nbsp;'
                        + f'{int(info["readiness"]*100)}%</small> '
                        if info["readiness"] < 0.9
                        else ' <small class="grey">&nbsp;'
                        + f'{int(info["readiness"]*100)}%</small> '
                        if info["readiness"] < 1
                        else ' <small class="none">&nbsp;</small> '
                    )
                    + " "
                    + f'<samp><a href="https://stepik.org/{id}">'
                    + (
                        f'<b><em>{info["title"]}</em></b>'
                        if info["is_popular"] and info["is_adaptive"]
                        else f'<em>{info["title"]}</em>'
                        if info["is_adaptive"]
                        else f'<b>{info["title"]}</b>'
                        if info["is_popular"]
                        else f'{info["title"]}'
                    )
                    + "</a></samp>",
                    (
                        "<sub>&nbsp;"
                        + (
                            f'${info["price"]}'
                            if info["currency_code"] == "USD"
                            else (
                                f'{int(float(info["price"]))}'
                                if float(info["price"]).is_integer()
                                else f'{info["price"]}'
                            )  # 'RUB'
                            + "&#8239;₽"
                        )
                        + "&nbsp;</sub>"
                        if info["is_paid"]
                        else "<sub>&nbsp;</sub>"
                    )
                    + (
                        "<code style='white-space:nowrap;'>&nbsp;"
                        + begin_end_date
                        + "</code>"
                        if begin_end_date
                        else ""
                    )
                    + "",
                    f'<br><small class=summary>{info["summary"]}</small>'
                    if summary == 3
                    else "",
                    "</li>",
                    file=f,
                )
        print(
            f"</{ulol}><blockquote>{cnt} courses printed.</blockquote>"
            f"<p>&nbsp;</p>",
            file=f,
        )

    def plural(once, twice, multiple=None, n=no_lessons):
        if multiple is None:
            multiple = twice
        return (
            once
            if n % 10 == 1 and n % 100 != 11
            else twice
            if 2 <= n % 10 <= 4 and n % 100 not in (12, 13, 14)
            else multiple
        )

    print(
        f"<p>Не показан{plural('', 'о', 'ы')} {no_lessons}"
        + f" {plural('курс', 'курса', 'курсов')}</p>",
        "<p>&nbsp;</p></body></html>",
        file=f,
    )


if __name__ == "__main__":
    with open(LIST[0], encoding="utf-8") as f:
        courses = json.load(f)
    print("courses:", len(courses), "loaded.")

    with open(LIST[1], encoding="utf-8") as f:
        owners = json.load(f)
    print("owners:", len(owners), "loaded.")

    for filename, summa, ttl in (
        (
            PATH + "_unsuitable.html",
            0,
            'кратко о неприемлемых курсах '
            '<small><code>["is_unsuitable"]</code></small>',
        ),
        (
            PATH + "_short.html",
            1,
            f"коротко о непопулярных курсах,"
            " но с уроками и учащимися >= {MAX}",
        ),
        (
            PATH + ".html",
            2,
            "курсы с владельцем, кроме совсем пустых и без курсантов",
        ),
        (
            PATH + "_long.html",
            3,
            "ВСЕ в группах по владельцу и с кратким описанием",
        ),
    ):
        with open(filename, "w", encoding="utf-8") as ff:
            print_list(ff, summa, ttl)
