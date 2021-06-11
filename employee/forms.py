from django import forms

from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, Row, HTML, ButtonHolder, Submit, Column
from .custom_layout_object import Formset
from django import forms
from .models import CV, JobExp
from employer.models import Vacancy

import re


class CollectionTitleForm(forms.ModelForm):

    class Meta:
        model = JobExp
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        print(kwargs.get('prefix', ''))
        # has_titles - 0


        formtag_prefix = re.sub('-[0-9]+$', '', kwargs.get('prefix', ''))
        # отбрасываем цифровую часть у префикса вместе с "-"  было  has_titles-1   стало has_titles
        print(formtag_prefix)
        # has_titles


        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Row(
                Div(
                    Row(
                        Column('employer', css_class='form-group col-md-6 mb-0'),
                        Column('position', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('start_at', css_class='form-group col-md-6 mb-0'),
                        Column('finish_at', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    )
                ), css_class='formset_row-{}'.format(formtag_prefix)
            )
        )


CollectionTitleFormSet = inlineformset_factory(
    CV, JobExp, form=CollectionTitleForm,
    fields=['employer', 'position', 'start_at', 'finish_at'], extra=1, can_delete=True
)


class CollectionForm(forms.ModelForm):

    class Meta:
        model = CV
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(CollectionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.disable_csrf = False
        self.helper.form_class = 'form-horizontal '
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Field('user_pic'),
                Field('position_seek'),
                Field('compensation_seek'),
                Field('first_name'),
                Field('middle_name'),
                Field('family_name'),
                Field('gender'),
                Field('birthday'),
                Field('email'),
                Field('city'),
                Field('profession'),
                Fieldset('Add Job Experience',
                         Formset('title')),  # Formset берется из custom_layout_object.py
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'Save')),
            )
        )


class VacancyFilterForm(forms.ModelForm):

    class Meta:
        model = Vacancy
        fields = ['position', 'compensation']


