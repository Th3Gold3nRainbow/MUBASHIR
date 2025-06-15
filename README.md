# Offline Article Database

Ce dépôt contient un petit script Python (`offline_db.py`) pour gérer une base
de données locale d'articles avec leurs codes EAN et PLU. La base de données est
stockée en SQLite pour fonctionner hors ligne.

## Prérequis
- Python 3

## Installation
Aucune installation n'est nécessaire. Clonez simplement le dépôt et exécutez le
script à l'aide de Python :

```bash
python3 offline_db.py --help
```

## Ajouter un article
Pour ajouter un nouvel article :

```bash
python3 offline_db.py add "Nom de l'article" --ean 1234567890123 --plu 9876
```

## Rechercher un article
Vous pouvez rechercher par nom, EAN ou PLU :

```bash
python3 offline_db.py search 1234567890123
```

Le script affiche alors les articles correspondants.

La base de données est créée automatiquement dans le fichier `articles.db` (qui
n'est pas suivi par git).

## Interface web
Une petite interface web est disponible à l'aide de Flask. Installez la
dépendance puis lancez le serveur :

```bash
pip install -r requirements.txt
python3 web_app.py
```

Ouvrez ensuite `http://localhost:5000` dans votre navigateur pour ajouter ou
rechercher des articles via une page web simple.
