from decimal import Decimal


def convert_price_from_float_to_decimal(price: float):
    return Decimal(price).quantize(Decimal("1.00000000"))
