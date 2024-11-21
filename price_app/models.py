from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime


# TODO: Verify price precision meets requirements. max_digits and decimal_places were arbitrarily selected.
# FIXME: A token is not uniquely identified by its name and symbol, it is uniquely identified by its contract address and chain.
# To increase robustness, the model should be updated to include the contract address and chain as fields that are unique_together.
# TODO: Add more constraints/warnings for suspected erroneous prices.
# TODO: Add more validation for ALL fields in model.


def validate_past_date(value):
    if value.tzinfo is None:
        value = value.replace(tzinfo=datetime.timezone.utc)
    if value > timezone.now():
        raise ValidationError("The date cannot be in the future.")


class CryptoCurrency(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=24, decimal_places=8)
    last_updated = models.DateTimeField(validators=[validate_past_date])

    def save(self, *args, **kwargs):
        self.full_clean()  # This will call all field validators
        super().save(*args, **kwargs)

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
