"""
Read-Only UI for Fragment Exploration

UPDATED:
- Pagination
- Similarity threshold filtering
- Still strictly read-only
"""

import sqlite3
import json
from flask import Flask, request, render_template_string

DB_PATH = "fragments.db"
STAGE1_LOG = "logs/concept_stage1.json"
PAGE_SIZE = 10

app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<title>Fragment Browser (Read-Only)</title>
<h1>Fragment Browser</h1>
<form method="get">
  <input type="text" name="q" placeholder="search fragments" value="{{ query }}" />
  <input type="number" step="0.01" name="sim" placeholder="similarity ≥" value="{{ sim }}" />
  <input type="submit" value="Apply" />
</form>
<hr/>
{% for f in fragments %}
  <div style="margin-bottom:1em;">
    <strong>Fragment {{ f['id'] }}</strong><br/>
    <pre>{{ f['content'] }}</pre>
    {% if f['related'] %}
      <em>Related fragments:</em>
      <ul>
        {% for r in f['related'] %}
          <li>Fragment {{ r }}</li>
        {% endfor %}
      </ul>
    {% endif %}
  </div>
{% endfor %}
<div>
{% if page > 1 %}<a href="?page={{ page - 1 }}">Prev</a>{% endif %}
Page {{ page }}
{% if has_more %}<a href="?page={{ page + 1 }}">Next</a>{% endif %}
</div>
"""


def load_fragments(query=None, page=1):
    offset = (page - 1) * PAGE_SIZE
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    if query:
        cur.execute(
            "SELECT id, content FROM fragments WHERE content LIKE ? LIMIT ? OFFSET ?",
            (f"%{query}%", PAGE_SIZE + 1, offset),
        )
    else:
        cur.execute(
            "SELECT id, content FROM fragments LIMIT ? OFFSET ?",
            (PAGE_SIZE + 1, offset),
        )

    rows = cur.fetchall()
    conn.close()

    has_more = len(rows) > PAGE_SIZE
    return [dict(r) for r in rows[:PAGE_SIZE]], has_more


def load_similarity(min_sim=None):
    try:
        with open(STAGE1_LOG) as f:
            data = json.load(f)
        signals = data.get("signals", [])
    except FileNotFoundError:
        return {}

    related = {}
    for s in signals:
        if min_sim is not None and s.get("similarity", 0) < min_sim:
            continue
        related.setdefault(s["a"], []).append(s["b"])
        related.setdefault(s["b"], []).append(s["a"])
    return related


@app.route("/fragments")
def fragments_view():
    query = request.args.get("q")
    page = int(request.args.get("page", 1))
    sim = request.args.get("sim")
    min_sim = float(sim) if sim else None

    fragments, has_more = load_fragments(query, page)
    related_map = load_similarity(min_sim)

    for f in fragments:
        f["related"] = related_map.get(f["id"], [])

    return render_template_string(
        TEMPLATE,
        fragments=fragments,
        query=query or "",
        page=page,
        has_more=has_more,
        sim=sim or "",
    )


if __name__ == "__main__":
    app.run(debug=True)
