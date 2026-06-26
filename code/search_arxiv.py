#!/usr/bin/env python3
import sys, urllib.parse, urllib.request, re, html

def search(query, max_results=8):
    base = "http://export.arxiv.org/api/query?"
    q = urllib.parse.urlencode({
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending"
    })
    url = base + q
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            data = r.read().decode("utf-8")
    except Exception as e:
        print("ERROR:", e); return
    entries = re.findall(r"<entry>(.*?)</entry>", data, re.DOTALL)
    for e in entries:
        title = re.search(r"<title>(.*?)</title>", e, re.DOTALL)
        title = html.unescape(title.group(1).strip().replace("\n"," ")) if title else "?"
        idm = re.search(r"<id>(.*?)</id>", e)
        aid = idm.group(1).strip() if idm else "?"
        pub = re.search(r"<published>(.*?)</published>", e)
        pub = pub.group(1)[:10] if pub else "?"
        summ = re.search(r"<summary>(.*?)</summary>", e, re.DOTALL)
        summ = html.unescape(summ.group(1).strip().replace("\n"," ")) if summ else ""
        print(f"### {title}")
        print(f"ID: {aid} | Published: {pub}")
        print(f"Abstract: {summ[:600]}")
        print()

if __name__ == "__main__":
    search(sys.argv[1], int(sys.argv[2]) if len(sys.argv)>2 else 8)
