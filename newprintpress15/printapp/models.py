from django.db import models
from datetime import datetime

class supplier(models.Model):
    Name = models.CharField(max_length=30)
    Company = models.CharField(max_length=30)
    Email = models.EmailField(max_length=254,blank=True,null=True)
    Mobile = models.IntegerField()
    Address = models.TextField(blank=True)


    def __str__(self):
        return self.Name

    # def __str__(self):
    #     return "%s %s" % (self.Name, self.Email)


class Order(models.Model):
    supplierName = models.ForeignKey(supplier, on_delete=models.CASCADE)
    OrderName = models.CharField(max_length=30)
    Date = models.DateField(default = datetime.now)
    document = models.FileField()
    Size = models.CharField(max_length=30)
    gsm = models.IntegerField()
    Quantity =models.IntegerField()
    Amount =models. IntegerField()
    Comment =models.TextField(blank=True)

    def __str__(self):
        return self.OrderName


Paid_CHOICES = [
    ('Cash', 'Cash'),
    ('cheque', 'Cheque'),
    ('Online', 'Online'),


]

class Payment(models.Model):
    supplierName = models.ForeignKey(supplier,on_delete=models.CASCADE)
    Date = models.DateField(default = datetime.now)
    paidIn = models.CharField(max_length=10,choices=Paid_CHOICES,default='Cash')
    credit = models.IntegerField(default=0)
    # Amount = models.IntegerField(default=0,blank=True)
    Comment = models.TextField(blank=True)


class Balance(models.Model):
    supplierName = models.ForeignKey(supplier,on_delete=models.CASCADE)
    # orderid = models.ForeignKey(Order,on_delete=models.CASCADE)
    # paymentid = models.ForeignKey(Payment,on_delete=models.CASCADE)
    Date = models.DateField(default = datetime.now)
    debit = models.IntegerField(default=0)
    credit = models.IntegerField(default=0)
    Amount = models.IntegerField(default=0,blank=True)

class attachments(models.Model):
    order =models.ForeignKey(Order,on_delete=models.CASCADE)
    files = models.FileField()

    # def __str__(self):
    #     return self.files

# Not yet used, testing purpose 
class Mails(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=1000)
    message = models.CharField(max_length=20000)
    document = models.FileField(upload_to='documents/')
    def __str__(self):
        return self.email
