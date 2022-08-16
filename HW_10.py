"критерієм перевірки буде проходження всіх ассертів"

##############################################################################
############                                                     #############
############                      TASK 1                         #############
############                                                     #############
##############################################################################
"""
написати декоратор wrap_validate, який не приймає жодних параметрів
його задача - перевірити, що функція, яку він задекорував, обовязково отримала
в своїх аргументах параметр 'password' (згадуємо про * в написанні аргументів функції)
значення 'password' повинне бути стрічкою, довжиною не менше 10 символів,
та містити в собі латинські літери (регістр не принципово), арабські цифри та знак '!"

кожну з перевірок отриманого значення паролю виконуємо в ОКРЕМІЙ функції, функції робимо
універсальними, називаємо їх (з опційними параметрами)
- is_valid_length(length=10)
- has_any_symbols(symbols='qwertyuiopasdfghjklzxcvbnm') (це приклад для латинських букв, повертає тру, якщо хоч
один символ в стрічці, аналогічно зробити для цифр та знаку оклику (у вас буде 3 виклики функції в середині декоратора
з різними параметрами)
- is_string()

якщо  'password'  відсутній - викликаємо помилку
raise AttributeError(f'no parameter "password" in arguments of function{func.__name__}')

якщо  'password'  не задовольняє вимогам валідації, написаним вище, то повертається словник виду
{ 'result': str(func(*args, **kwargs)),
  'is_secure': False,
}

якщо  'password'  задовольняє вимогам валідації, написаним вище, то повертається словник виду
{ 'result': str(func(*args, **kwargs)),
  'is_secure': True,
}

зауважте, що str(func(*args, **kwargs)) МАЄ бути довжиною не більше 100 символів
якщо даний результат буде довшим за 100 символів, то стрічка має бути обрізана до 100 символів, причому останні
три символи мають бути ... (трьома крапками)
тут ви вже й самы здогадалися написати функцію на виконання даної роботи (тут вже без підказок)
"""

import datetime
import functools
import inspect
import string
from typing import Any


def get_argument(argument, func, passed_args: list = [], passed_kwargs: dict = {}):
    func_args = inspect.getfullargspec(func).args
    if not argument in func_args:
        raise TypeError(f"'{argument}' is an invalid argument for function '{func.__name__}'")
    elif argument in passed_kwargs.keys():
        return passed_kwargs[argument]
    else:
        argument_index = func_args.index(argument)
        if argument_index < len(passed_args):
            return passed_args[argument_index]


def is_string(arg):
    return type(arg) is str


def is_valid_length(target_string, length):
    return len(target_string) >= length


def has_any_symbols(target_string, symbols):
    return any((symbol in target_string) for symbol in symbols)


def truncate_string(target_string, length=100, end='...'):
    return (target_string[:97] + '...') if len(target_string) > 100 else target_string


