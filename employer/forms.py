from bootstrap_modal_forms.forms import BSModalModelForm
from django import forms
from employee.models import CV
from employer.models import Company, Vacancy, Response

class CVFilterForm(forms.ModelForm):

    class Meta:
        model = CV
        fields = ['position_seek']


class VacancyCreateForm(forms.ModelForm):

    def __init__(self,  *args, **kwargs):
        self.request = kwargs.pop('request')
        super(VacancyCreateForm, self).__init__(*args, **kwargs)
        self.fields['company'].queryset = Company.objects.filter(user=self.request.user)

    class Meta:
        model = Vacancy
        exclude = ('user', 'is_active', 'is_checked', 'employee_bookmarked')
        # fields = ('__all__')




class ResponseCreateForm(forms.ModelForm):

    def __init__(self,  *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ResponseCreateForm, self).__init__(*args, **kwargs)
        self.fields['vacancy'].queryset = Vacancy.objects.filter(user=self.request.user)

    class Meta:
        model = Response
        exclude = ('user',)
        # fields = ('__all__')