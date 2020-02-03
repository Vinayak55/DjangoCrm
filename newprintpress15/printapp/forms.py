from django import forms
from .models import supplier,Order,Payment,Mails,attachments

class supplierForm(forms.ModelForm):
    class Meta:
        model = supplier
        fields = '__all__'

        def clean(self):
            cleaned_data =super(self,supplierForm).clean()
            Name =cleaned_data.get('Name')
            Email =cleaned_data.get('Email')
            Mobile = cleaned_data.get('Mobile')
            Address = cleaned_data.get('Address')
            Company = cleaned_data.get('Company')
            if not Name and not Email and not Mobile and not Address and not Company :
             raise forms.ValidationError("error ")


class orderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class attachmentForm(forms.ModelForm):
    class Meta:
        model = attachments
        fields = '__all__'


class paymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['supplierName','Date','paidIn','credit','Comment']


class EmailForm(forms.ModelForm):
    email = forms.EmailField(max_length=200,widget=forms.TextInput(attrs={'class': "form-control",'id': "clientemail"}))
    message = forms.CharField( widget=forms.Textarea(attrs={'class': "form-control"}))
    subject = forms.CharField( widget=forms.TextInput(attrs={'class': "form-control"}))
    class Meta:
        model = Mails
        fields = ('email','subject','message','document',)
