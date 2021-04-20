from django import forms
from employee.models import CV

class CVFilterForm(forms.ModelForm):

    class Meta:
        model = CV
        fields = ['position_seek']