from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from .forms import CollectionTitleFormSet, CollectionForm, VacancyFilterForm
from .models import CV, JobExp
from employer.models import Vacancy
from django.db import transaction
from django.http import HttpResponse, JsonResponse


# ['collections'] - relation name
# ['title'] - Formset('title')


class HomepageView(TemplateView):
    template_name = "employee/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # [relation_name]
        context['cv'] = CV.objects.order_by('id')
        return context


##########################################################################
#                           Resumes views                             #
##########################################################################

class CollectionDetailView(DetailView):
    model = CV
    template_name = 'employee/cv_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CollectionDetailView, self).get_context_data(**kwargs)
        return context


class CollectionCreate(CreateView):
    model = CV
    template_name = 'employee/cv_create.html'
    form_class = CollectionForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(CollectionCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['title'] = CollectionTitleFormSet(self.request.POST)
        else:
            data['title'] = CollectionTitleFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        # print(f'context {context}')
        titles = context['title']
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if titles.is_valid():
                titles.instance = self.object
                titles.save()
        return super(CollectionCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('employee:cv_detail', kwargs={'pk': self.object.pk})


    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super(CollectionCreate, self).dispatch(*args, **kwargs)


class CollectionUpdate(UpdateView):
    model = CV
    form_class = CollectionForm
    template_name = 'employee/cv_create.html'

    def get_context_data(self, **kwargs):
        data = super(CollectionUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['title'] = CollectionTitleFormSet(self.request.POST, instance=self.object)
        else:
            data['title'] = CollectionTitleFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        titles = context['title']
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if titles.is_valid():
                titles.instance = self.object
                titles.save()
        return super(CollectionUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('employee:cv_detail', kwargs={'pk': self.object.pk})



class CollectionDelete(DeleteView):
    model = CV
    template_name = 'employee/confirm_delete.html'
    success_url = reverse_lazy('employee:employee')


##########################################################################
#                           Vacancy Search views                             #
##########################################################################


class JobFilterView(FormView):
    template_name = 'employer/includes/inc_filter_cv.html'
    form_class = VacancyFilterForm

    def form_valid(self, form):
        if '' in self.request.POST:
            self.filter = ''
        else:
            self.filter = '?position_seek=' + form.cleaned_data['position_seek']

        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('employer:employer') + self.filter   # Add URL!!!



class SearchView(ListView):
    model = Vacancy
    context_object_name = 'jobs'
    template_name = "employee/search.html"

    def get_queryset(self):
        qs = super().get_queryset()
        if 'type' in self.request.GET:
            qs = qs.filter(cv_type=int(self.request.GET['type']))
        return qs


def vacancies(request):
    data = dict()
    if request.method == 'GET':
        jobs = Vacancy.objects.all()
        data['table'] = render_to_string(
            'employee/includes/inc_vacancy_table.html',
            {'jobs': jobs},
            request=request
        )
        return JsonResponse(data)


class JobBookmarkView(View):
    pass

class JobResponseView(View):
    pass

class JobReadView(View):
    pass