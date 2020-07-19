from django.contrib import admin
from .models import (MentalTest, MentalTestField, MentalTestFieldType, 
    MentalTestResult)

admin.site.register(MentalTest)
admin.site.register(MentalTestField)
admin.site.register(MentalTestFieldType)
admin.site.register(MentalTestResult)
