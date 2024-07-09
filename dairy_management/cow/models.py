from django.db import models
import uuid

# Create your models here.
class Cow(models.Model):
    cow_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, default='Unknown')
    breed = models.CharField(max_length=100)
    birth_date = models.DateField()
    status = models.CharField(max_length=50, default='available')
    eye_color = models.CharField(max_length=50, null=True, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    #cow_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    #cow_image = models.ImageField - use cloudinary for the images

    def __str__(self):
        return self.name
    
class VaccinationDoctor(models.Model):
    doctor_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor_name = models.CharField(max_length=100)
    doctor_nat_id = models.FloatField()
    doctor_email = models.EmailField(max_length=100)
    doctor_phone = models.IntegerField()
    treated_cow = models.ForeignKey(Cow, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.doctor_name

class Vaccination(models.Model):
    vaccination_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cow_vaccinated = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name='vaccinations')
    doctor = models.ForeignKey(VaccinationDoctor, on_delete=models.CASCADE, related_name='vaccinations')
    vaccination_type = models.CharField(max_length=100)
    vaccination_date = models.DateField()

    def __str__(self):
        return f"{self.vaccination_type} for {self.cow_vaccinated.name} by {self.doctor.doctor_name}"
