from django.contrib import admin

from .models import CV

class CvAdmin(admin.ModelAdmin):
    # какие поля будут отображаться в админке
    list_display = ('id', 'user', 'first_name', 'family_name', 'email', 'position_seek', 'profession', 'created_at')
    # какие поля будут ссылками на соответствующие модели
    list_display_links = ('id', 'user', 'first_name', 'family_name', 'email', 'position_seek')
    # какие поля будут участвовать в поиске
    search_fields = ('user', 'first_name', 'family_name', 'position_seek')


admin.site.register(CV, CvAdmin)