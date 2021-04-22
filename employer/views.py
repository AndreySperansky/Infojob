from bootstrap_modal_forms.generic import BSModalDeleteView
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
from .forms import CVFilterForm
from .models import *
from employee.models import *
# from django.db import transaction
# from django.http import HttpResponse



class HomepageView(TemplateView):
    template_name = "employer/employer.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = Company.objects.order_by('id')
        context['vacancy'] = Vacancy.objects.order_by('id')
        return context



#############################################################################################
#             Companies Views
#############################################################################################


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
#             Companies Views
#############################################################################################


class VacancyDetail(LoginRequiredMixin, DetailView):
    model = Vacancy
    context_object_name = 'vacancy'
    template_name = 'employer/vacancy_detail.html'



class VacancyCreate(LoginRequiredMixin, CreateView):
    model = Vacancy
    template_name = 'employer/vacancy_create.html'
    fields = ['company', 'position', 'city', 'duties', 'compensation', 'is_active']
    success_url = None

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(VacancyCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('employer:vacancy_detail', kwargs={'pk': self.object.pk})


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
    template_name = 'employer/includes/inc_filter_cv.html'
    form_class = CVFilterForm

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
    model = CV
    context_object_name = 'cvs'
    template_name = "employer/search.html"

    def get_queryset(self):
        qs = super().get_queryset()
        if 'type' in self.request.GET:
            qs = qs.filter(cv_type=int(self.request.GET['type']))
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



class CvResponseView(View):
    pass



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
        bookmarks = BookmarkVacancy.objects.filter(employer=user)
        data['table'] = render_to_string(
            'employer/includes/inc_bookmarks_table.html',
            {'bookmarks': bookmarks},
            request=request
        )
        return JsonResponse(data)





class BookmarkDeleteView(BSModalDeleteView):
    model = BookmarkCV
    template_name = 'employer/delete_bookmark.html'
    success_message = 'Success: Bookmark was deleted.'
    success_url = reverse_lazy('employer:bookmarks')
    # return HttpResponseRedirect(reverse('employer:cvs'))
