# https://dev.to/fleepgeek/prevent-multiple-sessions-for-a-user-in-your-django-application-13oo
# Link used for creating Only one session for the user.
from django.contrib.sessions.models import Session

class OneSessionPerUserMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user is not None and request.user.is_authenticated:
            stored_session_key = request.user.logged_in_user.session_key

            if stored_session_key and stored_session_key != request.session.session_key:
                Session.objects.get(session_key=stored_session_key).delete()

            request.user.logged_in_user.session_key = request.session.session_key
            request.user.logged_in_user.save()

        response = self.get_response(request)

        return response
