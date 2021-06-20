from bootstrap_modal_forms.generic import BSModalDeleteView, BSModalCreateView, BSModalUpdateView, BSModalReadView
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, View, FormView
from django.views.generic.detail import DetailView
# from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
# from .forms import *
from .forms import CVFilterForm, VacancyCreateForm, ResponseCreateForm
from .models import *
from employee.models import *
# from django.db import transaction
# from django.http import HttpResponse



class HomepageView(TemplateView):
    template_name = "employer/employer.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = Company.objects.filter(user=self.request.user)
        context['vacancies'] = Vacancy.objects.order_by('id')
        return context

    def get_queryset(self):
        return Company.objects.filter(user=self.request.user)



#############################################################################################
#             Companies Views
#############################################################################################


class CompanyList(ListView):
    model = Company
    context_object_name = 'companies'

    def get_queryset(self):
        return Company.objects.filter(user=self.request.user)



class CompanyDetail(LoginRequiredMixin, DetailView):
    model = Company
    context_object_name = 'company'
    template_name = 'employer/company_detail.html'



class CompanyCreate(LoginRequiredMixin, CreateView):
    model = Company
    template_name = 'employer/company_create.html'
    fields = ['company_name', 'industry_name', 'logo_pic', 'email', 'site_link', 'is_active']
    success_url = None

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CompanyCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('employer:company_detail', kwargs={'pk': self.object.pk})


class CompanyUpdate(LoginRequiredMixin, UpdateView):
    model = Company
    template_name = 'employer/company_update.html'
    fields = ['company_name', 'industry_name', 'logo_pic', 'email', 'site_link', 'is_active']
    success_url = None

    def get_success_url(self):
        return reverse_lazy('employer:company_detail', kwargs={'pk': self.object.pk})


class CompanyDelete(LoginRequiredMixin, DeleteView):
    model = Company
    context_object_name = 'company'
    template_name = 'employer/confirm_delete.html'
    success_url = reverse_lazy('employer:employer')



#############################################################################################
#             Vacancies Views
#############################################################################################


class VacancyDetail(LoginRequiredMixin, DetailView):
    model = Vacancy
    context_object_name = 'vacancy'
    template_name = 'employer/vacancy_detail.html'



