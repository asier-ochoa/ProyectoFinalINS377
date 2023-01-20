from typing import Any, Iterable
from configuration import config
from mariadb import Cursor, connect, Connection


class DuplicatedEntityException(Exception):
    pass


class EntityNotFoundException(Exception):
    pass


# Fetches table description to transform list of lists into list of dicts with key as the header name
def rows_to_dict(cursor: Cursor, table: list[Iterable] | Iterable) -> list[dict[str, Any]] | dict[str, Any] | None:
    header = cursor.description
    if table is None:
        return None
    else:
        if isinstance(table, list):
            return [{h[0]: x for h, x in zip(header, r)} for r in table]
        else:
            return {h[0]: x for h, x in zip(header, table)}


# Database connection wrapper
def db_connect() -> Connection | None:
    db_conf = config.mariadb
    return connect(host=db_conf.host, port=db_conf.port, user=db_conf.user, passwd=db_conf.password,
                   db=db_conf.database, autocommit=True)


# REDUNDANT
def get_content_type_id(ad_type: str, cursor: Cursor) -> int | None:
    cursor.execute(
        """
        SELECT id FROM `Space&Ad_type` WHERE type=?
        """,
        [ad_type]
    )
    ad_type_id = rows_to_dict(cursor, cursor.fetchone())
    if ad_type_id is None:
        return None
    ad_type_id = ad_type_id['id']
