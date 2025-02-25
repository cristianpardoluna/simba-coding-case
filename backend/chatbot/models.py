from django.db import models

class Computers(models.Model):
    brand = models.CharField(
        max_length=255
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.brand} x {self.price}"