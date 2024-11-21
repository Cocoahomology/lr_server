import requests
import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)


def get_cryptocurrency_prices_from_defillama(
    TOKEN_ADDRESS_LIST: list, cache_time: int = 10
):
    """Fetches current cryptocurrency prices for all tokens specified in TOKEN_ADDRESS_LIST.
    Each unique response is cached for cache_time seconds."""
    token_addresses_string = ",".join(TOKEN_ADDRESS_LIST)
    cache_key = f"defillama_prices_{token_addresses_string}"
    cached_response = cache.get(cache_key)

    if cached_response:
        logging.info(
            "returning cached reponse for get_cryptocurrency_prices_from_defillama"
        )
        return cached_response

    try:
        url = f"https://coins.llama.fi/prices/current/{token_addresses_string}"
        response = requests.get(url)
        if response.status_code != 200:
            raise requests.exceptions.RequestException(
                f"Unexpected response code: {response.status_code}"
            )
        data = response.json()
        cache.set(cache_key, data, timeout=cache_time)
        return data
    except (requests.exceptions.RequestException, ValueError) as e:
        logger.error(
            f"Failed to retrieve cryptocurrency prices from DefiLlama 'coins' endpoint: {e}"
        )
        return None
