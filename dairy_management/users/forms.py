# users/forms.py
from django import forms
from users.models import User
from cow.models import VaccinationDoctor  

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['name', 'username', 'phone', 'natid', 'password']  #profile_image
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_email(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This email is already taken")
        return username
    
    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class DoctorForm(forms.ModelForm):
    class Meta:
        model = VaccinationDoctor
        fields = ['doctor_name', 'doctor_nat_id', 'doctor_email', 'doctor_phone']

    def clean_doctor_email(self):
        doctor_email = self.cleaned_data.get('doctor_email')
        if VaccinationDoctor.objects.filter(doctor_email=doctor_email).exists():
            raise forms.ValidationError("This phone number is already taken")
        return doctor_email
    
    def clean_doctor_phone(self):
        doctor_phone = self.cleaned_data.get('doctor_phone')
        if VaccinationDoctor.objects.filter(doctor_phone=doctor_phone).exists():
            raise forms.ValidationError("This phone number is already taken")
        return doctor_phone