def wrap_validate(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        is_secure_password = True

        password = get_argument('password', func, args, kwargs)

        if not password:
            raise AttributeError(f'no parameter "password" in arguments of function {func.__name__}')
        elif not is_string(password):
            is_secure_password = False
        elif not is_valid_length(password, 10):
            is_secure_password = False
        elif not has_any_symbols(target_string=password, symbols=string.ascii_letters):
            is_secure_password = False
        elif not has_any_symbols(target_string=password, symbols=string.digits):
            is_secure_password = False
        elif not has_any_symbols(target_string=password, symbols='!'):
            is_secure_password = False

        result = func(*args, **kwargs)
        formatted_result = truncate_string(result, length=100, end='...')

        return {
            'result': formatted_result,
            'is_secure': is_secure_password,
        }

    return wrapper

##############################################################################
############                                                     #############
############                      TASK 2                         #############
############                                                     #############
##############################################################################
"""
написати функцію registration, яка приймає
- позиційний аргумент id, стрічка або число - не важливо,  значення за замовчуванням - відсутнє
- позиційний або іменований аргумент login, тип даних - не важливий, значення за замовчуванням - відсутнє
- позиційний або іменований аргумент notes, тип даних - не важливий, значення за замовчуванням - відсутнє
- password - тип даних - не важливий, значення за замовчуванням - відсутнє

в середині функції вставити код (зназок для отримання даних прописаний нижче)
date = datetime.date.today()

результат робити функції - стрічка
f'User {login} created account on {date} with password "{password}". Additional information: {notes}'

задекоруйте написаним в завданні 1 декоратором
"""
@wrap_validate
def registration(id: [str, int], login: Any, notes: Any, password: Any) -> str:
    date = datetime.date.today()
    return f'User {login} created account on {date} with password "{password}". Additional information: {notes}'

##############################################################################
############                                                     #############
############                      TASK 3                         #############
############                                                     #############
##############################################################################
"""
створіть умову if name == main (тут ціленаправлено написано не вірно, як вірно - ви знаєте)
в цій умові створіть assert на всі створені функції (окрім декоратора), викликайте функції з різними параметрами 
(довжина слів, різні текстовки....)
на кожну функцію, що використовується в декораторі, має бути мінімум 3 ассерта,

функцію registration перевіряйте з огляду на роботу декоратора (ключі, значення). обовязково перевірте кількість ключів, 
тип даних в значеннях, назви ключів, значення отриманого результату в залежності від переданих даних   

ВАЖЛИВО 
функцію registration ассертимо ТІЛЬКИ при передачі їй валідних даних (поля паролю)
"""
if __name__ == '__main__':

# Validate 'get_argument' function
    def test_func(password):
        pass


    assert get_argument('password', test_func, [],
                        {}) is None, "function 'get_argument' should return None if empty args and kwargs are passed"
    assert get_argument('password', test_func, ['abc'],
                        {}), "function 'get_argument' should return valid parameter if it's passed as a positional argument"
    assert get_argument('password', test_func, [], {
        'password': 'abc'}), "function 'get_argument' should return valid parameter if it's passed as a named argument"

    # Validate 'is_string' function
    assert is_string(''), "is_string: True for an empty string expected, got False"
    assert is_string('abc'), "is_string: True for a non-empty string expected, got False"
    assert not is_string(1), "is_string: False for non-string types expected, got True"

    # Validate 'is_valid_length' function
    assert is_valid_length('abc', 3), "is_valid_length: True for a valid string length expected, got False"
    assert is_valid_length('abc', 2), "is_valid_length: False for an invalid string length expected, got True"
    assert is_valid_length('', 0), "is_valid_length: True for a valid length of empty string expected, got False"

    # Validate 'has_any_symbols' function
    assert has_any_symbols('a1!', 'aAbBcC'), "has_any_symbols: True for a valid case expected, got False"
    assert has_any_symbols('a1!', '12345'), "has_any_symbols: True for a valid case expected, got False"
    assert has_any_symbols('a1!', '?!'), "has_any_symbols: True for a valid case expected, got False"

    # Validate 'truncate_string' function
    assert not truncate_string('a' * 5, length=100, end='...').endswith(
        '...'), "truncate_string: Strings with a length less than expected length shouldn't be be truncated"
    assert not truncate_string('a' * 100, length=100, end='...').endswith(
        '...'), "truncate_string: Strings with a length equal to expected length shouldn't be be truncated"
    assert truncate_string('a' * 200, length=100, end='...').endswith(
        '...'), "truncate_string: Strings with a length greater than expected length should be be truncated"
#   Validate `wrap_validate` decorator

#   try:
#        registration(1, login='test_user', notes='developer')
#    except AttributeError as e:
#     assert 'no parameter "password" in arguments' in str(e), "decorator 'wrap_validate' should raise AttributeError if `password` argumernt isn't passed"

    assert not registration(1, login='test_user', notes='developer', password=5)[
        'is_secure'], 'wrap_validate: is_secure should be False if non-string password passed'
    assert not registration(1, login='test_user', notes='developer', password='a1!')[
        'is_secure'], 'wrap_validate: is_secure should be False if password length is less than 10'
    assert not registration(1, login='test_user', notes='developer', password='123456789!')[
        'is_secure'], 'wrap_validate: is_secure should be False if no ascii letters in the password'
    assert not registration(1, login='test_user', notes='developer', password='abCDefGHi!')[
        'is_secure'], 'wrap_validate: is_secure should be False if no digits in the password'
    assert not registration(1, login='test_user', notes='developer', password='abCDef12345')[
        'is_secure'], 'wrap_validate: is_secure should be False if no `!` symbol letters in the password'
##############################################################################
############                                                     #############
############                      TASK 4                         #############
############                     HAVE FUN                        #############
############                                                     #############
##############################################################################

