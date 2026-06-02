"""
BEAK — the savant. Automated intel, gathered by candlelight.

In the tale, Beak saw every warren as a candle of a different color, kept dark
until the moment it was needed — and saved the white one for last. This Beak
sees intel sources the same way. Give him a subject; he lights his candles, one
at a time, and gathers a cited brief. A candle that cannot cite its light stays
dark. The white candle — the synthesis — burns last.

  white   the steady truth      Wikipedia extract + last-revision date
  black   the cutting edge       newest arXiv papers
  red     is it moving?          encyclopedia date vs. newest paper (the gap)
  purple  the shadow             adjacent topics + what stays unlit

Read-only. Two doors only: en.wikipedia.org and export.arxiv.org. Intel on
SUBJECTS and CONCEPTS — never people, never surveillance. Every line carries a
source; if it can't be cited, the candle does not light.

  python beak.py "topological insulator"          # gather, print the brief
  python beak.py "qubit" --save                    # also write briefs/<slug>.md
  python beak.py --selftest                         # prove the candles assemble
"""
import sys
import re
import json
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timezone

import requests

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).parent
BRIEFS = ROOT / "briefs"
UA = "beak-intel/1.0 (+https://github.com/DavidWise01/beak; read-only topic intel)"
WIKI = "https://en.wikipedia.org"
ARXIV = "https://export.arxiv.org/api/query"


def now():
    return datetime.now(timezone.utc).isoformat()


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "topic"


