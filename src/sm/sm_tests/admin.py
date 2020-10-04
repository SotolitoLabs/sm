from django.contrib import admin
from .models import (MentalTest, MentalTestField, MentalTestFieldType,
                     MentalTestResult, Company, Employee)

admin.site.register(MentalTest)
admin.site.register(MentalTestField)
admin.site.register(MentalTestFieldType)
admin.site.register(MentalTestResult)
admin.site.register(Company)
admin.site.register(Employee)
