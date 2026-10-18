import re
#!/usr/bin/env python3
"""Builds the static site ispacex.github.io/gap in English and Russian.

Usage:  python3 src/build.py [--refresh] [OUTDIR]   (default OUTDIR: the repository root, the parent of src/)
        --refresh  first update the upstream state of the pull requests in history.json from `gh`

One source of facts for both languages:
  numbers.json   numbers, commits, PR numbers (language-neutral);
  history.json   one entry per event (times in UTC), and the upstream state of each PR;
  facts.py       the tables (findings, open items, refuted items, standard presentations),
                 each text cell given in English and in Russian;
  pages/<lang>/  the prose of each page, with {{placeholders}} filled from the two above;
  partials/      style and theme script, shared.
English pages go to OUTDIR, Russian ones to OUTDIR/ru.
"""
import datetime, html, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
REFRESH = "--refresh" in sys.argv[1:]
OUT = os.path.abspath(ARGS[0]) if ARGS else os.path.dirname(HERE)
sys.dont_write_bytecode = True
sys.path.insert(0, HERE)
import facts  # noqa: E402

N = json.load(open(os.path.join(HERE, "numbers.json"), encoding="utf-8"))
HISTORY_FILE = os.path.join(HERE, "history.json")
H = json.load(open(HISTORY_FILE, encoding="utf-8"))


def partial(name):
    return open(os.path.join(HERE, "partials", name), encoding="utf-8").read()


STYLE, THEME_HEAD, THEME_JS = partial("style.html"), partial("theme_head.html"), partial("theme.js.html")

BASE = "https://ispacex.github.io/gap/"
REPO = "https://github.com/gap-packages/anupq"
FORK = "https://github.com/ispacex/anupq"
PAGES = ["index.html", "findings.html", "checks.html", "open.html", "history.html", "data.html"]
LANGS = ["en", "ru"]
MONTHS_RU = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября",
             "октября", "ноября", "декабря"]

UI = {
    "en": {
        "site": "ANUPQ: a correctness audit",
        "titles": {"index.html": "Summary", "findings.html": "Findings and fixes",
                   "checks.html": "Differential checks", "open.html": "Open items",
                   "history.html": "History", "data.html": "Data and scripts"},
        "desc": {"index.html": "What we checked in ANUPQ, what we found, and the fixes we propose.",
                 "findings.html": "Each defect: reproducer, cause, fix, why it is right, evidence.",
                 "checks.html": "Descendants against SmallGroups, other presentations, standard presentations.",
                 "open.html": "What is still open, and what was checked and refuted.",
                 "history.html": "When each finding was added, and the state of its pull request.",
                 "data.html": "Scripts and data to repeat the checks."},
        "sections": "Sections", "onpage": "On this page", "language": "Language", "theme": "Theme",
        "themes": {"system": "system", "light": "light", "dark": "dark"},
        "branch": "branch", "prepared": "fix prepared, pull request to come",
        "footer": 'An audit of the GAP package ANUPQ (<a href="{repo}">gap-packages/anupq</a>, master at '
                  '{master}) by the D₅ project (<a href="https://github.com/ispacex/dimension-subrings">'
                  'ispacex/dimension-subrings</a>), which relies on ANUPQ for p-group generation. Fixes: '
                  'pull requests #96–#117; all of them together: branch <a href="{fork}/tree/correctness">'
                  '<code>correctness</code></a> at {correctness}. As of {date}.<br>'
                  'Part of <a href="https://ispacex.github.io/math/">Mathematics</a> at ispacex.github.io.',
    },
    "ru": {
        "site": "ANUPQ: проверка корректности",
        "titles": {"index.html": "Сводка", "findings.html": "Дефекты и исправления",
                   "checks.html": "Сверки", "open.html": "Открытые вопросы",
                   "history.html": "История", "data.html": "Данные и скрипты"},
        "desc": {"index.html": "Что мы проверили в ANUPQ, что нашли и какие исправления предлагаем.",
                 "findings.html": "Каждый дефект: воспроизведение, причина, исправление, обоснование, проверка.",
                 "checks.html": "Потомки против библиотеки SmallGroups, другие презентации, стандартные презентации.",
                 "open.html": "Что ещё открыто, а что проверено и опровергнуто.",
                 "history.html": "Когда добавлен каждый дефект и в каком состоянии его PR.",
                 "data.html": "Скрипты и данные, чтобы повторить проверки."},
        "sections": "Разделы", "onpage": "На этой странице", "language": "Язык", "theme": "Тема",
        "themes": {"system": "системная", "light": "светлая", "dark": "тёмная"},
        "branch": "ветка", "prepared": "исправление готово, PR готовится",
        "footer": 'Проверка пакета GAP ANUPQ (<a href="{repo}">gap-packages/anupq</a>, master '
                  '{master}), выполненная проектом D₅ (<a href="https://github.com/ispacex/dimension-subrings">'
                  'ispacex/dimension-subrings</a>), который опирается на ANUPQ при построении p-групп. '
                  'Исправления: PR #96–#117; все вместе — ветка <a href="{fork}/tree/correctness">'
                  '<code>correctness</code></a>, коммит {correctness}. Состояние на {date}.<br>'
                  'Раздел <a href="https://ispacex.github.io/ru/math/">«Математика»</a> на ispacex.github.io.',
    },
}

