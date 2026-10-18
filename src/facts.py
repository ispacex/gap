"""Tables shared by the English and the Russian pages.

Each text cell is {"en": ..., "ru": ...}; code, numbers and file names are the same in both.
Cells may use {{placeholders}} from numbers.json. A finding's "fix" names a key k with
"pr_k" (a pull request), "prepared_k" (fix ready, no PR yet) or "branch_k" in numbers.json.
"""


def t(en, ru):
    return {"en": en, "ru": ru}


def group(en, ru):
    return {"group": t(en, ru)}


# Summary table on the index page; the anchors are the sections of findings.html.
FINDINGS = [
    group("First pass: pull requests #96–#104", "Первый проход: PR #96–#104"),
    dict(anchor="aut-basis", fix="aut_basis", cls="bad",
         defect=t("Automorphisms sent in the wrong basis", "Автоморфизмы передаются в чужом базисе"),
         effect=t("wrong descendants; pq crash", "неверные потомки; падение pq"),
         reached=t("<code>PqDescendants(G)</code> for a pc group whose pcgs is not pq's own pcp: {{basis_wrong_old}} of "
                   "{{basis_copies}} isomorphic copies of SmallGroups of order 64–256 gave wrong descendants, "
                   "{{basis_failed_old}} crashed pq",
                   "<code>PqDescendants(G)</code> для pc-группы, чей pcgs не совпадает с pcp, который строит сам pq: "
                   "из {{basis_copies}} изоморфных копий групп SmallGroups порядков 64–256 неверных потомков дали "
                   "{{basis_wrong_old}}, pq упал на {{basis_failed_old}}")),
    dict(anchor="char-counters", fix="char_counters", cls="bad",
         defect=t("Orbit counters in <code>char</code>", "Счётчики орбит в <code>char</code>"),
         effect=t("wrong descendants and stabilisers", "неверные потомки и стабилизаторы"),
         reached=t("127 or more automorphisms, e.g. <code>AbelianGroup([2^3,2^5,2^7,2^9,2^11])</code>: 16384 step-1 "
                   "descendants instead of 26",
                   "127 и более автоморфизмов, например <code>AbelianGroup([2^3,2^5,2^7,2^9,2^11])</code>: 16384 "
                   "потомка с шагом 1 вместо 26")),
    dict(anchor="sp-epimorphism", fix="sp_epimorphism", cls="bad",
         defect=t("<code>EpimorphismStandardPresentation</code>", "<code>EpimorphismStandardPresentation</code>"),
         effect=t("map not bijective", "отображение не биективно"),
         reached=t("pc groups whose generators are not their pcgs, e.g. <code>AbelianGroup(IsPcGroup,[4,2])</code>; "
                   "the SP itself is right",
                   "pc-группы, у которых порождающие не совпадают с pcgs, например "
                   "<code>AbelianGroup(IsPcGroup,[4,2])</code>; сама стандартная презентация верна")),
    dict(anchor="descendants-law", fix="descendants_law", cls="bad",
         defect=t("Exponent law the group breaks", "Закон экспоненты, которому группа не удовлетворяет"),
         effect=t("pq crash", "падение pq"),
         reached=t("<code>PqDescendants(SmallGroup(16,5) : Exponent := 4)</code>",
                   "<code>PqDescendants(SmallGroup(16,5) : Exponent := 4)</code>")),
    dict(anchor="sp-relators", fix="sp_relators", cls="amb",
         defect=t("SP rank with <code>Relators</code>", "Ранг в SP при опции <code>Relators</code>"),
         effect=t("hang", "зависание"),
         reached=t('<code>PqStandardPresentation(F : Prime := 2, Relators := ["a^8", "b*a^-2"])</code>',
                   '<code>PqStandardPresentation(F : Prime := 2, Relators := ["a^8", "b*a^-2"])</code>')),
    dict(anchor="stale-descendants", fix="stale_descendants", cls="bad",
         defect=t("Stale groups in interactive <code>PqDescendants</code>",
                  "Старые группы в интерактивном <code>PqDescendants</code>"),
         effect=t("extra groups returned", "возвращаются лишние группы"),
         reached=t("an interactive process after <code>PqPGConstructDescendants</code>",
                   "интерактивный процесс после <code>PqPGConstructDescendants</code>")),
    dict(anchor="savepqlist", fix="savepqlist", cls="amb",
         defect=t("<code>SavePqList</code>", "<code>SavePqList</code>"),
         effect=t("file unreadable", "файл не читается"),
         reached=t("a group with an automorphism group", "группа с заданной группой автоморфизмов")),
    dict(anchor="relative-orders", fix="relative_orders", cls="amb",
         defect=t("<code>RelativeOrders</code> option", "Опция <code>RelativeOrders</code>"),
         effect=t("wrong data or error", "неверные данные или ошибка"),
         reached=t("<code>PqPGSupplyAutomorphisms(.. : RelativeOrders := [3, 2])</code>",
                   "<code>PqPGSupplyAutomorphisms(.. : RelativeOrders := [3, 2])</code>")),
    dict(anchor="isomorphic-trivial", fix="isomorphic_trivial", cls="amb",
         defect=t("Trivial groups in <code>IsIsomorphicPGroup</code>", "Тривиальные группы в <code>IsIsomorphicPGroup</code>"),
         effect=t("error", "ошибка"),
         reached=t("two trivial groups", "две тривиальные группы")),

    group("Second pass, wrong results without a message (none is reached by 2-group generation with default options)",
          "Второй проход: неверный результат без сообщения (ни один не достигается при построении 2-групп "
          "с параметрами по умолчанию)"),
    dict(anchor="pcgs-automorphisms", fix="pcgs_automorphisms", cls="bad",
         defect=t("Option <code>PcgsAutomorphisms</code> with a sequence that is not PAG",
                  "Опция <code>PcgsAutomorphisms</code> с последовательностью, не являющейся PAG"),
         effect=t("wrong descendants (isomorphic duplicates)", "неверные потомки (изоморфные повторы)"),
         reached=t("<code>PqDescendants(ElementaryAbelianGroup(4) : ClassBound := 3, PcgsAutomorphisms)</code>: "
                   "161 groups instead of 136",
                   "<code>PqDescendants(ElementaryAbelianGroup(4) : ClassBound := 3, PcgsAutomorphisms)</code>: "
                   "161 группа вместо 136")),
    dict(anchor="exponent-reduced-list", fix="exponent_reduced_list", cls="bad",
         defect=t("Exponent law with automorphisms supplied by hand", "Закон экспоненты при автоморфизмах, заданных вручную"),
         effect=t("group too large", "группа слишком велика"),
         reached=t("<code>PqSupplyAutomorphisms</code> with automorphisms that do not induce $GL(d,p)$, then "
                   "<code>PqNextClass</code> under <code>Exponent</code>: $2^{13}$ instead of $2^4$",
                   "<code>PqSupplyAutomorphisms</code> с автоморфизмами, которые не индуцируют $GL(d,p)$, затем "
                   "<code>PqNextClass</code> с <code>Exponent</code>: $2^{13}$ вместо $2^4$")),
    dict(anchor="exponent-queue", fix="exponent_queue", cls="bad",
         defect=t("Exponent-law queue at class 2", "Очередь закона экспоненты в классе 2"),
         effect=t("wrong groups or pq crash (heap overflow)", "неверные группы или падение pq (переполнение кучи)"),
         reached=t("<code>PqSupplyAutomorphisms</code> generating $GL(d,2)$, $d \\ge 7$, with <code>Exponent := 2</code>: "
                   "e.g. $2^{11}$ instead of $2^7$ in 6 of 10 runs",
                   "<code>PqSupplyAutomorphisms</code>, порождающие $GL(d,2)$, $d \\ge 7$, с <code>Exponent := 2</code>: "
                   "например $2^{11}$ вместо $2^7$ в 6 прогонах из 10")),
    dict(anchor="gl-order", fix="gl_order", cls="bad",
         defect=t("<code>glOrder</code> for $p^d &gt; 10000$", "<code>glOrder</code> при $p^d &gt; 10000$"),
         effect=t("wrong stabilisers handed to pq", "в pq передаются неверные стабилизаторы"),
         reached=t("<code>PqDescendants</code> of a group of rank $d$ with $p^d &gt; 10000$, e.g. $(C_{101})^2$: "
                   "<code>glOrder</code> 1020000/1030301 instead of 1030200",
                   "<code>PqDescendants</code> для группы ранга $d$ с $p^d &gt; 10000$, например $(C_{101})^2$: "
                   "<code>glOrder</code> 1020000/1030301 вместо 1030200")),
    dict(anchor="epimorphism-non-pgroup", fix="epimorphism_non_pgroup", cls="bad",
         defect=t("<code>PqEpimorphism</code> for a pc group that is not a $p$-group",
                  "<code>PqEpimorphism</code> для pc-группы, не являющейся $p$-группой"),
         effect=t("map not a homomorphism, or error", "отображение не гомоморфизм, или ошибка"),
         reached=t("generators other than the pcgs, e.g. those of a pc group $S_3 \\times C_4$ in reverse order",
                   "порождающие не совпадают с pcgs, например порождающие pc-группы $S_3 \\times C_4$ в обратном порядке")),
    dict(anchor="interface-bookkeeping", fix="interface_bookkeeping", cls="bad",
         defect=t("<code>StepSize</code> above the nuclear rank; temporary directory; group names",
                  "<code>StepSize</code> больше ядерного ранга; временный каталог; имена групп"),
         effect=t("wrong descendants with <code>PcgsAutomorphisms</code>; otherwise errors",
                  "неверные потомки при <code>PcgsAutomorphisms</code>; в остальных случаях ошибки"),
         reached=t("<code>PqDescendants(SmallGroup(4,2) : StepSize := 4, PcgsAutomorphisms)</code>: 3 groups instead "
                   "of none; <code>ANUPQDirectoryTemporary</code>; a group name with <code>_</code>",
                   "<code>PqDescendants(SmallGroup(4,2) : StepSize := 4, PcgsAutomorphisms)</code>: 3 группы вместо "
                   "пустого списка; <code>ANUPQDirectoryTemporary</code>; имя группы с <code>_</code>")),
    dict(anchor="prime-bound", fix="prime_bound", cls="bad",
         defect=t("Primes $p \\ge 2^{15}$", "Простые $p \\ge 2^{15}$"),
         effect=t("wrong epimorphism or $p$-cover", "неверный эпиморфизм или $p$-накрытие"),
         reached=t("<code>PqEpimorphism(G : Prime := 32771, ClassBound := 1)</code>: a relation of $G$ fails in the image",
                   "<code>PqEpimorphism(G : Prime := 32771, ClassBound := 1)</code>: соотношение группы $G$ в образе "
                   "не выполняется")),
    dict(anchor="pc-generator-limit", fix="pc_generator_limit", cls="bad",
         defect=t("More than 65535 pc generators in one class", "Больше 65535 pc-порождающих в одном классе"),
         effect=t("corrupted presentation", "испорченная презентация"),
         reached=t("<code>PqNextClass</code> for <code>FreeGroup(361)</code>, $p = 2$, from class 1 to class 2",
                   "<code>PqNextClass</code> для <code>FreeGroup(361)</code>, $p = 2$, переход от класса 1 к классу 2")),
    dict(anchor="commutator-workspace", fix="commutator_workspace", cls="bad",
         defect=t("Workspace for a commutator relation with an exponent",
                  "Рабочая память для коммутаторного соотношения с показателем"),
         effect=t("wrong order", "неверный порядок"),
         reached=t('<code>Relators := ["[b,a]^3"]</code> with <code>PqWorkspace</code> near its limit: $2^7$ instead of $2^6$',
                   '<code>Relators := ["[b,a]^3"]</code> при <code>PqWorkspace</code> у самого предела: $2^7$ вместо $2^6$')),

    dict(anchor="sp-pquotient", fix="sp_pquotient", cls="bad",
         defect=t("<code>StandardPresentation</code> with a <code>pQuotient</code> in another pc presentation",
                  "<code>StandardPresentation</code> с <code>pQuotient</code> в другой pc-презентации"),
         effect=t("wrong standard presentation; pq crash", "неверная стандартная презентация; падение pq"),
         reached=t("<code>pQuotient := Q</code> of class at least 2 whose pcgs is not pq's: order 64, 354 copies, "
                   "59 wrong, 109 crashes",
                   "<code>pQuotient := Q</code> класса не меньше 2, чей pcgs не совпадает с pcp pq: порядок 64, "
                   "354 копии, 59 неверных, 109 падений")),

    group("Second pass, crashes and errors", "Второй проход: падения и ошибки"),
    dict(anchor="gmp-separator", fix="gmp_separator", cls="bad",
         defect=t("Saved group files with GMP", "Файлы сохранённых групп при сборке с GMP"),
         effect=t("pq crash", "падение pq"),
         reached=t("<code>PqDescendants(CyclicGroup(53))</code>; every $p$ with $p \\bmod 256 \\in [48, 57]$ "
                   "(53, 307, 311, …)",
                   "<code>PqDescendants(CyclicGroup(53))</code>; любое $p$ с $p \\bmod 256 \\in [48, 57]$ "
                   "(53, 307, 311, …)")),
    dict(anchor="stabiliser-space", fix="stabiliser_space", cls="bad",
         defect=t("Schreier words without a space check", "Слова Шрайера без проверки места"),
         effect=t("memory overwrite; pq crash", "затирание памяти; падение pq"),
         reached=t("on master only through finding 1, e.g. a copy of <code>SmallGroup(256,1325)</code>",
                   "на master только через дефект 1, например копия <code>SmallGroup(256,1325)</code>")),
    dict(anchor="degree-overflow", fix="degree_overflow", cls="amb",
         defect=t("Overflow of the number of allowable subgroups", "Переполнение числа допустимых подгрупп"),
         effect=t("error; pq went on in a broken state", "ошибка; pq продолжал работу в испорченном состоянии"),
         reached=t("<code>StandardPresentation</code> of groups of large Frattini rank, e.g. rank 6, order $2^9$ "
                   "(issue #32)",
                   "<code>StandardPresentation</code> групп большого ранга Фраттини, например ранга 6 порядка $2^9$ "
                   "(задача #32 в трекере пакета)")),

    group("Second pass, wrong data", "Второй проход: неверные данные"),
    dict(anchor="gap-relorders", fix="gap_relorders", cls="amb",
         defect=t("Relative orders written for GAP", "Относительные порядки, записанные для GAP"),
         effect=t("wrong data", "неверные данные"),
         reached=t("<code>ANUPQAutomorphisms(D).relativeOrders</code> of a descendant: the last entry repeated",
                   "<code>ANUPQAutomorphisms(D).relativeOrders</code> у потомка: последний элемент повторён")),
    dict(anchor="stabiliser-relative", fix="stabiliser_relative", cls="amb",
         defect=t("Relative orders of a soluble stabiliser", "Относительные порядки разрешимого стабилизатора"),
         effect=t("wrong data", "неверные данные"),
         reached=t("<code>ANUPQAutomorphisms</code> of descendants: more soluble generators than automorphisms",
                   "<code>ANUPQAutomorphisms</code> у потомков: разрешимых порождающих больше, чем автоморфизмов")),
]

