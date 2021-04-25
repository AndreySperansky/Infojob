from django.urls import path
from .views import index, ViewNews

app_name = 'mainapp'

urlpatterns = [
    path('', index, name='index'),
    path('news/<int:pk>/', ViewNews.as_view(), name = 'view_news')
]