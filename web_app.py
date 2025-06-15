#!/usr/bin/env python3
"""Simple Flask app to manage the offline article database."""

from flask import Flask, request, redirect, url_for, render_template_string
import offline_db

app = Flask(__name__)
offline_db.init_db()

INDEX_TEMPLATE = """
<!doctype html>
<title>Articles</title>
<h1>Base d'articles</h1>
<form method="get" action="/">
    <input type="text" name="q" placeholder="Rechercher" value="{{ request.args.get('q', '') }}">
    <input type="submit" value="Chercher">
</form>
<form method="post" action="/add">
    <input type="text" name="name" placeholder="Nom" required>
    <input type="text" name="ean" placeholder="EAN">
    <input type="text" name="plu" placeholder="PLU">
    <input type="submit" value="Ajouter">
</form>
<ul>
{% for a in articles %}
    <li>{{ a[1] }} - EAN: {{ a[2] or '' }} - PLU: {{ a[3] or '' }}</li>
{% endfor %}
</ul>
"""


@app.route("/", methods=["GET"])
def index():
    term = request.args.get("q", "").strip()
    if term:
        articles = offline_db.search_article(term)
    else:
        articles = offline_db.list_articles()
    return render_template_string(INDEX_TEMPLATE, articles=articles)


@app.route("/add", methods=["POST"])
def add_article():
    name = request.form.get("name")
    ean = request.form.get("ean") or None
    plu = request.form.get("plu") or None
    offline_db.add_article(name, ean, plu)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
