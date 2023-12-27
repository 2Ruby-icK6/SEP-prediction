from django.contrib import admin
from predictionUI.models import EmployeeData

class EmployeeDataAdmin(admin.ModelAdmin):
    list_display = ("id","name", "age", "gender", "civil_status", "relative_size", "work_experiences", "monthly_salary")

# Register your models here.
admin.site.register(EmployeeData, EmployeeDataAdmin)