FIX_KEYS = [r["fix"] for r in FINDINGS if "fix" in r]

# Open items: what is still open after the second pass.
OPEN = [
    dict(item=t("With a very small <code>PqWorkspace</code>, below the total length of the relations (for our "
                "groups below about 1000 words), <code>setup</code> and the reading of relations write a few words "
                "past the end of the workspace before, or instead of, reporting <code>Ran out of space</code>. Plain "
                "builds stop with that message in every case we tried; only AddressSanitizer sees the writes",
                "При очень маленьком <code>PqWorkspace</code>, меньше суммарной длины соотношений (для наших групп "
                "меньше примерно 1000 слов), <code>setup</code> и чтение соотношений пишут несколько слов за конец "
                "рабочей памяти до сообщения <code>Ran out of space</code> или вместо него. Обычные сборки во всех "
                "проверенных случаях останавливаются с этим сообщением; записи видит только AddressSanitizer"),
         where="<code>src/setup.c:75</code>, <code>src/pretty_filter.c:195, 420</code>",
         status=t("verified (ASan); harmless in practice; patch kept, no PR",
                  "подтверждено (ASan); на практике безвредно; патч есть, PR не открываем")),
    dict(item=t("<code>image_of_generator</code> writes the image of a generator into the workspace without a "
                "space check. Its length is bounded by $(p-1)^2 \\cdot \\mathrm{lastg}^2$, more than the nearest "
                "check reserves ($7 \\cdot \\mathrm{lastg} + 4$)",
                "<code>image_of_generator</code> пишет образ порождающего в рабочую память без проверки места. "
                "Его длина ограничена величиной $(p-1)^2 \\cdot \\mathrm{lastg}^2$, а ближайшая проверка "
                "резервирует меньше ($7 \\cdot \\mathrm{lastg} + 4$)"),
         where="<code>src/stabiliser.c:227–281</code>",
         status=t("measured: at most 20 words written, at least 94 to spare, also at the smallest workspace that "
                  "suffices; documented risk",
                  "замерено: записывается не больше 20 слов, запас не меньше 94, в том числе при минимальной "
                  "достаточной рабочей памяти; известный риск")),
]

