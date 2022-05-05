from __future__ import annotations

from abc import ABC
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

    @classmethod
    def from_dict(cls, value: Dict[str, Union[int, float, str]]) -> Serializable:
        """Creates an object from a dictionary containing its contents.

        Args:
            value(Dict[str, Union[int, float, str]]): Dictionary containing contents of the object.

        Returns:
            Dictable: Object containing the contents given in Dictionary.
        """
        pass


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
        return self.to_dict().__str__()
