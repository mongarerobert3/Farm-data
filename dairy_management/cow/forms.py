# cow/forms.py

from django.utils import timezone
from django import forms
from .models import Cow, Vaccination, VaccinationDoctor

class CowForm(forms.ModelForm):
    class Meta:
        model = Cow
        fields = [
            'name',
            'gender',
            'breed',
            'birth_date',
            'status',
            'eye_color',
            'purchase_date',
            #'cow_weight',
            #image
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
        }

class VaccinateForm(forms.ModelForm):
    class Meta:
        model = Vaccination
        fields = ['doctor', 'vaccination_type', 'vaccination_date']
        widgets = {
            'vaccination_date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super(VaccinateForm, self).__init__(*args, **kwargs)
        self.fields['doctor'].queryset = VaccinationDoctor.objects.all()
        self.fields['vaccination_type'].widget = forms.TextInput(attrs={'placeholder': 'Type of Vaccination'})

    def clean_vaccination_date(self):
        vaccination_date = self.cleaned_data.get('vaccination_date')
        if vaccination_date > timezone.now().date():
            raise forms.ValidationError("The vaccination date cannot be in the future.")
        return vaccination_date

    