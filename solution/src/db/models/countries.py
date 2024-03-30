from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column

from src.db.db import Base
from src.schemas.countries import CountrySchema


class Regions(Enum):
    Europe = "Europe"
    Afirca = "Africa"
    Oceania = "Ocenia"
    Asia = "Asia"


class Country(Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    alpha2: Mapped[str] = mapped_column(unique=True)
    alpha3: Mapped[str] = mapped_column()
    region: Mapped[str] = mapped_column()

    def to_read_model(self) -> CountrySchema:
        return CountrySchema(
                name=self.name,
                alpha2=self.alpha2,
                alpha3=self.alpha3,
                region=self.region
        )