# Checked and refuted.
REFUTED = [
    dict(item=t("A non-homogeneous relation is reported and ignored, and the computation goes on "
                "(<code>src/echelon.c:52–60</code>).",
                "Неоднородное соотношение сообщается и отбрасывается, а вычисление продолжается "
                "(<code>src/echelon.c:52–60</code>)."),
         why=t("On <code>pq</code>'s own paths a relation can be non-homogeneous only if the previous class is already "
               "wrong; a probe build saw no case in the test suite or the SmallGroups check. Where a user hands in "
               "an arbitrary word (<code>PqCollect</code>, <code>PqEchelonise</code>), ignoring it is the right "
               "response: a relation that fails in a lower class cannot be imposed in class $c$. Only the report "
               "is weak: the message appears from <code>InfoANUPQ</code> level 4, and <code>PqEchelonise</code> "
               "returns <code>fail</code>.",
               "На собственных путях <code>pq</code> соотношение может быть неоднородным, только если предыдущий "
               "класс уже неверен; отладочная сборка не встретила ни одного такого случая ни в тестах пакета, ни в "
               "сверке с SmallGroups. Там, где пользователь подаёт произвольное слово (<code>PqCollect</code>, "
               "<code>PqEchelonise</code>), отбросить его правильно: соотношение, которое нарушено в младшем "
               "классе, нельзя наложить в классе $c$. Слабое место только в сообщении: оно видно начиная с уровня "
               "<code>InfoANUPQ</code> 4, а <code>PqEchelonise</code> возвращает <code>fail</code>.")),
    dict(item=t("One death of <code>pq</code> in the standard presentation check of order 64.",
                "Одна смерть <code>pq</code> в проверке стандартных презентаций порядка 64."),
         why=t("Not a defect: <code>pq</code> was killed from outside. At that second the audit itself ran "
               "<code>pkill -f \".../pq -G\"</code>, which matches every <code>pq</code> started by GAP from that "
               "build. Six reruns of order 64 (6408 calls of <code>PqStandardPresentation</code>; master, "
               "<code>correctness</code>, master under ASan) had no failure. The first run of order 128 died the "
               "same way.",
               "Это не дефект: <code>pq</code> был убит извне. В ту же секунду сам аудит выполнил "
               "<code>pkill -f \".../pq -G\"</code>, а под этот шаблон попадает любой <code>pq</code>, запущенный "
               "из GAP с этой сборкой. Шесть повторных прогонов порядка 64 (6408 вызовов "
               "<code>PqStandardPresentation</code>; master, <code>correctness</code>, master с ASan) прошли без "
               "сбоев. Первый прогон порядка 128 оборвался так же.")),
]

