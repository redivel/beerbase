from __future__ import annotations

import csv

from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from typing import Optional, List
from pathlib import Path
from logging import getLogger

from beerbase.datatypes import Beer
from beerbase.utils import Singleton

logger = getLogger("logger")


class Database(metaclass=Singleton):
    """Singleton class to maintain connection to database."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        if db_path is None:
            raise ValueError("No database URL passed")
        else:
            try:
                url = f'sqlite:///{db_path}'
                self.engine = create_engine(url=url, echo=False)
                Session = sessionmaker(bind=self.engine)
                self.session = Session()
            except Exception as exc:
                raise ConnectionError("Failed to connect to database.") from exc


class DatabaseHandler:
    """Class in charge of communicating with the database."""

    def __init__(self):
        self.session = Database().session

    def load_csv(self, path: Path):
        """Load contents of csv specified by file into database.

        Args:
            path (Path): Path to csv data file.
        """

        try:
            with path.open('r') as file:
                reader = csv.reader(file)
                next(reader)
                header = ['abv', 'ibu', 'beer_id', 'name', 'style', 'brewery_id', 'size']
                data = []
                for row in reader:
                    beer_dict = {header[i]: row[i] for i in range(0, len(row))}
                    if not beer_dict['abv'].strip():
                        beer_dict['abv'] = None
                    if not beer_dict['ibu'].strip():
                        beer_dict['ibu'] = None
                    beer = Beer.from_dict(beer_dict)
                    self.session.add(beer)
        except Exception as exc:
            logger.error(exc)
        else:
            try:
                self.session.commit()
            except Exception as exc:
                logger.error(exc)

    def get_beers(self, abv: Optional[float] = -1,
                  ibu: Optional[float] = -1,
                  beer_id: Optional[int] = None,
                  name: Optional[str] = None,
                  style: Optional[str] = -1,
                  brewery_id: Optional[int] = None,
                  size: Optional[float] = None) \
            -> List[Beer]:
        """Get beers matching either of specified attributes.

        Args:
            abv (float): ABV (Alcohol by Volume) of searched beer(s).
            ibu (float): IBU (International Bitterness Unit) of searched beer(s).
            beer_id (int): ID of searched beer.
            name (str): Name of searched beer.
            style (str): Style of searched beer(s).
            brewery_id (int): ID of brewer of searched beer(s).
            size (float): Size of searched beer(s) in ounces.

        Returns:
            List[Beer]: List of beers matching either of specified attributes.
        """

        results = []
        try:

            for beer in self.session.query(Beer).filter(or_(Beer.abv == abv,
                                                            Beer.ibu == ibu,
                                                            Beer.beer_id == beer_id,
                                                            Beer.name == name,
                                                            Beer.style == style,
                                                            Beer.brewery_id == brewery_id,
                                                            Beer.size == size)):
                results.append(beer.to_dict())
            print(results)
        except Exception as exc:
            raise RuntimeError("Could not retrieve beer(s) from database.") from exc
        return results

    def delete_beer(self, beer_id: int) -> str:
        """Delete beer with specified ID.

        Args:
            beer_id (int): ID of beer to be deleted.

        Returns:
            str: String confirming deletion.
        """
        try:
            beer = self.session.query(Beer).filter(Beer.beer_id == beer_id).first()
            if beer is None:
                raise ValueError("No beer with such ID exists.")
            self.session.delete(beer)
        except Exception as exc:
            if not isinstance(exc, ValueError):
                raise RuntimeError("Internal server error") from exc
            else:
                raise exc
        else:
            try:
                self.session.commit()
            except Exception as exc:
                logger.error(exc)

        return "Successfully deleted."
