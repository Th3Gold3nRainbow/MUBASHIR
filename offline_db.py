#!/usr/bin/env python3
import sqlite3
import argparse
from pathlib import Path

DB_PATH = Path(__file__).with_name('articles.db')


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            ean TEXT UNIQUE,
            plu TEXT UNIQUE
        )
        """
    )
    conn.commit()
    conn.close()


def add_article(name, ean=None, plu=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO articles (name, ean, plu) VALUES (?, ?, ?)", (name, ean, plu))
    conn.commit()
    conn.close()


def search_article(term):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        SELECT id, name, ean, plu
        FROM articles
        WHERE name LIKE ? OR ean = ? OR plu = ?
        """,
        (f"%{term}%", term, term),
    )
    results = c.fetchall()
    conn.close()
    return results


def list_articles():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        SELECT id, name, ean, plu
        FROM articles
        ORDER BY id
        """
    )
    results = c.fetchall()
    conn.close()
    return results


def main():
    parser = argparse.ArgumentParser(description="Offline Article Database CLI")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add a new article")
    add_parser.add_argument("name", help="Article name")
    add_parser.add_argument("--ean", help="EAN code")
    add_parser.add_argument("--plu", help="PLU code")

    search_parser = subparsers.add_parser("search", help="Search for article")
    search_parser.add_argument("term", help="Name, EAN or PLU to search")

    args = parser.parse_args()

    init_db()

    if args.command == "add":
        add_article(args.name, args.ean, args.plu)
        print("Article added.")
    elif args.command == "search":
        results = search_article(args.term)
        if results:
            for r in results:
                print(f"ID: {r[0]} | Name: {r[1]} | EAN: {r[2]} | PLU: {r[3]}")
        else:
            print("No matching article found.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
