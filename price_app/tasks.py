from .models import CryptoCurrency
from celery import shared_task
from .services.defillama_request_service import defillama_request_service
from . import config
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def update_cryptocurrency_prices(self):
    # TODO: Add retry logic for failed requests
    # TODO: Consider better error handling
    # TODO: Ensure the insertion is being done atomically (need to double-check Django ORM behavior)
    # TODO: Consider moving this logic to separate module.
    try:
        response_json = (
            defillama_request_service.get_cryptocurrency_prices_from_defillama(
                config.TOKEN_ADDRESS_LIST, 5
            )
        )
        token_data_dict = response_json.get("coins")
        if not token_data_dict:
            logger.error("No token data found in the response.")
            return
    except Exception as e:
        logger.error(f"Error fetching cryptocurrency prices: {e}")
        return

    for token, token_data in token_data_dict.items():
        try:
            token_name = config.TOKEN_NAME_MAPPING.get(token)
            token_symbol = token_data["symbol"]
            token_price = token_data["price"]
            token_last_updated = datetime.fromtimestamp(
                timestamp=int(token_data["timestamp"]),
                tz=timezone.utc,
            )
        except KeyError as e:
            logger.error(f"Missing expected key in token data: {e}")
            continue

        try:
            CryptoCurrency.objects.update_or_create(
                name=token_name,
                symbol=token_symbol,
                defaults={
                    "price": token_price,
                    "last_updated": token_last_updated,
                },
            )
        except Exception as e:
            logger.error(
                f"Error updating or creating CryptoCurrency object for token {token_name}: {e}"
            )

    return
