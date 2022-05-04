from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import Dict, Union

class Serializable():
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
class Beer(Serializable):
    """Class containing all attributes known about a beer."""

    abv: float
    ibu: float
    beer_id: int
    name: str
    style: str
    brewery_id: int
    size: float

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
