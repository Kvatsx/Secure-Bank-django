
def get_value(request, param):
    if param in request:
        return request[param]
    return ""

# https://rock-it.pl/custom-exception-handler-in-django/
class SecureBankException(Exception):
    pass
