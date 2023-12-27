from django.forms import ModelForm
from django import forms
from .models import EmployeeData

class EmployeeForm(ModelForm):
    # birthdate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = EmployeeData
        fields = "__all__"