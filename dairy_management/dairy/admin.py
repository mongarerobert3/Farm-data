from django.contrib import admin

# Register your models here.
from .models import ProductionRecord, ProductionRecordHistory, FeedingRecord

admin.site.register(ProductionRecord)
admin.site.register(ProductionRecordHistory)
admin.site.register(FeedingRecord)