class VacancyCreate(LoginRequiredMixin, CreateView):
    model = Vacancy
    template_name = 'employer/vacancy_create.html'
    form_class = VacancyCreateForm
    success_url = None

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(VacancyCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('employer:vacancy_detail', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display companies that belong to a given user"""

        kwargs = super(VacancyCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class VacancyUpdate(LoginRequiredMixin, UpdateView):
    model = Vacancy
    template_name = 'employer/vacancy_update.html'
    fields = ['company', 'position', 'city', 'duties', 'compensation', 'is_active']
    success_url = None

    def get_success_url(self):
        return reverse_lazy('employer:vacancy_detail', kwargs={'pk': self.object.pk})


class VacancyDelete(LoginRequiredMixin, DeleteView):
    model = Vacancy
    context_object_name = 'vacancy'
    template_name = 'employer/confirm_delete.html'
    success_url = reverse_lazy('employer:employer')


#############################################################################################
#             Add Favorite CV Views
#############################################################################################

class CvFilterView(FormView):
    template_name = 'employer/filter.html'
    form_class = CVFilterForm

    def form_valid(self, form):
        if '' in self.request.POST:
            self.filter = ''
        else:
            self.filter = '?position_seek=' + form.cleaned_data['position_seek']

        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('employer:cvs') + self.filter   # Add URL!!!



class SearchView(ListView):
    model = CV
    context_object_name = 'cvs'
    template_name = "employer/search.html"

    def get_queryset(self):
        qs = super().get_queryset()
        if 'position_seek' in self.request.GET:
            qs = qs.filter(position_seek=int(self.request.GET['position_seek']))
        return qs


def cvs(request):
    data = dict()
    if request.method == 'GET':
        cvs = CV.objects.all()
        data['table'] = render_to_string(
            'employer/includes/inc_cv_table.html',
            {'cvs': cvs},
            request=request
        )
        return JsonResponse(data)


def add_remove_bookmark(request, pk):
    user = request.user

    try:
        bookmark = BookmarkCV.objects.get(employer=user, cv=pk)
        bookmark.delete()
        res=False
    except:
        bookmark = BookmarkCV.objects.create(
            employer=user,
            cv=CV.objects.get(id=pk))
        bookmark.save()
        res=True

    data = {
        'res': res
    }

    return JsonResponse(data, safe=False)
    # return HttpResponseRedirect(reverse('employer:cvs'))



class CvDetailView(DetailView):
    model = CV
    template_name = 'employer/cv_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CvDetailView, self).get_context_data(**kwargs)
        return context


##########################################################################
#                          Vacancy  Bookmark views                         #
##########################################################################

class BookmarkView(ListView):
    model = BookmarkCV
    context_object_name = 'bookmarks'
    template_name = "employer/bookmarks.html"


    def get_queryset(self):
        qs = super().get_queryset()
        if 'type' in self.request.GET:
            qs = qs.filter(bookmark_type=int(self.request.GET['type']))
        return qs


def cv_bookmarks(request):
    user = request.user
    data = dict()
    if request.method == 'GET':
        bookmarks = BookmarkCV.objects.filter(employer=user)
        data['table'] = render_to_string(
            'employer/includes/inc_bookmarks_table.html',
            {'bookmarks': bookmarks},
            request=request,
        )
        return JsonResponse(data)


class BookmarkDeleteView(BSModalDeleteView):
    model = BookmarkCV
    template_name = 'employer/delete_bookmark.html'
    success_message = 'Success: Bookmark was deleted.'
    success_url = reverse_lazy('employer:bookmarks')



##########################################################################
#                          Response views                                #
##########################################################################

class ResponseView(ListView):
    model = Response
    context_object_name = 'responses'
    template_name = "employer/response.html"
    def get_context_data(self,  **kwargs):
        context = super(ResponseView, self).get_context_data(**kwargs)
        context['title'] = 'Отклики'
        return context


def responses(request):
    user = request.user
    data = dict()
    if request.method == 'GET':
        responses = Response.objects.filter(vacancy_id=1)
#         # responses = Response.objects.all()
        data['table'] = render_to_string(
            'employer/includes/inc_response_table.html',
            {'responses': responses},
            request=request
        )
        return JsonResponse(data)




class ResponseCreate(BSModalCreateView):
    model = Response
    template_name = 'employer/create_response.html'
    form_class = ResponseCreateForm
    # success_message = 'Отклик отпарвлен!'
    # success_url = reverse_lazy('employer:bookmarks')
    success_url = reverse_lazy('employer:bookmarks')


    def form_valid(self, form):
        form.instance = form.save(commit=False)
        form.instance.user = self.request.user
        form.instance.cv = CV.objects.get(pk=self.kwargs['pk'])
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
    template_name = 'employer/delete_response.html'
    success_message = 'Success: Response was deleted.'
    success_url = reverse_lazy('employer:responses')


#
# class BookReadView(BSModalReadView):
#     model = Book
#     template_name = 'employer/read_book.html'


# def add_remove_response(request, pk1, pk2):
#     # user = request.user
#
#     try:
#         response = Response.objects.get(cv=pk1, vacancy=pk2)
#         response.delete()
#         res=False
#     except:
#         response = Response.objects.create(
#             cv = CV.objects.get(pk=pk1),
#             vacancy = Vacancy.objects.get(pk=pk2))
#         response.save()
#         res=True
#
#     data = {
#         'res': res
#     }
#
#     return JsonResponse(data, safe=False)
#

    # return HttpResponseRedirect(reverse('employee:vacancies'))
    # в шаблон { % url 'employer:response' pk1 = cv.pk pk2 = vacancy.pk %}



