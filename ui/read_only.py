"""
Read-Only UI for Fragment Exploration

Exposes:
- Fragment browser
- Read-only search (no concepts, no labels)
- Optional similarity view from Stage 1 outputs

Hard constraints:
- No mutation of fragments
- No concept naming
- No ontology exposure
"""

import sqlite3
import json
from flask import Flask, request, render_template_string

DB_PATH = "fragments.db"
STAGE1_LOG = "logs/concept_stage1.json"

app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<title>Fragment Browser (Read-Only)</title>
<h1>Fragment Browser</h1>
<form method="get">
  <input type="text" name="q" placeholder="search fragments" value="{{ query }}" />
  <input type="submit" value="Search" />
</form>
<hr/>
{% for f in fragments %}
  <div style="margin-bottom:1em;">
    <strong>Fragment {{ f['id'] }}</strong><br/>
    <pre>{{ f['content'] }}</pre>
    {% if f['related'] %}
      <em>Related fragments (similarity only):</em>
      <ul>
        {% for r in f['related'] %}
          <li>Fragment {{ r }}</li>
        {% endfor %}
      </ul>
    {% endif %}
  </div>
{% endfor %}
"""


def load_fragments(query=None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    if query:
        cur.execute("SELECT id, content FROM fragments WHERE content LIKE ?", (f"%{query}%",))
    else:
        cur.execute("SELECT id, content FROM fragments")

    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def load_similarity():
    try:
        with open(STAGE1_LOG) as f:
            data = json.load(f)
        signals = data.get("signals", [])
    except FileNotFoundError:
        return {}

    related = {}
    for s in signals:
        related.setdefault(s["a"], []).append(s["b"])
        related.setdefault(s["b"], []).append(s["a"])
    return related


@app.route("/fragments")
def fragments_view():
    query = request.args.get("q")
    fragments = load_fragments(query)
    related_map = load_similarity()

    for f in fragments:
        f["related"] = related_map.get(f["id"], [])

    return render_template_string(TEMPLATE, fragments=fragments, query=query or "")


if __name__ == "__main__":
    app.run(debug=True)
