from django.db import models

# Create your models here.
class BaseModel (models.Model) :
    created_at = models.DateField(auto_now_add = True, db_index = True)
    updated_at = models.DateField(auto_now = True, db_index = True)

    class Meta:
        abstract = True
        
# Employee Data Here.
class EmployeeData(BaseModel) :
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 100, null = True, blank = True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length = 100, null=True, blank=True)
    civil_status = models.CharField(max_length = 100, null=True, blank=True)
    relative_size = models.IntegerField(null=True, blank=True)
    work_experiences = models.IntegerField(null=True, blank=True)
    monthly_salary = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.name