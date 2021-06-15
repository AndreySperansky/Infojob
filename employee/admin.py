from django.contrib import admin

from .models import CV, BookmarkCV

class CvAdmin(admin.ModelAdmin):
    # какие поля будут отображаться в админке
    list_display = ('id', 'user', 'first_name', 'family_name', 'email', 'position_seek', 'profession', 'created_at')
    # какие поля будут ссылками на соответствующие модели
    list_display_links = ('id', 'user', 'first_name', 'family_name', 'email', 'position_seek')
    # какие поля будут участвовать в поиске
    search_fields = ('user', 'first_name', 'family_name', 'position_seek')


admin.site.register(CV, CvAdmin)


class BookmarkCVAdmin(admin.ModelAdmin):
    # какие поля будут отображаться в админке
    list_display = ('id', 'cv', 'employer',)
    # какие поля будут ссылками на соответствующие модели
    list_display_links = ('id', 'cv', 'employer',)
    # какие поля будут участвовать в поиске
    search_fields = ('cv', 'employer',)


admin.site.register(BookmarkCV, BookmarkCVAdmin)


# class ResponseCVAdmin(admin.ModelAdmin):
#     # какие поля будут отображаться в админке
#     list_display = ('id', 'user', 'cv', 'message')
#     # какие поля будут ссылками на соответствующие модели
#     list_display_links = ('id', 'user', 'cv',)
#     # какие поля будут участвовать в поиске
#     search_fields = ('user', 'cv',)
#
#
# admin.site.register(ResponseCV, ResponseCVAdmin)

