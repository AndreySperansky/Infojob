from django.contrib import admin

from .models import Vacancy, Company, BookmarkVacancy, Response


class CompanyAdmin(admin.ModelAdmin):
    # какие поля будут отображаться в админке
    list_display = ('id', 'user', 'company_name', 'industry_name', 'email', 'is_active', 'created_at')
    # какие поля будут ссылками на соответствующие модели
    list_display_links = ('id', 'user', 'company_name')
    # какие поля будут участвовать в поиске
    search_fields = ('user','company_name', 'industry_name')



class VacancyAdmin(admin.ModelAdmin):
    # какие поля будут отображаться в админке
    list_display = ('id', 'company', 'position', 'city', 'compensation', 'is_active', 'created_at')
    # какие поля будут ссылками на соответствующие модели
    list_display_links = ('id', 'company')
    # какие поля будут участвовать в поиске
    search_fields = ('company', 'position', 'city', 'compensation')




class BookmarkVacancyAdmin(admin.ModelAdmin):
    # какие поля будут отображаться в админке
    list_display = ('id', 'vacancy', 'employee',)
    # какие поля будут ссылками на соответствующие модели
    list_display_links = ('id', 'vacancy', 'employee',)
    # какие поля будут участвовать в поиске
    search_fields = ('vacancy', 'employee',)



class ResponseAdmin(admin.ModelAdmin):
    # какие поля будут отображаться в админке
    list_display = ('id', 'cv', 'vacancy', 'message')
    # какие поля будут ссылками на соответствующие модели
    list_display_links = ('id', 'cv', 'vacancy',)
    # какие поля будут участвовать в поиске
    search_fields = ('cv', 'vacancy',)



admin.site.register(Company, CompanyAdmin)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(BookmarkVacancy, BookmarkVacancyAdmin)
admin.site.register(Response, ResponseAdmin)



