from django.shortcuts import render
from django.http import HttpResponse
from .models import News
from employer.models import  Company
from django.views.generic import ListView, DetailView, CreateView

def index(request):
    print(request)   # <WSGIRequest: GET '/news/'>
    news = News.objects.all()
    companies = Company.objects.all()[:6]
    # news = News.objects.order_by('-created_at')
    context = {
        'news': news,
        'companies':companies,
        'title': 'InfoJob Home'
    }
    # ключи из словарей затем используются в качестве переменных в шаблонах
    return render(request, 'mainapp/index.html', context)
    # return render(request, template_name='news/index.html', context=context)


class ViewNews(DetailView):
    model = News
    template_name = 'mainapp/news.html'
    context_object_name = 'post'    # по умолчанию - object
    # pk_url_kwarg = 'id_news'      # если в urls path параметр отличный от pk или id






