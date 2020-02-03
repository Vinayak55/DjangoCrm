from django import forms
from .models import MPayment,MOrder,Msupplier

class MorderForm(forms.ModelForm):
    class Meta:
        model = MOrder
        fields = '__all__'

class MsupplierForm(forms.ModelForm):
    class Meta:
        model = Msupplier
        fields = '__all__'


class MpaymentForm(forms.ModelForm):
    class Meta:
        model = MPayment
        fields = ['Msupplier','Date','paidBy','Amount','Comment']
