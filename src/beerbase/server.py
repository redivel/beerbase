from __future__ import annotations

import connexion
import sys

from flask import render_template
from argparse import ArgumentParser, Namespace
from pathlib import Path
from logging import INFO, getLogger, Formatter, StreamHandler

from database import Database, Database_handler
from datatypes import Base

app = connexion.App("beerbase")


@app.route("/")
def home():
    """
    This function just responds to the browser URL
    localhost:5000/

    Returns:
        The rendered template "home.html".
    """

    return render_template("home.html")


def parse_args() -> Namespace:
    """Argument parser to define paths of external files

    Returns:
        Namespace: parsed args.
    """

    parser = ArgumentParser()

    parser.add_argument("--templates", help="Absolute path of templates folder", type=Path, required=True)
    parser.add_argument("--assets", help="Absolute path of assets folder", type=Path, required=True)
    parser.add_argument("--db", help="Absolute path of database file", type=Path, required=True)
    parser.add_argument("--data", help="Absolute path of data file", type=Path, required=True)

    return parser.parse_args()


def init_db(db_path: Path, csv_path: Path) -> None:
    """Set's up database and loads contents of csv in.

    Args:
        db_path (Path): Path to database file.
        csv_path (Path): Path to csv datafile.
    """

    if not db_path.exists():
        file = db_path.open('w')
        file.close()

    db = Database(db_path=str(db_path))
    Base.metadata.drop_all(db.engine)
    Base.metadata.create_all(db.engine)

    if csv_path.exists():
        handler = Database_handler()
        handler.load_csv(csv_path)


def set_logger() -> None:
    """Set's up logger"""

    FORMAT = '%(levelname)-7s:%(asctime)s: %(message)s'
    formatter = Formatter(FORMAT)

    handler = StreamHandler(stream=sys.stdout)
    handler.setLevel(INFO)
    handler.setFormatter(formatter)

    logger = getLogger("logger")
    logger.addHandler(handler)
    logger.setLevel(INFO)


def main():
    set_logger()

    args = parse_args()

    # Initialize database
    init_db(db_path=args.db, csv_path=args.data)

    # Create app and link external file locations
    app.specification_dir = args.assets
    app.add_api(specification="openapi_cfg.yaml")
    app.app.template_folder = args.templates

    app.run(debug=False, threaded=False)


if __name__ == "__main__":
    main()
