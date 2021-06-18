from bootstrap_modal_forms.generic import BSModalDeleteView, BSModalCreateView
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from .forms import CollectionTitleFormSet, CollectionForm, VacancyFilterForm, ResponseCreateForm
from .models import CV
from employer.models import Vacancy, BookmarkVacancy, Response
from django.db import transaction
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect



# ['title'] - Formset('title')


class HomepageView(TemplateView):
    template_name = "employee/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ['cv'] - relation name
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
#                           Vacancy Search views                         #
##########################################################################


class JobFilter(FormView):
    template_name = 'employee/filter.html'
    form_class = VacancyFilterForm

    def form_valid(self, form):
        if '' in self.request.POST:
            self.filter = ''
        else:
            self.filter = '?position=' + form.cleaned_data['position']

        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('employee:vacancies') + self.filter   # Add URL!!!



class SearchView(ListView):
    model = Vacancy
    context_object_name = 'jobs'
    template_name = "employee/search.html"

    def get_queryset(self):
        qs = super().get_queryset()
        if 'position' in self.request.GET:
            qs = qs.filter(position = self.request.GET['position'])
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


def add_remove_bookmark(request, pk):
    user = request.user

    try:
        bookmark = BookmarkVacancy.objects.get(employee=user, vacancy=pk)
        bookmark.delete()
        res=False
    except:
        bookmark = BookmarkVacancy.objects.create(
            employee=user,
            vacancy=Vacancy.objects.get(id=pk))
        bookmark.save()
        res=True

    data = {
        'res': res
    }

    return JsonResponse(data, safe=False)
    # return HttpResponseRedirect(reverse('employee:vacancies'))


class JobDetailView(DetailView):
    model = Vacancy
    template_name = 'employee/vacancy_detail.html'

    def get_context_data(self, **kwargs):
        context = super(JobDetailView, self).get_context_data(**kwargs)
        return context


##########################################################################
#                          Vacancy  Bookmark views                         #
##########################################################################

class BookmarkView(ListView):
    model = BookmarkVacancy
    context_object_name = 'bookmarks'
    template_name = "employee/bookmarks.html"
    def get_context_data(self, **kwargs):
        context = super(BookmarkView, self).get_context_data(**kwargs)
        context['title'] = 'Закладки'
        return context


    def get_queryset(self):

        qs = super().get_queryset()
        user = self.request.user
        qs = qs.filter(employee=user)
        return qs


def job_bookmarks(request):
    user = request.user
    data = dict()
    if request.method == 'GET':
        bookmarks = BookmarkVacancy.objects.all()
        data['table'] = render_to_string(
            'employee/includes/inc_bookmarks_table.html',
            {'bookmarks': bookmarks},
            request=request
        )
        return JsonResponse(data)



class BookmarkDeleteView(BSModalDeleteView):
    model = BookmarkVacancy
    template_name = 'employee/delete_bookmark.html'
    success_message = 'Success: Bookmark was deleted.'
    success_url = reverse_lazy('employee:bookmarks')


##########################################################################
#                          Response views                                #
##########################################################################

class ResponseView(ListView):
    model = Response
    context_object_name = 'responses'
    template_name = "employee/response.html"

    def get_queryset(self):

        qs = super().get_queryset()
        user = self.request.user
        # qs = qs.exclude(user=user)
        qs = qs.exclude(user=user).filter(cv__user = user)
        return qs

    def get_context_data(self,  *args, **kwargs):
        context = super(ResponseView, self).get_context_data(**kwargs)
        context['title'] = 'Отклики'
        return context


def responses(request):
    data = dict()
    if request.method == 'GET':
        responses = Response.objects.all()
        data['table'] = render_to_string(
            'employee/includes/inc_response_table.html',
            {'responses': responses},
            request=request
        )
        return JsonResponse(data)



class ResponseCreate(BSModalCreateView):
    model = Response
    template_name = 'employee/create_response.html'
    form_class = ResponseCreateForm
    # success_message = 'Отклик отпарвлен!'
    success_url = reverse_lazy('employee:bookmarks')


    def form_valid(self, form):
        form.instance = form.save(commit=False)
        form.instance.user = self.request.user
        form.instance.vacancy = Vacancy.objects.get(pk=self.kwargs['pk'])
        form.instance.save()
        return super(ResponseCreate, self).form_valid(form)


    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display vacancies that belong to a given user"""
        kwargs = super(ResponseCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class ResponseDelete(BSModalDeleteView):
    model = Response
    template_name = 'employee/delete_response.html'
    success_message = 'Success: Response was deleted.'
    success_url = reverse_lazy('employee:responses')