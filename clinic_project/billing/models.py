from django.db import models

class Discount(models.Model):
    category = models.CharField("Категория льгот", max_length=50, unique=True)
    percentage = models.DecimalField("Процент скидки", max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.category} ({self.percentage}%)"
    
