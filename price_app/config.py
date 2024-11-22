from celery.schedules import crontab

# TODO: Check that this file is in a sensible place (need to research best practices for configuration files in Django projects).

# List of token addresses to fetch data for from DefiLlama API.
TOKEN_ADDRESS_LIST = [
    "ethereum:0xd533a949740bb3306d119cc777fa900ba034cd52",
    "ethereum:0xf939e0a03fb07f59a73314e73794be0e57ac1b4e",
    "ethereum:0x0655977feb2f289a4ab78af67bab0d17aab84367",
    "solana:Df6yfrKC8kZE3KNkrHERKzAetSxbrWeniQfyJY4Jpump",
]

# Mapping for token chain/address to name, which determines 'name' field in CryptoCurrency model.
# Each token chain/address string in TOKEN_ADDRESS_LIST must have corresponding name in this dictionary.
TOKEN_NAME_MAPPING = {
    "ethereum:0xf939e0a03fb07f59a73314e73794be0e57ac1b4e": "crvUSD",
    "ethereum:0xd533a949740bb3306d119cc777fa900ba034cd52": "Curve DAO",
    "ethereum:0x0655977feb2f289a4ab78af67bab0d17aab84367": "Savings crvUSD",
    "solana:Df6yfrKC8kZE3KNkrHERKzAetSxbrWeniQfyJY4Jpump": "Chill Guy",
}

# Celery Beat schedule for updating cryptocurrency prices.
UPDATE_PRICES_CRON_SCHEDULE = crontab(minute="*")
