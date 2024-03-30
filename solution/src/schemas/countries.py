from enum import Enum

from pydantic import BaseModel, Field


class CountrySchema(BaseModel):
    name: str = Field(
            max_length=100,
            description="Полное название страны"
    )
    alpha2: str = Field(
            max_length=2,
            pattern=r"[a-zA-Z]{2}",
            examples=["RU",],
            description="Двухбуквенный код, уникально идентифицирующий страну"
    )
    alpha3: str = Field(
            max_length=3,
            pattern=r"[a-zA-Z]{3}",
            description="Трехбуквенный код страны"
    )
    region: str = Field(
            description="Географический регион, к которому относится страна",
            examples=["Europe", "Africa", "Americas",
                      "Oceania", "Asia", "Americas"]
    )

    class Config:
        from_attributes = True


class Countries(Enum):
    europe = "Europe"
    afirca = "Africa"
    oceania = "Ocenia"
    asia = "Asia"
    americas = "Americas"
    all_ = None