THEME_ICONS = {
    "system": '<circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 0 1 0 18z" fill="currentColor"/>',
    "light": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "dark": '<path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/>',
}


def date(lang):
    d = datetime.date.fromisoformat(N["date"])
    if lang == "ru":
        return f"{d.day} {MONTHS_RU[d.month - 1]} {d.year} г."
    return f"{d.day} {d.strftime('%B')} {d.year}"


def num(lang, x):
    """A decimal number as written in the language."""
    s = str(x)
    return s.replace(".", ",") if lang == "ru" else s


def pr(key, lang):
    n = N.get("pr_" + key)
    if n:
        return f'<a href="{REPO}/pull/{n}">#{n}</a>'
    if N.get("prepared_" + key):
        return UI[lang]["prepared"]
    b = N["branch_" + key]
    return f'{UI[lang]["branch"]} <a href="{FORK}/tree/{b}"><code>{b}</code></a>'


# ---------------------------------------------------------------------------------------------
# History

NUMBER = {}  # finding anchor -> its number on findings.html
for r in facts.FINDINGS:
    if "anchor" in r:
        NUMBER[r["anchor"]] = len(NUMBER) + 1

HT = {
    "en": {"added": "added", "time": "time (UTC)", "event": "event", "no": "no.", "finding": "finding",
           "fix": "fix", "pr_opened": "PR opened", "state": "upstream",
           "states": {"open": "open", "merged": "merged", "closed": "closed"},
           "verdict": {"confirmed": "Open item {item} confirmed ({issue}) → finding {k}",
                       "refuted": "Open item {item} refuted ({issue})"},
           "found": "Found while checking {via}: {issue}",
           "extra": "{issue} confirmed → finding {k}", "extra_open": "{issue} {note}",
           "prs": "Pull requests {prs} opened for findings 1–9",
           "pr": "Pull request {pr} opened for finding {k}",
           "prepared": "fix prepared", "see": "see"},
    "ru": {"added": "добавлен", "time": "время (UTC)", "event": "событие", "no": "№", "finding": "дефект",
           "fix": "исправление", "pr_opened": "PR открыт", "state": "в апстриме",
           "states": {"open": "открыт", "merged": "влит", "closed": "закрыт"},
           "verdict": {"confirmed": "Открытый вопрос {item} подтверждён ({issue}) → дефект {k}",
                       "refuted": "Открытый вопрос {item} опровергнут ({issue})"},
           "found": "Найдено при проверке {via}: {issue}",
           "extra": "{issue} подтверждён → дефект {k}", "extra_open": "{issue}: {note}",
           "prs": "Открыты PR {prs} для дефектов 1–9",
           "pr": "Открыт PR {pr} для дефекта {k}",
           "prepared": "исправление готово", "see": "см."},
}


def dmy(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day:02d}.{d.month:02d}.{d.year}"


def event_id(e):
    if e.get("id"):
        return "e-" + e["id"]
    k = e["kind"]
    if k == "pr":
        return f"e-pr-{e['pr']}"
    if k in ("verdict", "found", "extra"):
        return f"e-{k}-{e['issue']}"
    return f"e-{e['date']}-{e['time'].replace(':', '')}"


