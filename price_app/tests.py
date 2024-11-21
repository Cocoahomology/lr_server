from django.test import TestCase
from unittest.mock import patch, MagicMock
from .services.defillama_request_service import defillama_request_service
from .tasks import update_cryptocurrency_prices
from . import config
from .models import CryptoCurrency
from django.core.exceptions import ValidationError
from datetime import datetime, timezone, timedelta

# TODO: Add more tests.


class DefillamaRequestServiceTests(TestCase):
    # TODO: Implement tests for caching and other edge cases.
    @patch("requests.get")
    def test_get_cryptocurrency_prices_from_defillama(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "coins": {"token1": {"symbol": "T1", "price": 100, "timestamp": 1638316800}}
        }
        mock_response.status_code = 200  # Ensure the status code is set to 200
        mock_requests_get.return_value = mock_response

        result = defillama_request_service.get_cryptocurrency_prices_from_defillama(
            config.TOKEN_ADDRESS_LIST, 0
        )
        self.assertIsNotNone(result)
        self.assertIn("coins", result)

    @patch("requests.get")
    def test_get_cryptocurrency_prices_from_defillama_error(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 500  # Simulate an internal server error
        mock_requests_get.return_value = mock_response

        result = defillama_request_service.get_cryptocurrency_prices_from_defillama(
            config.TOKEN_ADDRESS_LIST, 0
        )
        self.assertIsNone(result)


class UpdateCryptocurrencyPricesTests(TestCase):
    @patch("requests.get")
    def test_update_cryptocurrency_prices_success(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "coins": {
                "token1": {"symbol": "T1", "price": 100, "timestamp": 1638316800},
                "token2": {"symbol": "T2", "price": 200, "timestamp": 1638316800},
            }
        }
        mock_response.status_code = 200
        mock_requests_get.return_value = mock_response

        update_cryptocurrency_prices(use_token_name_mapping=False)

        self.assertTrue(CryptoCurrency.objects.filter(name="token1").exists())
        self.assertTrue(CryptoCurrency.objects.filter(name="token2").exists())

    @patch("requests.get")
    def test_update_cryptocurrency_prices_failure(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_requests_get.return_value = mock_response

        update_cryptocurrency_prices(use_token_name_mapping=False)

        self.assertFalse(CryptoCurrency.objects.filter(name="token1").exists())
        self.assertFalse(CryptoCurrency.objects.filter(name="token2").exists())


class CryptoCurrencyModelTests(TestCase):
    def test_price_gte_0_constraint(self):
        crypto = CryptoCurrency(
            name="Bitcoin",
            symbol="BTC",
            price=-1,
            last_updated=datetime.now(timezone.utc),
        )
        with self.assertRaises(ValidationError):
            crypto.full_clean()  # This will call all field validators

    def test_last_updated_validator(self):
        future_date = datetime.now(timezone.utc) + timedelta(days=1)
        crypto = CryptoCurrency(
            name="Bitcoin", symbol="BTC", price=50000, last_updated=future_date
        )
        with self.assertRaises(ValidationError):
            crypto.full_clean()  # This will call all field validators

    def test_unique_together_constraint(self):
        CryptoCurrency.objects.create(
            name="Bitcoin",
            symbol="BTC",
            price=50000,
            last_updated=datetime.now(timezone.utc),
        )
        duplicate_crypto = CryptoCurrency(
            name="Bitcoin",
            symbol="BTC",
            price=60000,
            last_updated=datetime.now(timezone.utc),
        )
        with self.assertRaises(ValidationError):
            duplicate_crypto.full_clean()  # This will call all field validators

    def test_valid_cryptocurrency(self):
        crypto = CryptoCurrency(
            name="Ethereum",
            symbol="ETH",
            price=3000,
            last_updated=datetime.now(timezone.utc),
        )
        try:
            crypto.full_clean()  # This will call all field validators
            crypto.save()
        except ValidationError:
            self.fail(
                "CryptoCurrency with valid data raised ValidationError unexpectedly!"
            )
