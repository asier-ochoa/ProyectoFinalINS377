from mariadb import Cursor
from tools import rows_to_dict, DuplicatedEntityException


class SpaceProvider:
    def __init__(self, company_name, email, iban):
        self.company_name: str = company_name
        self.email: str = email
        self.iban: str = iban

    def submit(self, cursor: Cursor):
        cursor.execute("""
        INSERT INTO Space_provider(company_name, contact_email, payment_account_iban)
        VALUES(?, ?, ?)
        """,
                       [self.company_name, self.email, self.iban])


class AdProvider:
    def __init__(self, company_name, email):
        self.company_name: str = company_name
        self.email: str = email

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
        cursor.execute("""
        INSERT INTO Ad_provider(company_name, contact_email)
        VALUES (?, ?)
        """,
                       [self.company_name, self.email])

    def create_ad(self, cursor: Cursor):
        pass
