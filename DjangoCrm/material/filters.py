import django_filters
from django_filters import DateFilter, CharFilter
from django import forms
#
# from printapp import forms
from .models import Msupplier, MOrder
#
#
# # class supplierFilter(django_filters.FilterSet):
# #     MsupplierName =django_filters.CharFilter(field_name="Name")
# #     class Meta:
# #         model = Msupplier
# #         fields = ['MsupplierName']
# #
#
class orderFilter(django_filters.FilterSet):
    OrderName = django_filters.CharFilter(lookup_expr='icontains')
    start_date = DateFilter(field_name="Date", lookup_expr='gte')
    end_date = DateFilter(field_name="Date", lookup_expr='lte')
    # Amount = django_filters.NumberFilter(lookup_expr='contains')
    document =django_filters.CharFilter(field_name="document", lookup_expr='icontains')
    class Meta:
        model = MOrder
        fields = ['supplierName', 'OrderName', 'Date', 'Amount','start_date','end_date','Quantity']
