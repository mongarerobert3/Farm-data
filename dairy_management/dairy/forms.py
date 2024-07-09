# dairy/forms.py
from django import forms
from cow.models import Cow  

from .models import FeedingRecord, ProductionRecord

class ProductionRecordForm(forms.ModelForm):
    cow = forms.ModelChoiceField(queryset=Cow.objects.all(), empty_label="Select a Cow")

    class Meta:
        model = ProductionRecord
        fields = ['cow', 'date', 'milk_produced']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

class FeedingRecordForm(forms.ModelForm):
    cow = forms.ModelChoiceField(queryset=Cow.objects.all(), empty_label="Select a Cow")

    def __init__(self, *args, cow_instance=None, **kwargs):
        super().__init__(*args, **kwargs)
        if cow_instance:
            self.fields['cow'].queryset = Cow.objects.filter(cow_id=cow_instance.cow_id)
        else:
            self.fields['cow'].queryset = Cow.objects.all()

    class Meta:
        model = FeedingRecord
        fields = ['feed_date', 'feed_type', 'quantity', 'cow', 'feed_time', 'supplements']
        widgets = {
            'feed_date': forms.DateInput(attrs={'type': 'date'}),
            'feed_time': forms.TimeInput(attrs={'type': 'datetime-local'}),
        }
