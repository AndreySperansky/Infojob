from django.test import TestCase

from .forms import CVFilterForm, VacancyCreateForm, ResponseCreateForm
from .models import *
from employee.models import *


bookmarks = BookmarkVacancy.objects.all()
print(bookmarks)
