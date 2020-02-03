import django_filters
from django_filters import DateFilter, CharFilter
from django import forms

from printapp import forms
from .models import supplier, Order,Payment


class supplierFilter(django_filters.FilterSet):
    supplierName =django_filters.CharFilter(field_name="Name")
    class Meta:
        model = supplier
        fields = ['supplierName']


class orderFilter(django_filters.FilterSet):
    OrderName = django_filters.CharFilter(lookup_expr='icontains')
    start_date = DateFilter(field_name="Date", lookup_expr='gte')
    end_date = DateFilter(field_name="Date", lookup_expr='lte')
    # Amount = django_filters.NumberFilter(lookup_expr='contains')
    document =django_filters.CharFilter(field_name="document", lookup_expr='icontains')
    class Meta:
        model = Order
        fields = ['supplierName', 'OrderName', 'Date', 'Amount','document','start_date','end_date','Quantity']


# class MorderFilter(django_filters.FilterSet):
#     Mname = django_filters.CharFilter(lookup_expr='icontains')
#     start_date = DateFilter(field_name="Date", lookup_expr='gte')
#     end_date = DateFilter(field_name="Date", lookup_expr='lte')
#     # Amount = django_filters.NumberFilter(lookup_expr='contains')
#     document =django_filters.CharFilter(field_name="document", lookup_expr='icontains')
#     class Meta:
#         model = Order
#         fields = ['Msupplier', 'Mname', 'Date', 'start_date','end_date']



class paymentFilter(django_filters.FilterSet):
    Comment = django_filters.CharFilter(lookup_expr='icontains')
    start_date = DateFilter(field_name="Date", lookup_expr='gte')
    end_date = DateFilter(field_name="Date", lookup_expr='lte')

    class Meta:
        model = Payment
        fields = ['supplierName', 'paidIn', 'Date', 'Comment','credit','start_date','end_date',]

class BalanceFilter(django_filters.FilterSet):
    
    start_date1 = DateFilter(field_name="Date", lookup_expr='gte')
    end_date1 = DateFilter(field_name="Date", lookup_expr='lte')

    class Meta:
        model = Payment
        fields = ['supplierName', 'Date','start_date1','end_date1']