def added():
    """finding anchor -> (event id, date) of the event that put it on findings.html"""
    a = {}
    for e in H["events"]:
        for f in e.get("findings", []):
            a[f] = (event_id(e), e["date"])
        if e["kind"] in ("verdict", "extra") and e.get("finding"):
            a[e["finding"]] = (event_id(e), e["date"])
    missing = set(NUMBER) - set(a)
    if missing:
        raise SystemExit("findings without a history entry: " + ", ".join(sorted(missing)))
    return a


def flink(anchor, lang):
    word = {"en": "finding", "ru": "дефект"}[lang]
    return f'<a href="findings.html#{anchor}">{NUMBER[anchor]}</a>' if anchor else word


def prlink(n):
    return f'<a href="{REPO}/pull/{n}">#{n}</a>'


def event_text(e, lang):
    T = HT[lang]
    k = e["kind"]
    if k == "text":
        return e["text"][lang]
    if k == "verdict":
        s = T["verdict"][e["verdict"]].format(item=e["item"], issue=e["issue"],
                                              k=flink(e["finding"], lang) if e.get("finding") else "")
        if e["verdict"] == "refuted":
            s += f' — {T["see"]} <a href="open.html#refuted">{UI[lang]["titles"]["open.html"]}</a>'
        return s
    if k == "found":
        return T["found"].format(via=e["via"], issue=e["issue"])
    if k == "extra":
        if e.get("finding"):
            return T["extra"].format(issue=e["issue"], k=flink(e["finding"], lang))
        return T["extra_open"].format(issue=e["issue"], note=e["note"][lang])
    if k == "prs":
        return T["prs"].format(prs=", ".join(prlink(n) for n in e["prs"]))
    if k == "pr":
        return T["pr"].format(pr=prlink(e["pr"]), k=flink(e["finding"], lang))
    raise SystemExit("unknown event kind " + k)


def history_events(lang):
    T = HT[lang]
    ev = sorted(H["events"], key=lambda e: (e["date"], e["time"] or "99:99"), reverse=True)
    rows, day = [], None
    for e in ev:
        if e["date"] != day:
            day = e["date"]
            rows.append(f'<tr><th class=l colspan=2 id="d-{day}">{dmy(day)}</th></tr>')
        rows.append(f'<tr id="{event_id(e)}"><td>{e["time"] or "—"}</td><td class=l>{event_text(e, lang)}</td></tr>')
    head = f'<tr><th>{T["time"]}</th><th class=l>{T["event"]}</th></tr>'
    return '<div class="tw"><table>\n' + head + "\n" + "\n".join(rows) + "\n</table></div>"


def history_findings(lang):
    T, a = HT[lang], added()
    rows = []
    for r in facts.FINDINGS:
        if "anchor" not in r:
            continue
        eid, d = a[r["anchor"]]
        n = N.get("pr_" + r["fix"])
        if n:
            st = H["pr_states"].get(str(n), "open")
            fix, opened, state = prlink(n), dmy(H["pr_created"][str(n)]), T["states"].get(st, st)
            cls = {"merged": "ok", "closed": "bad"}.get(st, "")
        else:
            fix, opened, state, cls = T["prepared"], "—", "—", "amb"
        rows.append(f'<tr><td>{NUMBER[r["anchor"]]}</td><td class=l><a href="findings.html#{r["anchor"]}">'
                    f'{r["defect"][lang]}</a></td><td><a href="#{eid}">{dmy(d)}</a></td><td>{fix}</td>'
                    f'<td>{opened}</td><td class="{cls}">{state}</td></tr>')
    head = "<tr>" + "".join(f"<th{' class=l' if i == 1 else ''}>{T[k]}</th>" for i, k in
                            enumerate(["no", "finding", "added", "fix", "pr_opened", "state"])) + "</tr>"
    return '<div class="tw"><table>\n' + head + "\n" + "\n".join(rows) + "\n</table></div>"


