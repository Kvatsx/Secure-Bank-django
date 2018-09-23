from django.http import HttpResponseRedirect


def getArgumentsValues(request, param):
    if param in request:
        return request[param]
    return ""