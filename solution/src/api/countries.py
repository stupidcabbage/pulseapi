from typing import Annotated

from fastapi import APIRouter, Path, Query

from src.api.dependencies import UOWDep
from src.repositories.excpetions import CountryDoesNotExists
from src.schemas.countries import Countries, CountrySchema
from src.services.countries import CountriesService

router = APIRouter(prefix="/countries",
                   tags=["countries"])


@router.get("", summary="Получить список стран")
async def get_countries(uow: UOWDep,
                        region: Annotated[list[Countries], Query()] = [Countries.all_]
) -> list[CountrySchema]:
    """
    Получение списка стран с возможной фильтрацией.\n
    Используется на странице регистрации для предоставления
    возможности выбора страны, к которой относится пользователь.\n
    Если никакие из фильтров не переданы, необходимо вернуть все страны.
    """
    match region:
        case [Countries.all_]:
            countries = await CountriesService().get_countries(uow)
        case _:
            countries = await CountriesService().get_countries_by(
                    uow, {"region": [i.value for i in region]})
    return countries


@router.get("/{alpha2}", summary="Получить страну по alpha2 коду")
async def get_country_by_alpha2(
        uow: UOWDep,
        alpha2: Annotated[str,
                          Path(example="RU")]
) -> CountrySchema:
    """
    Получение одной страны по её уникальному двухбуквенному коду.\n
    Используется для получения информации по определенной стране
    """
    country = await CountriesService().get_country_by(uow, {"alpha2": alpha2})
    if not country:
        raise CountryDoesNotExists
    return country