# Test added by each fix's pull request (tst/<name>.tst in the PR); none for #108 (see finding 21).
TESTS = {
    "aut_basis": "aut_basis.tst", "descendants_law": "descendants_law.tst", "sp_relators": "sp_relators.tst",
    "char_counters": "orbit_counters.tst", "sp_epimorphism": "sp_epimorphism.tst",
    "stale_descendants": "stale_descendants.tst", "savepqlist": "savepqlist.tst",
    "relative_orders": "relative_orders.tst", "isomorphic_trivial": "isomorphic_trivial.tst",
    "gmp_separator": "gmp_separator.tst", "exponent_queue": "exponent_queue.tst",
    "gap_relorders": "relative_orders_gap.tst", "commutator_workspace": "commutator_workspace.tst",
    "pcgs_automorphisms": "pcgs_automorphisms.tst", "epimorphism_non_pgroup": "epimorphism_non_pgroup.tst",
    "exponent_reduced_list": "exponent_reduced_list.tst", "degree_overflow": "degree_overflow.tst",
    "pc_generator_limit": "pc_generator_limit.tst", "stabiliser_relative": "stabiliser_relative.tst",
    "prime_bound": "prime_bound.tst", "gl_order": "gl_order.tst",
    "sp_pquotient": "sp_pquotient_basis.tst",
    "interface_bookkeeping": ["step_size_dialogue.tst", "group_name.tst", "sp_tmpdir.tst"],
}

