from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm

from .models import InfojobUser


class InfojobUserLoginForm(AuthenticationForm):
    class Meta:
        model = InfojobUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(InfojobUserLoginForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'




class InfojobUserRegisterForm(UserCreationForm):
    class Meta:
        model = InfojobUser
        fields = ('username', 'first_name', 'email', 'avatar', 'password1',  'password2', 'user_role')



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['user_role'].empty_lable = 'Роль не выбрана'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    # блок проверки совпадения паролей
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']



class InfojobUserEditForm(UserChangeForm):
    class Meta:
        model = InfojobUser
        fields = ('username', 'first_name', 'avatar', 'email', 'user_role', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['user_role'].empty_lable = 'Роль не выбрана'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()


