from __future__ import annotations

import connexion

from flask import render_template
from argparse import ArgumentParser, Namespace
from pathlib import Path

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

    return parser.parse_args()


def main():
    args = parse_args()

    # Create app and link external file locations
    app.specification_dir = args.assets
    app.add_api(specification="openapi_cfg.yaml")
    app.app.template_folder = args.templates

    app.run(debug=True, threaded=False)


if __name__ == "__main__":
    main()
