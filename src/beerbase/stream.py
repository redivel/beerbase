from __future__ import annotations

from typing import Optional, List, Dict, Union
from logging import getLogger

from beerbase.database import Database, DatabaseHandler

handler = DatabaseHandler()
logger = getLogger("logger")


def get_beer(abv: Optional[float] = -1,
             ibu: Optional[float] = -1,
             beer_id: Optional[int] = None,
             name: Optional[str] = None,
             style: Optional[str] = -1,
             brewery_id: Optional[int] = None,
             size: Optional[float] = None
             ) \
        -> tuple[Union[str, List[Dict[str, Union[int, float, str]]]], int]:
    """Handler for /beer endpoint

    Args:
        abv (float): ABV (Alcohol by Volume) of searched beer(s).
        ibu (float): IBU (International Bitterness Unit) of searched beer(s).
        beer_id (int): ID of searched beer(s).
        name (str): Name of searched beer(s).
        style (str): Style of searched beer(s).
        brewery_id (int): ID of brewer of searched beer(s).
        size (float): Size of searched beer(s) in ounces.

    Returns: tuple[Union[str, List[Dict[str, Union[int, float, str]]], int]]: Tuple containing the response to the
    request and corresponding status code.
    """

    response = None
    code = 200

    try:
        logger.info(f'Get beer(s) abv: {abv}, ibu: {ibu}, beer_id: {beer_id}, name: {name}, style: {style}, '
                    f'brewery_id: {brewery_id}, size: {size}')
        response = handler.get_beers(abv=abv, ibu=ibu, beer_id=beer_id, name=name, style=style,
                                     brewery_id=brewery_id, size=size)
    except Exception as exc:
        response = "Could not retrieve beer(s) from database."
        code = 500
        logger.error(f'{response}\n'
                     f'Cause:\n'
                     f'{exc}')
    else:
        if not response:
            response = "No such beer found."
            code = 400
            logger.error(response)
        else:
            logger.info(f'Successfully got {len(response)} beer(s)')

    return response, code


def delete_beer(beer_id: int) -> tuple[str, int]:
    """Handler for /beer/delete endpoint.

    Tries to remove beer with given id from database.

    Args:
        beer_id (int): ID of beer to be deleted.

    Returns:
        tuple[str, int]: Tuple containing the response to the request and corresponding status code.
    """

    response = None
    code = 200

    try:
        logger.info(f'Delete beer beer_id: {beer_id}')
        handler.delete_beer(beer_id)
        response = "Beer successfully deleted."
    except Exception as exc:
        if isinstance(exc, ValueError):
            response = "No beer with such ID exists."
            code = 400
            logger.error(response)
        else:
            response = "Internal server error."
            code = 500
            logger.error(f'{response}\n'
                         f'Cause:\n'
                         f'{exc}')
    else:
        logger.info(f'Successfully deleted beer with id: {beer_id}')

    return response, code
