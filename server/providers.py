from mariadb import Cursor
from tools import rows_to_dict, DuplicatedEntityException, EntityNotFoundException
import tools


# Gather list of available content types
def get_content_types(cursor: Cursor) -> list[dict]:
    cursor.execute(
        """
        SELECT id, type as content_type FROM `Space&Ad_type`
        """
    )
    return rows_to_dict(cursor, cursor.fetchall())


def search_tags(query: str, cursor: Cursor) -> list[dict]:
    query = f"%{query.replace('%', '').replace('_', '')}%"
    cursor.execute(
        """
        SELECT * FROM Category_tags
        WHERE name LIKE ?
        ORDER BY name
        LIMIT 10
        """,
        [query]
    )
    return rows_to_dict(cursor, cursor.fetchall())


class SpaceProvider:
    def __init__(self, company_name, email, iban):
        self.company_name: str = company_name
        self.email: str = email
        self.iban: str = iban

    def submit(self, cursor: Cursor):
        cursor.execute(
            """
            INSERT INTO Space_provider(company_name, contact_email, payment_account_iban, payment_interval)
            VALUES(?, ?, ?, 14)
            """,
            [self.company_name, self.email, self.iban]
        )


class AdProvider:
    def __init__(self, company_name, email, p_id=None):
        self.company_name: str = company_name
        self.email: str = email
        self.p_id: int | None = p_id

    @staticmethod
    def provider_factory_id(p_id: int, cursor: Cursor):
        cursor.execute(
            """
            SELECT id as p_id, company_name, contact_email as email FROM Ad_provider where id=?
            """,
            [p_id]
        )
        ad_provider = rows_to_dict(cursor, cursor.fetchone())
        if ad_provider is None:
            raise EntityNotFoundException(f"Could not find ad provider with id {p_id}")

        return AdProvider(**ad_provider)

    def get_provider(self, cursor: Cursor):
        cursor.execute(
            """
            SELECT * FROM Ad_provider where company_name=?
            """,
            [self.company_name]
        )
        return rows_to_dict(cursor, cursor.fetchone())

    def submit(self, cursor: Cursor):
        existing_provider = self.get_provider(cursor)
        if existing_provider is not None:
            raise DuplicatedEntityException(f"Company {existing_provider['company_name']} already exists!")
        cursor.execute(
            """
            INSERT INTO Ad_provider(company_name, contact_email)
            VALUES (?, ?)
            """,
            [self.company_name, self.email]
        )

    def create_ad(self, name: str, provider_id: int, ad_type: int, content_route: str, redirect_url: str, cursor: Cursor):
        # Check if provider has ad with same name
        cursor.execute(
            """
            SELECT id FROM Ads where name=? and provider_id=?
            """,
            [name, provider_id]
        )
        existing_ad = rows_to_dict(cursor, cursor.fetchone())
        if existing_ad is not None:
            raise DuplicatedEntityException(f"Provider {self.company_name} already has ad called {name}")

        # Insert new ad
        cursor.execute(
            """
            INSERT INTO Ads(name, provider_id, type, content_route, redirect_url)
            VALUES(?, ?, ?, ?, ?)
            """,
            [name, provider_id, ad_type, content_route, redirect_url]
        )

    def list_ads(self, cursor: Cursor):
        cursor.execute(
            """
            SELECT * FROM Ads where provider_id=?
            """
        )
