from django import forms
from .models import Sales

class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = ['milk_collection_id', 'customer_name', 'liter', 'price_per_ltr', 'date']
