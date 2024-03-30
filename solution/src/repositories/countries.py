from src.db.models.countries import Country
from src.repositories.repository import SQLAlchemyRepository


class CountriesRepository(SQLAlchemyRepository):
    model = Country
