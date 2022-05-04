from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import Dict, Union, Optional

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Text, Float, null


Base = declarative_base()


class Serializable:
    """Interface for serializable classes."""
    __metaclass__ = ABC

    def to_dict(self) -> Dict[str, Union[int, float, str]]:
        """Serializes the object into a dictionary.

        Returns:
            Dict[str, Union[int, float, str]]: Dictionary containing contents of the object.
        """
        pass

    def from_dict(cls, value: Dict[str, Union[int, float, str]]) -> Serializable:
        """Creates an object from a dictionary containing its contents.

        Args:
            value(Dict[str, Union[int, float, str]]): Dictionary containing contents of the object.

        Returns:
            Dictable: Object containing the contents given in Dictionary.
        """
        pass


@dataclass
class Beer(Serializable, Base):
    """Class containing all attributes known about a beer."""

    __tablename__ = 'beers'

    abv = Column(Float, nullable=True)
    ibu = Column(Float, nullable=True)
    beer_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    style = Column(Text, nullable=False)
    brewery_id = Column(Integer, nullable=False)
    size = Column(Float, nullable=False)

    def __init__(self,
                 beer_id: int,
                 name: str,
                 style: str,
                 brewery_id: int,
                 size: float,
                 abv: Optional[float] = null(),
                 ibu: Optional[float] = null()):
        self.abv = abv
        if ibu is None:
            self.ibu = null()
        else:
            self.ibu = ibu
        self.beer_id = beer_id
        self.name = name
        self.style = style
        self.brewery_id = brewery_id
        self.size = size

    def to_dict(self) -> Dict[str, Union[int, float, str]]:
        """See Serializable class"""

        return {
            "abv": self.abv,
            "ibu": self.ibu,
            "beer_id": self.beer_id,
            "name": self.name,
            "style": self.style,
            "brewery_id": self.brewery_id,
            "size": self.size
        }

    @classmethod
    def from_dict(cls, value: Dict[str, Union[int, float, str]]) -> Beer:
        """See Serializable class"""

        return cls(**value)

    def __str__(self) -> str:
        return self.to_dict()
