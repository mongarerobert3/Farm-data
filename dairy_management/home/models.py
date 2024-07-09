from django.db import models

from dairy.models import ProductionRecord

# Create your models here.
class Sales(models.Model):
		milk_collection_id = models.ForeignKey(ProductionRecord, on_delete=models.CASCADE, related_name='sales_as_milk_collection')
		customer_name = models.CharField(max_length=100)
		liter = models.DecimalField(max_digits=10, decimal_places=2)
		price_per_ltr = models.DecimalField(max_digits=10, decimal_places=2)
		total = models.DecimalField(max_digits=15, decimal_places=2)
		date = models.DateField()

		def save(self, *args, **kwargs):
				#Calculate total based on liter and price per liter
				if self.liter > self.milk_collection_id.milk_produced:
					return ValueError('Check milk produced Entry')
				else:
					self.total = self.liter * self.price_per_ltr
				super(Sales, self).save(*args, **kwargs)
																				
		def __str__(self):
				return self.customer_name
		