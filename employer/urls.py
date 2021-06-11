from django.urls import path
from .views import *

app_name = 'employer'

urlpatterns = [
	path('', HomepageView.as_view(), name='employer'),

	path('company/<int:pk>/', CompanyDetail.as_view(), name='company_detail'),
    path('company/create/', CompanyCreate.as_view(), name='company_create'),
    path('company/update/<int:pk>/', CompanyUpdate.as_view(), name='company_update'),
    path('company/delete/<int:pk>/', CompanyDelete.as_view(), name='company_delete'),
    path('vacancy/<int:pk>/', VacancyDetail.as_view(), name='vacancy_detail'),
    path('vacancy/create/', VacancyCreate.as_view(), name='vacancy_create'),
    path('vacancy/update/<int:pk>/', VacancyUpdate.as_view(), name='vacancy_update'),
    path('vacancy/delete/<int:pk>/', VacancyDelete.as_view(), name='vacancy_delete'),

    path('cv/', SearchView.as_view(), name='cvs'),
    path('cv/list/', cvs, name='cv_list'),
    path('cv/bookmark/', BookmarkView.as_view(), name='bookmarks'),
    path('cv/bookmark/list/', cv_bookmarks, name='bookmark_list'),
    path('cv/bookmark/<int:pk>', add_remove_bookmark, name='cv_bookmark'),
    path('cv/delete/<int:pk>', BookmarkDeleteView.as_view(), name='delete_bookmark'),
    path('cv/read/<int:pk>', CvDetailView.as_view(), name='cv_read'),
    path('cv/filter/', CvFilterView.as_view(), name='cv_filter'),

    # path('response/', ResponseView.as_view(), name='responses'),
    path('response/', ResponseCreate.as_view(), name='response'),
    # path('response/list/', response_list, name='response_list'),
    # path('response/<int:pk>/', add_remove_response, name='add_response'),
    # path('response/read/<int:pk>/', ResponseView.as_view(), name='read_response'),
    # path('response/reject/<int:pk>/', ResponseView.as_view(), name='reject_response'),
]

