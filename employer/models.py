from django.db import models
from django.conf import settings
from employee.models import CV



class Company(models.Model):

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
        ordering = ['company_name']

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='company',
        verbose_name='создатель'
    )
    #dash = request.user.company.all()  для доступа ко всем компаниям пользователя
    company_name = models.CharField(max_length=150, verbose_name='Наименование')
    industry_name = models.CharField(max_length=150, verbose_name='индустрия')
    logo_pic = models.ImageField(upload_to='companies/%Y/%m/%d/', verbose_name='Логотип')
    email = models.EmailField(max_length=150, unique=True)
    site_link = models.URLField(max_length=150, verbose_name='ссылка на сайт', blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Активно')
    is_checked = models.BooleanField(default=True, verbose_name='Проверено')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    def __str__(self):
        return f"{self.company_name}"

    @property
    def related_company(self):
        '''
        Filter up companies off users
        '''
        _companies = Company.objects.filter(user=self.user)
        return _companies




class Vacancy(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='for_company' )
    position = models.CharField(max_length=150, verbose_name='должность')
    city = models.CharField(max_length=150, verbose_name='город')
    duties = models.TextField(verbose_name='обязанности')
    compensation = models.PositiveIntegerField(verbose_name='зарплата')
    is_active = models.BooleanField(default=True, verbose_name='активно')
    is_checked = models.BooleanField(default=True, verbose_name='проверено')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='обновлено')
    employee_bookmarked = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='BookmarkVacancy',
        related_name='bookmark_holder',
        verbose_name='владелец закладки',
    )
    response = models.ManyToManyField(
        CV,
        through='Response',
        related_name='vacancy_cv',
        verbose_name='резюме',
    )



    def __str__(self):
        return f"{self.position}, {self.city}, {self.compensation}"

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['position', '-compensation']



class BookmarkVacancy(models.Model):
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='employee_concern',
        verbose_name='Соискатель')
    vacancy = models.ForeignKey(
        Vacancy,
        on_delete=models.CASCADE,
        related_name='bookmarked_vacancy',
        verbose_name='Вакансия')
    # in_bookmarks = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.vacancy.position}, {self.vacancy.compensation}, {self.vacancy.company}'


    class Meta:
        verbose_name = 'Избранные вакансии'
        verbose_name_plural = 'Избранные вакансии'
        ordering = ['vacancy']


class Response(models.Model):
    cv = models.ForeignKey(
        CV,
        on_delete=models.CASCADE,
        related_name='fk_cv',
        verbose_name='Резюме')
    vacancy = models.ForeignKey(
        Vacancy,
        on_delete=models.CASCADE,
        related_name='fk_vacancy',
        verbose_name='Вакансия')
