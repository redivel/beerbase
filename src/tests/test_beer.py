from __future__ import annotations

from beerbase.database import Database, DatabaseHandler
from beerbase.datatypes import Beer

db = Database("A:/Projects/Intern_Test/beerbase/data/beerbase.sqlite")
handler = DatabaseHandler()

assert handler.get_beers(beer_id=999)[0] == {
        "abv": 0.067,
        "beer_id": 999,
        "brewery_id": 150,
        "ibu": 70.0,
        "name": "Watershed IPA (2013)",
        "size": 12.0,
        "style": "American IPA"
}

assert handler.delete_beer()
