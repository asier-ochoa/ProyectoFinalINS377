from mariadb import Cursor


def create_content_type(content_type: str, cursor: Cursor):
    cursor.execute(
        """
        INSERT INTO `Space&Ad_type`(type)
        VALUES (?)
        """,
        [content_type]
    )
