from django.contrib import admin

from .models import Vacancy, Company


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





admin.site.register(Company, CompanyAdmin)
admin.site.register(Vacancy, VacancyAdmin)
