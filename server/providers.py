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
        # Gather provider data by getting all ads with tags
        cursor.execute(
            """
            SELECT Ads.id as ad_id, Ads.name, type.type, content_route, redirect_url, Ct.name as tag, Ct.id as tag_id FROM Ads
            JOIN `Space&Ad_type` type on type.id = Ads.type
            LEFT JOIN Ad_categories cats on cats.ad_id = Ads.id
            LEFT JOIN Category_tags Ct on cats.category_tag = Ct.id
            WHERE provider_id=?
            """,
            [self.p_id]
        )
        tags_with_ads = rows_to_dict(cursor, cursor.fetchall())
        if len(tags_with_ads) == 0:
            raise EntityNotFoundException(f"Could not find ad provider with id {self.p_id}")

        ret = {}
        for r in tags_with_ads:
            if ret.get(r['ad_id']) is None:
                ret[r['ad_id']] = r
                ret[r['ad_id']]['tag'] = [{'name': r['tag'], 'id': r['tag_id']}] if r['tag'] is not None else []
                ret[r['ad_id']].pop('tag_id')
            else:
                ret[r['ad_id']]['tag'].append({'name': r['tag'], 'id': r['tag_id']})

        return [r for r in ret.values()]

    def add_tags(self, ad_id, tags: list[dict[str, int]], cursor: Cursor):
        cursor.executemany(
            """
            INSERT INTO Ad_categories(ad_id, category_tag, relative_weight) 
            VALUES (?, ?, ?)
            """,
            [(ad_id, t['id'], t['relative_weight']) for t in tags]
        )

    def delete_tags(self, ad_id, tags: list[dict[str, int]], cursor: Cursor):
        cursor.executemany(
            """
            DELETE FROM Ad_categories
            where ad_id=? and category_tag=?
            """,
            [(ad_id, t['id']) for t in tags]
        )
