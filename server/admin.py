from mariadb import Cursor


def create_content_type(content_type: str, cursor: Cursor):
    cursor.execute(
        """
        INSERT INTO `Space&Ad_type`(type)
        VALUES (?)
        """,
        [content_type]
    )


def create_category_tag(name: str, description: str, cursor: Cursor):
    cursor.execute(
        """
        INSERT INTO Category_tags(name, description)
        VALUES(?, ?)
        """,
        [name, description]
    )