DT = {
    "en": {"file": "file", "what": "what", "supports": "supports", "fix": "fix", "test": "test in the PR",
           "data": "data", "finding": "finding", "page": {"checks.html": "check", "open.html": "open item",
                                                         "open.html#refuted": "refuted item"}},
    "ru": {"file": "файл", "what": "что это", "supports": "к чему", "fix": "исправление", "test": "тест в PR",
           "data": "данные", "finding": "дефект", "page": {"checks.html": "сверка", "open.html": "открытый вопрос",
                                                          "open.html#refuted": "опровергнутое"}},
}
FIX_OF = {r["anchor"]: r["fix"] for r in facts.FINDINGS if "anchor" in r}


def test_link(fix):
    n, name = N.get("pr_" + fix), facts.TESTS.get(fix)
    return f'<a href="{REPO}/pull/{n}/files"><code>tst/{name}</code></a>' if n and name else ""


def data_table(lang, depth):
    T, a = DT[lang], added()
    files_dir = "../" * depth + "data/"
    rows = []
    for d in facts.DATA:
        files = "<br>".join(f'<a href="{files_dir}{f}"><code>{f}</code></a>' for f in d["files"])
        sup = [f'{T["finding"]} <a href="findings.html#{x}">{NUMBER[x]}</a> '
               f'(<a href="history.html#{a[x][0]}">{dmy(a[x][1])}</a>)' for x in d["findings"]]
        if d.get("page"):
            key = d["page"] if d["page"].startswith("open") else d["page"].split("#")[0]
            sup.append(f'<a href="{d["page"]}">{T["page"][key]}</a>')
        fixes = sorted({FIX_OF[x] for x in d["findings"]})
        rows.append(f'<tr id="d-{d["id"]}"><td class=l>{files}</td><td class=l>{d["what"][lang]}</td>'
                    f'<td class=l>{"; ".join(sup)}</td><td>{" ".join(pr(f, lang) for f in fixes)}</td>'
                    f'<td>{" ".join(test_link(f) for f in fixes)}</td></tr>')
    head = "<tr>" + "".join(f"<th class=l>{T[k]}</th>" for k in ("file", "what", "supports")) + \
           f'<th>{T["fix"]}</th><th>{T["test"]}</th></tr>'
    return '<div class="tw"><table>\n' + head + "\n" + "\n".join(rows) + "\n</table></div>"


