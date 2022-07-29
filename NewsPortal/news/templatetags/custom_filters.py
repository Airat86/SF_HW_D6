from django import template

register = template.Library()  # Регистрируем наш фильтр


# @register.filter(name='multiply') # Регистрируем наш фильтр под названием multiply

# def multiply(value, arg): # Первый аргумент это то, к чему надо применить фильтр, второй - это аргумент фильтра
#    if isinstance(value, str) and isinstance(arg, int): # Проверяем что value это точно строка, а arg точно число
#        return str(value) * arg # Возвращаемое функцией значение - это то значение, которое подставится к нам в шаблон
#    else:
#        raise ValueError(f'Нельзя умножить {type(value)} на {type(arg)}') # Выводим ошибку если вдруг неправильно применим наш тэг


censor_list = ['БББББ', 'ХХХХХ', 'ССССС']


@register.filter(name='censor')
def censor(value):
    for word in censor_list:
        value = value.replace(word, '***')
    return value
