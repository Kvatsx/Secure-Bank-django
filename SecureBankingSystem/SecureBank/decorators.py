from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

ExternalUserList = ['I', 'O']
InternalUserList = ['R', 'S', 'A']
def is_external(user):
    return user.is_active and user.bankuser.type_of_user in ExternalUserList

def is_internal(user):
    return user.is_active and user.is_staff and user.bankuser.type_of_user in InternalUserList

def external_user_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    actual_decorator = user_passes_test(
        is_external,
        login_url=login_url,
        redirect_field_name=None
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def internal_user_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    actual_decorator = user_passes_test(
        is_internal,
        login_url=login_url,
        redirect_field_name=None
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

