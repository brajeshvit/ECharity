from django import forms
from django.contrib.auth.models import User
from products.models import Product
from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget 


class PostForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('title', 'description', 'active', 'quantity','address', 'zip_Code', 'expire_date', )



class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select image (Image can not be update in future)',
    )
    title = forms.CharField(
        label='title',
    )
    
    description = forms.CharField(
        label='description',
    )   
   
    active = forms.BooleanField(
        label='active',
    )
    quantity = forms.IntegerField(
        label='quantity',
    )
    zip_Code = forms.CharField(
        label='zip_Code',
    )
    address = forms.CharField(
        label='address',
    )
    expire_date = forms.DateTimeField(widget=DateTimeWidget(usel10n=True, bootstrap_version=3))
    
    
    
