from django.contrib.auth.models import User
from django.db import models


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    date = models.DateField(auto_now_add=True)
    model_name = models.CharField(max_length=30, default='', null=True, blank=True)
    name_fabric = models.CharField(max_length=30, default='', null=True, blank=True)
    fabric = models.IntegerField(default=0, null=True, blank=True)
    accessories = models.IntegerField(default=0, null=True, blank=True)
    threads = models.IntegerField(default=0, null=True, blank=True)
    other = models.IntegerField(default=0, null=True, blank=True)
    sewing = models.IntegerField(default=0, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.total = sum(filter(None, [self.fabric, self.accessories, self.threads, self.other, self.sewing]))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} - {self.model_name} - {self.name_fabric} - {self.fabric} - {self.accessories} - {self.threads} - {self.other} - {self.sewing}"
