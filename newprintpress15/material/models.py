from datetime import datetime
from django.db import models

class Msupplier(models.Model):
    Name = models.CharField(max_length=30)
    Company = models.CharField(max_length=30)
    Mobile = models.CharField(max_length=12)
    Address = models.TextField(blank=True)

    def __str__(self):
        return self.Name

class MOrder(models.Model):
    supplierName = models.ForeignKey(Msupplier, on_delete=models.CASCADE)
    OrderName = models.CharField(max_length=30)
    Date = models.DateField(default = datetime.now)
    Size = models.CharField(max_length=30,blank=True)
    gsm = models.IntegerField(blank=True)
    Quantity =models.CharField(max_length=30)
    Amount =models. IntegerField()
    Comment =models.TextField(blank=True)

    def __str__(self):
        return self.Mname

Paid_CHOICES = [
    ('Cash', 'Cash'),
    ('cheque', 'Cheque'),
    ('Online', 'Online'),
]


class MPayment(models.Model):
    Msupplier = models.ForeignKey(Msupplier,on_delete=models.CASCADE)
    Date = models.DateField(default = datetime.now)
    paidBy = models.CharField(max_length=10,choices=Paid_CHOICES,default='Cash')
    Amount = models.IntegerField(default=0)
    # Amount = models.IntegerField(default=0,blank=True)
    Comment = models.TextField(blank=True)

