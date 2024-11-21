from django.db import models

# TODO: Verify price precision meets requirements. max_digits and decimal_places were arbitrarily selected.
"""FIXME: A token is not uniquely identified by its name and symbol, it is uniquely identified by its contract address and chain.
To increase robustness, the model should be updated to include the contract address and chain as fields that are unique_together.
"""
# TODO: Add more constraints/warnings for suspected erroneous prices.


class CryptoCurrency(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=24, decimal_places=8)
    last_updated = models.DateTimeField()

    def __str__(self):
        return f"{self.name} ({self.symbol})"

    class Meta:
        unique_together = (
            (
                "name",
                "symbol",
            ),
        )
        constraints = [
            models.CheckConstraint(
                condition=models.Q(price__gte=0), name="price_gte_0"
            ),
        ]
