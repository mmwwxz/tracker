from django.db import models
from django.contrib.auth.models import User


class ProductionRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    date = models.DateField(auto_now_add=True)
    model = models.CharField(default='', max_length=30, null=True, blank=True)
    name = models.CharField(default='', max_length=30, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    received_by = models.IntegerField(default=0, null=True, blank=True)
    price = models.IntegerField(default=0, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default='')

    def save(self, *args, **kwargs):
        # Calculate 'total' before saving
        self.total = self.received_by * self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} - {self.model} - {self.name}"