def write_data_readme():
    import re
    plain = lambda h: re.sub(r"<[^>]+>", "", h).replace("$", "").replace("\\", "")
    lines = ["Files of https://ispacex.github.io/gap/data.html (generated by src/build.py from src/facts.py).", ""]
    for d in facts.DATA:
        sup = ", ".join(f"finding {NUMBER[x]}" for x in d["findings"]) or d.get("page", "")
        for f in d["files"]:
            if not os.path.exists(os.path.join(OUT, "data", f)):
                raise SystemExit("data file missing: data/" + f)
            lines.append(f"{f}: {plain(d['what']['en'])} [{sup}]")
    with open(os.path.join(OUT, "data", "README.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def mark_findings(body, lang):
    """A small 'added dd.mm.yyyy' line under each finding's heading, linking to its history entry."""
    a = added()
    for anchor, (eid, d) in a.items():
        tag = f'<h3 id="{anchor}">'
        i = body.find(tag)
        if i < 0:
            raise SystemExit(f"finding {anchor} not on findings.html ({lang})")
        j = body.index("</h3>", i) + len("</h3>")
        bits = [f'<a href="history.html#{eid}">{HT[lang]["added"]} {dmy(d)}</a>']
        data = [x for x in facts.DATA if anchor in x["findings"]]
        if data:
            bits.append(DT[lang]["data"] + ": " + ", ".join(
                f'<a href="data.html#d-{x["id"]}"><code>{x["files"][0]}</code></a>' for x in data))
        t = test_link(FIX_OF[anchor])
        if t:
            bits.append(DT[lang]["test"] + ": " + t)
        body = body[:j] + '\n<p class="added">' + " · ".join(bits) + "</p>" + body[j:]
    return body


def refresh_pr_states():
    import subprocess
    out = subprocess.run(["gh", "pr", "list", "--repo", "gap-packages/anupq", "--state", "all", "--limit", "200",
                          "--json", "number,createdAt,state"], check=True, capture_output=True, text=True).stdout
    for p in json.loads(out):
        k = str(p["number"])
        if k in H["pr_states"]:
            H["pr_states"][k] = p["state"].lower()
            H["pr_created"][k] = p["createdAt"][:10]
    H["pr_states_as_of"] = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    with open(HISTORY_FILE, "w", encoding="utf-8") as fh:
        json.dump(H, fh, indent=1, ensure_ascii=False)
        fh.write("\n")


# ---------------------------------------------------------------------------------------------
# Shared tables

def findings_table(lang):
    rows = []
    for r in facts.FINDINGS:
        if "group" in r:
            rows.append(f'<tr><th class=l colspan=4>{r["group"][lang]}</th></tr>')
            continue
        rows.append(
            f'<tr><td class=l><a href="findings.html#{r["anchor"]}">{r["defect"][lang]}</a></td>'
            f'<td class="l {r["cls"]}">{r["effect"][lang]}</td><td class=l>{r["reached"][lang]}</td>'
            f'<td>{pr(r["fix"], lang)}</td></tr>')
    h = {"en": ("Defect", "Effect", "Reached by", "Fix"), "ru": ("Дефект", "Последствие", "Когда проявляется", "Исправление")}[lang]
    head = "<tr>" + "".join(f"<th class=l>{t}</th>" for t in h[:3]) + f"<th>{h[3]}</th></tr>"
    return '<div class="tw"><table>\n' + head + "\n" + "\n".join(rows) + "\n</table></div>"


def open_table(lang):
    h = {"en": ("Item", "Where", "Status"), "ru": ("Вопрос", "Где", "Состояние")}[lang]
    rows = [f'<tr><td class=l>{r["item"][lang]}</td><td class=l>{r["where"]}</td>'
            f'<td class="l {r.get("cls", "")}">{r["status"][lang]}</td></tr>' for r in facts.OPEN]
    head = "<tr>" + "".join(f"<th class=l>{t}</th>" for t in h) + "</tr>"
    return '<div class="tw"><table>\n' + head + "\n" + "\n".join(rows) + "\n</table></div>"


def refuted_list(lang):
    return "<ul>\n" + "\n".join(f'<li><b>{r["item"][lang]}</b> {r["why"][lang]}</li>' for r in facts.REFUTED) + "\n</ul>"


def sp_rows(lang):
    rows = []
    for order, groups, copies, bad in N["sp_table"]:
        rows.append(f"<tr><td>{order}</td><td>{groups}</td><td>{copies}</td>"
                    f'<td class={"ok" if bad == 0 else "bad"}>{bad}</td></tr>')
    for order, groups, copies in N.get("sp_pending", []):
        txt = {"en": "rerun in progress", "ru": "идёт повторный прогон"}[lang]
        rows.append(f"<tr><td>{order}</td><td>{groups}</td><td>{copies}</td><td class=amb>{txt}</td></tr>")
    return "".join(rows)


# ---------------------------------------------------------------------------------------------

def values(lang, depth):
    v = {k: str(x) for k, x in N.items() if not isinstance(x, (list, dict))}
    for k in ("timing_old", "timing_new"):
        v[k] = num(lang, N[k])
    v["date"] = date(lang)
    v["repo"], v["fork"] = REPO, FORK
    v["data"] = "../" * depth + "data/"
    for k in facts.FIX_KEYS:
        v["pr_" + k + "_link"] = pr(k, lang)
    tables = {"findings_table": findings_table(lang), "open_table": open_table(lang),
              "refuted_list": refuted_list(lang), "sp_rows": sp_rows(lang),
              "history_events": history_events(lang), "history_findings": history_findings(lang),
              "data_table": data_table(lang, depth)}
    v["pr_states_as_of"] = dmy(H["pr_states_as_of"])
    for k, s in tables.items():  # table cells may use the plain values
        v[k] = fill(s, v)
    return v


def fill(s, v):
    out, i = [], 0
    while True:
        j = s.find("{{", i)
        if j < 0:
            out.append(s[i:])
            return "".join(out)
        k = s.find("}}", j)
        key = s[j + 2:k]
        if key not in v:
            raise SystemExit(f"unfilled placeholder {{{{{key}}}}} near: {s[j:j + 60]!r}")
        out.append(s[i:j])
        out.append(v[key])
        i = k + 2


def theme_buttons(lang):
    u = UI[lang]
    b = "".join(
        f'<button type="button" data-t="{t}" aria-pressed="{"true" if t == "system" else "false"}" '
        f'aria-label="{u["theme"]}: {u["themes"][t]}" title="{u["theme"]}: {u["themes"][t]}">'
        f'<svg viewBox="0 0 24 24" aria-hidden="true">{THEME_ICONS[t]}</svg></button>' for t in THEME_ICONS)
    return f'<span class="theme" role="group" aria-label="{u["theme"]}">{b}</span>'


def lang_switch(lang, fname):
    if lang == "en":
        return (f'<span class="lang" role="group" aria-label="{UI[lang]["language"]}"><strong lang="en" aria-current="true">EN</strong>'
                f'<a href="ru/{fname}" hreflang="ru" lang="ru">RU</a></span>')
    return (f'<span class="lang" role="group" aria-label="{UI[lang]["language"]}"><a href="../{fname}" hreflang="en" lang="en">EN</a>'
            f'<strong lang="ru" aria-current="true">RU</strong></span>')


def toc(body, label):
    """the page's own headings with an id, as a side panel; None if too few"""
    heads = re.findall(r'<h([23]) id="([^"]+)"[^>]*>(.*?)</h\1>', body, re.S)
    if len(heads) < 4:
        return None
    items = "".join(
        f'<li class="l{lvl}"><a href="#{hid}">{re.sub(r"<[^>]+>", "", text).strip()}</a></li>'
        for lvl, hid, text in heads)
    return f'<aside class="toc" aria-label="{html.escape(label)}"><p>{html.escape(label)}</p><ol>{items}</ol></aside>'


def page(lang, fname):
    u = UI[lang]
    depth = 0 if lang == "en" else 1
    v = values(lang, depth)
    body = fill(open(os.path.join(HERE, "pages", lang, fname), encoding="utf-8").read(), v)
    if fname == "findings.html":
        body = mark_findings(body, lang)
    title = u["site"] if fname == "index.html" else u["titles"][fname] + " — " + u["site"]
    nav = "".join(
        f'<a href="{f}" class=cur aria-current=page>{u["titles"][f]}</a>' if f == fname else f'<a href="{f}">{u["titles"][f]}</a>'
        for f in PAGES)
    alt = (f'<link rel="alternate" hreflang="en" href="{BASE}{fname}">\n'
           f'<link rel="alternate" hreflang="ru" href="{BASE}ru/{fname}">\n'
           f'<link rel="alternate" hreflang="x-default" href="{BASE}{fname}">\n'
           f'<link rel="canonical" href="{BASE}{"" if lang == "en" else "ru/"}{fname}">')
    side = toc(body, u["onpage"])
    main_cls = "wrap has-toc" if side else "wrap"
    side = side or ""
    body_cls = ' class="has-toc"' if main_cls != "wrap" else ""
    footer = u["footer"].format(repo=REPO, fork=FORK, master=N["master"], correctness=N["correctness"], date=v["date"])
    return f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
{THEME_HEAD}
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(u["desc"][fname])}">
{alt}
{STYLE}
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
 onload="renderMathInElement(document.body,{{delimiters:[{{left:'$$',right:'$$',display:true}},{{left:'$',right:'$',display:false}}]}})"></script></head>
<body{body_cls}><header><div class="wrap"><div class="top"><a class="title" href="index.html">{u["site"]}</a>
<div class="tools">{theme_buttons(lang)}{lang_switch(lang, fname)}</div></div>
<nav aria-label="{u["sections"]}">{nav}</nav></div></header>
<main class="{main_cls}">
<div class="content">
{body}
</div>{side}
</main><footer><div class="wrap"><small>{footer}</small></div></footer>
{THEME_JS}
</body></html>
"""


def main():
    if REFRESH:
        refresh_pr_states()
    for lang in LANGS:
        d = OUT if lang == "en" else os.path.join(OUT, lang)
        os.makedirs(d, exist_ok=True)
        for f in PAGES:
            with open(os.path.join(d, f), "w", encoding="utf-8") as fh:
                fh.write(page(lang, f))
    write_data_readme()
    open(os.path.join(OUT, ".nojekyll"), "w").close()


if __name__ == "__main__":
    main()
