from django.contrib import admin
from printapp.models import supplier, Order ,Payment,Mails,Balance,attachments
from material.models import MOrder,Msupplier,MPayment


class supplierName(admin.ModelAdmin):
    list_display = ('id', 'Name', 'Company', 'Mobile', 'Email', 'Address')


class OrderName(admin.ModelAdmin):
    list_display = ('id', 'supplierName', 'OrderName', 'Date', 'document', 'Size', 'Quantity', 'Amount', 'Comment')

class PaymentName(admin.ModelAdmin):
    list_display = ('id', 'supplierName', 'Date', 'credit',  'Comment')

class BalanceName(admin.ModelAdmin):
    list_display = ('id', 'supplierName', 'Date','debit', 'credit',  'Amount')

class attachmentName(admin.ModelAdmin):
    list_display = ('id','order','files')

admin.site.register(supplier, supplierName)
admin.site.register(Order, OrderName)
admin.site.register(Payment, PaymentName)
admin.site.register(Mails)
admin.site.register(Balance,BalanceName)
admin.site.register(attachments,attachmentName)

admin.site.register(Msupplier)
admin.site.register(MOrder)
admin.site.register(MPayment)
