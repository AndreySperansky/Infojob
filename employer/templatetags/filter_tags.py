from django import template

register = template.Library()

# фильтрует QS по пользователю
@register.filter(name='in_user_category')
def in_user_category(objects, category):
    return objects.filter(user=category)

# как вариант регистрации без декоратора
# register.filter('in_user_category', in_user_category)

# фильтрует QS по связанной категории (компания)
@register.filter(name='in_company_category')
def in_company_category(objects, category):
    return objects.filter(company=category)


# Ищет пользователя в наборе
@register.filter(name='user_in')
def user_in(objects, user):
    if user.is_authenticated:
        return objects.filter(user=user).exists()
    return False