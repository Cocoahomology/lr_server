# Description: Configuration file for which tokens to fetch data for from DefiLlama API.
# Also contains a mapping for token chain/address to name, which determines 'name' field in CryptoCurrency model.
# TODO: Ensure file is in sensible place (need to research best practices for configuration files in Django projects).

TOKEN_ADDRESS_LIST = [
    "bsc:0x762539b45a1dcce3d36d080f74d1aed37844b878",
    "ethereum:0xdB25f211AB05b1c97D595516F45794528a807ad8",
]

TOKEN_NAME_MAPPING = {
    "bsc:0x762539b45a1dcce3d36d080f74d1aed37844b878": "Linear",
    "ethereum:0xdB25f211AB05b1c97D595516F45794528a807ad8": "Stasis Euro",
}