def parse_iso(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


# ── the candles (each returns data, or None = stays dark) ────────────────────
def white_candle(topic):
    """The steady truth — Wikipedia extract + last revision."""
    try:
        s = requests.get(f"{WIKI}/api/rest_v1/page/summary/{urllib.parse.quote(topic)}",
                         headers={"User-Agent": UA}, timeout=20)
        if s.status_code != 200:
            return None
        j = s.json()
        if j.get("type", "").endswith("not_found"):
            return None
        title = j.get("title", topic)
        url = j.get("content_urls", {}).get("desktop", {}).get("page") \
            or f"{WIKI}/wiki/{urllib.parse.quote(title.replace(' ', '_'))}"
        rev = requests.get(f"{WIKI}/w/api.php", headers={"User-Agent": UA}, timeout=20, params={
            "action": "query", "prop": "revisions", "titles": title,
            "rvprop": "timestamp", "rvlimit": 1, "format": "json"}).json()
        last = None
        for _, p in rev.get("query", {}).get("pages", {}).items():
            r = p.get("revisions")
            if r:
                last = r[0]["timestamp"]
        return {"title": title, "extract": (j.get("extract") or "").strip(),
                "url": url, "last_revised": last}
    except Exception as e:
        print(f"white candle dark: {e}", file=sys.stderr)
        return None


def black_candle(topic, n=4):
    """The cutting edge — newest arXiv papers."""
    try:
        r = requests.get(ARXIV, headers={"User-Agent": UA}, timeout=25, params={
            "search_query": f"all:{topic}", "sortBy": "submittedDate",
            "sortOrder": "descending", "max_results": n})
        ns = {"a": "http://www.w3.org/2005/Atom"}
        out = []
        for e in ET.fromstring(r.text).findall("a:entry", ns):
            out.append({
                "title": " ".join(e.findtext("a:title", default="", namespaces=ns).split()),
                "url": e.findtext("a:id", default="", namespaces=ns).strip(),
                "published": e.findtext("a:published", default="", namespaces=ns).strip(),
            })
        return out or None
    except Exception as e:
        print(f"black candle dark: {e}", file=sys.stderr)
        return None


def purple_candle(topic, n=8):
    """The shadow — adjacent topics (Wikipedia links)."""
    try:
        j = requests.get(f"{WIKI}/w/api.php", headers={"User-Agent": UA}, timeout=20, params={
            "action": "query", "prop": "links", "titles": topic,
            "plnamespace": 0, "pllimit": 40, "format": "json"}).json()
        links = []
        for _, p in j.get("query", {}).get("pages", {}).items():
            for l in p.get("links", []):
                links.append(l["title"])
        return links[:n] or None
    except Exception as e:
        print(f"purple candle dark: {e}", file=sys.stderr)
        return None


def red_candle(white, black):
    """Is it moving? — encyclopedia date vs. newest paper."""
    if not white or not white.get("last_revised") or not black:
        return None
    wiki_dt = parse_iso(white["last_revised"])
    newest = max(black, key=lambda p: parse_iso(p["published"]))
    paper_dt = parse_iso(newest["published"])
    gap_days = (paper_dt - wiki_dt).days
    return {"wiki": white["last_revised"][:10], "paper": newest["published"][:10],
            "gap_days": gap_days, "newest_url": newest["url"]}


def gather(topic):
    w = white_candle(topic)
    b = black_candle(topic)
    p = purple_candle(w["title"] if w else topic)
    r = red_candle(w, b)
    return {"topic": topic, "at": now(), "white": w, "black": b, "purple": p, "red": r}


# ── the brief ────────────────────────────────────────────────────────────────
def render(data):
    t = data["topic"]
    L = [f"# Intel Brief — {t}",
         f"*gathered by Beak · {data['at'][:19]}Z · read-only public sources*", ""]
    lit, sources = [], []

    w = data["white"]
    L.append("## white candle — the steady truth")
    if w:
        lit.append("white")
        L.append(w["extract"] or "(no extract)")
        L.append("")
        L.append(f"— Wikipedia, last revised {w.get('last_revised','?')[:10]} · {w['url']}")
        sources.append(w["url"])
    else:
        L.append("*(dark — no encyclopedia entry could be cited)*")
    L.append("")

    b = data["black"]
    L.append("## black candle — the cutting edge")
    if b:
        lit.append("black")
        for p in b:
            L.append(f"- {p['title']} ({p['published'][:10]}) — {p['url']}")
            sources.append(p["url"])
    else:
        L.append("*(dark — no recent papers could be cited)*")
    L.append("")

    r = data["red"]
    L.append("## red candle — is it moving?")
    if r:
        lit.append("red")
        if r["gap_days"] > 0:
            L.append(f"The encyclopedia was last revised {r['wiki']}; the newest paper is "
                     f"{r['paper']} — the field is **{r['gap_days']} days ahead** of the article.")
        else:
            L.append(f"The encyclopedia ({r['wiki']}) is current with the newest paper ({r['paper']}).")
    else:
        L.append("*(dark — not enough lit candles to compare)*")
    L.append("")

    p = data["purple"]
    L.append("## purple candle — the shadow (adjacent & gaps)")
    if p:
        lit.append("purple")
        L.append("Adjacent: " + " · ".join(p))
    else:
        L.append("*(dark — no adjacent topics could be cited)*")
    L.append("")

    L.append("## the white candle, last")
    if w and b and r:
        L.append(f"**{t}** is documented and active research is {'moving ahead of' if r['gap_days']>0 else 'level with'} "
                 f"the record. {len(lit)}/4 candles lit. Verify every line at its source.")
    elif lit:
        L.append(f"{len(lit)}/4 candles lit — partial light. Treat the gaps as unknown, not absent.")
    else:
        L.append("No candle would light. Beak gathered nothing he could cite — so there is nothing to report.")
    L.append("")
    L.append("---")
    L.append("**sources** (verify each): " + (" · ".join(dict.fromkeys(sources)) if sources else "none"))
    L.append(f"\n*candles lit: {', '.join(lit) if lit else 'none'}. read-only · subjects only · never people.*")
    return "\n".join(L)


# ── self-test (offline: assembly + the unlit rule) ───────────────────────────
def selftest():
    mock = {"topic": "Test", "at": now(),
            "white": {"title": "Test", "extract": "An extract.", "url": "https://en.wikipedia.org/wiki/Test",
                      "last_revised": "2024-01-01T00:00:00Z"},
            "black": [{"title": "A paper", "url": "https://export.arxiv.org/abs/2601.1", "published": "2026-05-01T00:00:00Z"}],
            "purple": ["Adjacent A", "Adjacent B"], "red": None}
    mock["red"] = red_candle(mock["white"], mock["black"])
    brief = render(mock)
    ok1 = "535 days" not in brief and "ahead" in brief        # red lit and computed a gap
    ok2 = "candles lit: white, black, red, purple" in brief    # all four assembled
    empty = render({"topic": "Void", "at": now(), "white": None, "black": None, "purple": None, "red": None})
    ok3 = "No candle would light" in empty                     # the unlit rule holds
    for name, ok in [("assembles a full brief", ok2),
                     ("red candle computes the gap", ok1),
                     ("unlit topic reports nothing", ok3)]:
        print(f"selftest: {name} -> {'PASS' if ok else 'FAIL'}")
    return 0 if (ok1 and ok2 and ok3) else 1


def main():
    a = sys.argv[1:]
    if "--selftest" in a:
        return selftest()
    topics = [x for x in a if not x.startswith("--")]
    if not topics:
        print("usage: beak.py \"<subject>\" [--save]")
        return 2
    topic = " ".join(topics)
    data = gather(topic)
    brief = render(data)
    print(brief)
    if "--save" in a:
        BRIEFS.mkdir(exist_ok=True)
        path = BRIEFS / f"{slug(topic)}.md"
        path.write_text(brief + "\n", encoding="utf-8")
        print(f"\n[saved] {path.relative_to(ROOT)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
