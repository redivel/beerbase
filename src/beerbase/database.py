from __future__ import annotations

import csv

import kwargs as kwargs
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from typing import Optional, List
from pathlib import Path

from datatypes import Beer
from utils import Singleton


class Database(metaclass=Singleton):
    """Singleton class to maintain connection to database."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        if db_path is None:
            raise ValueError("No database URL passed")
        else:
            try:
                url = f'sqlite:///{db_path}'
                self.engine = create_engine(url=url, echo=True)
                Session = sessionmaker(bind=self.engine)
                self.session = Session()
            except Exception as exc:
                raise ConnectionError("Failed to connect to database.") from exc


class Database_handler():
    def __init__(self):
        self.session = Database().session

    def load_csv(self, path: Path):
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
            self.session.commit()

    def get_beers(self, abv: Optional[float] = None,
                  ibu: Optional[float] = None,
                  beer_id: Optional[int] = None,
                  name: Optional[str] = None,
                  style: Optional[str] = None,
                  brewery_id: Optional[int] = None,
                  size: Optional[float] = None) -> List[Beer]:

        results = []
        try:
            # for beer in self.session.query(Beer).filter_by(beer_id=kwargs['beer_id']):
            #     beers.append(beer.to_dict())
            for beer in self.session.query(Beer).filter(or_(Beer.abv==abv,
                                                            Beer.ibu==ibu,
                                                            Beer.beer_id==beer_id,
                                                            Beer.name==name,
                                                            Beer.style==style,
                                                            Beer.brewery_id==brewery_id,
                                                            Beer.size==size)):
                results.append(beer.to_dict())
        except Exception as exc:
            raise RuntimeError("Could not retrieve beer(s) from database.") from exc
        return results
