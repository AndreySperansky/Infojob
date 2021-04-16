from django.urls import path
from .views import *


app_name = 'employee'

urlpatterns = [
	path('', HomepageView.as_view(), name='employee'),
	path('<int:pk>/', CollectionDetailView.as_view(), name='cv_detail'),
    path('create/', CollectionCreate.as_view(), name='cv_create'),
    path('update/<int:pk>/', CollectionUpdate.as_view(), name='cv_update'),
    path('delete/<int:pk>/', CollectionDelete.as_view(), name='cv_delete'),
    path('vacancy/', SearchView.as_view(), name='vacancies'),
    path('vacancy/list/', vacancies, name='job_list'),
    path('vacancy/filter/', JobFilterView.as_view(), name='job_filter'),
    path('vacancy/bookmark/<int:pk>', JobBookmarkView.as_view(), name='job_bookmark'),
    path('vacancy/response/<int:pk>', JobResponseView.as_view(), name='job_response'),
    path('vacancy/read/<int:pk>', JobReadView.as_view(), name='job_read'),
]
