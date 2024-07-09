from django.db import models
from django.utils import timezone
import uuid
from users.models import User
from cow.models import Cow


# Existing models for reference

class ProductionRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    milk_produced = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE)

    def clean_milk_produced(self):
        milk_produced = self.cleaned_data.get('milk_produced')
        if (milk_produced <= 0):
            raise ValueError("Milk produced must be a positive number.")
        return milk_produced

    def delete(self, *args, **kwargs):
        # Create history entry before deletion
        ProductionRecordHistory.objects.create(
            production_record=self,
            user=self.user,
            cow=self.cow,
            date=self.date,
            milk_produced=self.milk_produced,
            action='Deleted',
            timestamp=timezone.now()
        )
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.cow.name} - {self.date} - {self.milk_produced}"

class FeedingRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    feed_date = models.DateField()
    feed_type = models.CharField(max_length=100)
    quantity = models.FloatField()
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, default=None)
    feed_time = models.TimeField(default=timezone.now)
    supplements = models.CharField(max_length=100, default=None)

    def __str__(self):
        return f"Feeding Record for {self.cow.name} on {self.feed_date} at {self.feed_time}"

class ProductionRecordHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    production_record = models.ForeignKey(ProductionRecord, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
    date = models.DateField()
    milk_produced = models.FloatField()
    action = models.CharField(max_length=100, default='Updated') 
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.production_record.cow.name} - {self.timestamp}"
