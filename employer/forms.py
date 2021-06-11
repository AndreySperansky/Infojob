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
        fields = ('__all__')



class ResponseCreateForm(BSModalModelForm):

    # def __init__(self,  *args, **kwargs):
    #     self.request = kwargs.pop('request')
    #     super(ResponseCreateForm, self).__init__(*args, **kwargs)
    #     self.fields['vacancy'].queryset = Vacancy.objects.filter(user=self.request.user)

    class Meta:
        model = Response
        fields = ('__all__')