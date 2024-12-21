import datetime
from unittest.mock import Mock, patch

import pytest

from app.main import outdated_products


FAKE_TODAY_DATE = datetime.date(2022, 2, 10)


@pytest.fixture(autouse=True)
def mock_datetime() -> Mock:
    with patch("app.main.datetime") as mock_datetime:
        mock_datetime.date.today = Mock(return_value=FAKE_TODAY_DATE)
        yield mock_datetime


def create_products(
        create_expired: bool = True,
        how_many: int = 1
) -> list[dict]:
    if create_expired:
        return [
            {
                "name": f"expired{i}",
                "expiration_date": (
                    FAKE_TODAY_DATE
                    - datetime.timedelta(days=i + 1)
                )
            }
            for i in range(how_many)]
    else:
        return [
            {
                "name": f"not_expired{i}",
                "expiration_date": (
                    FAKE_TODAY_DATE
                    + datetime.timedelta(days=i + 1)
                )
            }
            for i in range(how_many)
        ]


def test_should_return_empty_list_when_no_expired_products() -> None:

    assert (
        outdated_products(
            create_products(
                create_expired=False, how_many=4
            )
        ) == []
    ), "Should return empty list if all products are expired"


def test_should_return_all_names_when_all_products_expired() -> None:

    expired_products = create_products(create_expired=True, how_many=4)

    expired_products_names = [
        expired_product.get("name")
        for expired_product in expired_products
    ]

    result = outdated_products(expired_products)

    assert (
        len(result) == len(expired_products)
        and result == expired_products_names
    ), "Should return all products' names if all expired"


def test_should_return_expired_only_when_mixed_products() -> None:

    expired_products = create_products(create_expired=True, how_many=4)

    expired_products_names = [
        fake_product.get("name")
        for fake_product in expired_products
    ]

    mixed_products = (
        expired_products
        + create_products(create_expired=False, how_many=4)
    )

    result = outdated_products(mixed_products)

    assert (
        len(result) == len(expired_products)
        and result == expired_products_names
    ), "Should return only expired products' names"