# Files in data/: which findings (anchors) or other items they support. "page" links a non-finding target.
# The data page, data/README.txt and the links under each finding are all generated from this list.
DATA = [
    dict(id="desc-vs-sg", files=["desc_vs_sg.g"], findings=[], page="checks.html#smallgroups",
         what=t("descendants against SmallGroups (set <code>P</code>, <code>N</code>)",
                "потомки против SmallGroups (задайте <code>P</code>, <code>N</code>)")),
    dict(id="coords", files=["coords.g"], findings=["aut-basis"], page="checks.html#copies",
         what=t("descendants of three other presentations of each group", "потомки трёх других презентаций каждой группы")),
    dict(id="codes", files=["gen_codes.g", "codes.txt"], findings=["aut-basis"],
         what=t("the fixed list of copies (order, id, pc code)", "фиксированный список копий (порядок, номер, pc-код)")),
    dict(id="check-codes", files=["check_codes.g", "check_codes_master.txt", "check_codes_fixed.txt"], findings=["aut-basis"],
         what=t("the copies against SmallGroups, and the outputs on master and with the fix",
                "копии против SmallGroups и выводы на master и с исправлением")),
    dict(id="spcheck", files=["spcheck.g"], findings=[], page="checks.html#sp",
         what=t("standard presentations as an isomorphism key", "стандартная презентация как ключ изоморфизма")),
    dict(id="ds-children", files=["ds_children.g"], findings=["aut-basis"], page="checks.html#dimension-subrings",
         what=t("pq2048 children built in GAP (needs <code>dimension-subrings/compute</code>)",
                "дети pq2048, построенные в GAP (нужен <code>dimension-subrings/compute</code>)")),
    dict(id="pcgs-automorphisms", files=["pcgs_automorphisms.g"], findings=["pcgs-automorphisms"],
         what=t("136 against 161 descendants of $C_2^2$; the insoluble case $C_2^3$",
                "136 против 161 потомка $C_2^2$; неразрешимый случай $C_2^3$")),
    dict(id="exponent-reduced-list", files=["exponent_reduced_list.g"], findings=["exponent-reduced-list"],
         what=t("orders with and without supplied automorphisms, 19 cases", "порядки с заданными автоморфизмами и без них, 19 случаев")),
    dict(id="exponent-queue", files=["exponent_queue.g", "exponent_queue_standalone.pq"], findings=["exponent-queue"],
         what=t("GAP: $GL(7,2)$ with exponent 2 (repeat it, the outcome varies); standalone input for an ASan build",
                "GAP: $GL(7,2)$ с экспонентой 2 (повторите несколько раз, исход меняется); вход автономного pq для сборки с ASan")),
    dict(id="gl-order", files=["gl_order.g"], findings=["gl-order"],
         what=t("the <code>glOrder</code> printed for $(C_{101})^2$", "<code>glOrder</code>, напечатанный для $(C_{101})^2$")),
    dict(id="epimorphism-non-pgroup", files=["epimorphism_non_pgroup.g"], findings=["epimorphism-non-pgroup"],
         what=t("cases A–F: homomorphism and surjectivity of both maps", "случаи A–F: гомоморфность и сюръективность обоих отображений")),
    dict(id="interface-bookkeeping", files=["step_size.g", "sp_tmpdir.g", "group_name.g"], findings=["interface-bookkeeping"],
         what=t("(a) step size above the nuclear rank, (b) temporary directory, (c) group name with <code>_</code>",
                "(a) шаг больше ядерного ранга, (b) временный каталог, (c) имя группы с <code>_</code>")),
    dict(id="prime-bound", files=["prime_bound.g", "composite_prime.in"], findings=["prime-bound"],
         what=t("$p = 32749$ against $p = 32771$; standalone input with $p = 9$ (hangs on master)",
                "$p = 32749$ против $p = 32771$; вход автономного pq с $p = 9$ (на master зависает)")),
    dict(id="pc-generator-limit", files=["pc_generator_limit.g", "free361.in"], findings=["pc-generator-limit"],
         what=t("GAP, 50 ms; the same for the standalone <code>pq</code> (needs <code>-s 400000000</code>)",
                "GAP, 50 мс; то же для автономного <code>pq</code> (нужен <code>-s 400000000</code>)")),
    dict(id="commutator-workspace", files=["commutator_workspace.g"], findings=["commutator-workspace"],
         what=t("$2^6$ against $2^7$ at <code>PqWorkspace := 210</code>", "$2^6$ против $2^7$ при <code>PqWorkspace := 210</code>")),
    dict(id="sp-pquotient", files=["sp_pquotient.g"], findings=["sp-pquotient"],
         what=t("one wrong standard presentation and one crash, order 64", "одна неверная стандартная презентация и одно падение, порядок 64")),
    dict(id="gmp-separator", files=["gmp_separator.g"], findings=["gmp-separator"],
         what=t("descendants of $C_{53}$ and $C_{53}^2$", "потомки $C_{53}$ и $C_{53}^2$")),
    dict(id="stabiliser-space", files=["stabiliser_space.g"], findings=["stabiliser-space"],
         what=t("a copy of <code>SmallGroup(256, 1325)</code>; run with an ASan build of master",
                "копия <code>SmallGroup(256, 1325)</code>; запускать со сборкой master с ASan")),
    dict(id="degree-overflow", files=["degree_overflow.g"], findings=["degree-overflow"],
         what=t("a group of rank 6 and order $2^9$ whose standard presentation overflows",
                "группа ранга 6 порядка $2^9$, у которой стандартная презентация переполняется")),
    dict(id="relative-orders-gap", files=["relative_orders_gap.g"], findings=["gap-relorders"],
         what=t("<code>relativeOrders</code> against the number of automorphisms of descendants",
                "<code>relativeOrders</code> против числа автоморфизмов у потомков")),
    dict(id="stabiliser-relative", files=["stabiliser_relative.g"], findings=["stabiliser-relative"],
         what=t("soluble generators against automorphisms of descendants", "разрешимые порождающие против автоморфизмов у потомков")),
    dict(id="tiny-workspace", files=["tiny_workspace.in", "tiny_workspace.g"], findings=[], page="open.html",
         what=t("open item: a tiny workspace, standalone (<code>pq -s N</code>) and through GAP",
                "открытый вопрос: крошечная рабочая память, автономно (<code>pq -s N</code>) и через GAP")),
    dict(id="non-homogeneous", files=["non_homogeneous.g"], findings=[], page="open.html#refuted",
         what=t("refuted: a non-homogeneous relation handed to <code>PqEchelonise</code>",
                "опровергнуто: неоднородное соотношение, переданное в <code>PqEchelonise</code>")),
    dict(id="pq-killed", files=["pq_killed.g"], findings=[], page="open.html#refuted",
         what=t("refuted: an outside kill of <code>pq</code> gives the error of the order-64 run",
                "опровергнуто: внешнее убийство <code>pq</code> даёт ту же ошибку, что в прогоне порядка 64")),
]
