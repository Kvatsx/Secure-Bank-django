# https://dev.to/fleepgeek/prevent-multiple-sessions-for-a-user-in-your-django-application-13oo
# Link used for creating Only one session for the user.
from django.contrib.sessions.models import Session
from django.contrib.auth import logout
from SecureBankingSystem import settings
from datetime import datetime, timedelta

class OneSessionPerUserMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user is not None and request.user.is_authenticated:
            stored_session_key = request.user.logged_in_user.session_key

            if stored_session_key and stored_session_key != request.session.session_key:
                Session.objects.get(session_key=stored_session_key).delete()

            request.user.logged_in_user.session_key = request.session.session_key
            request.user.logged_in_user.name = request.user.username
            request.user.logged_in_user.save()

        response = self.get_response(request)

        return response

class AutoLogout:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if not request.user.is_authenticated:
            return self.get_response(request)

        try:
            time = datetime.now()
            last_touch_string = request.session['last_touch']
            last_touch_date = datetime.strptime(last_touch_string, '%Y-%m-%d %H:%M:%S')

            if time - last_touch_date > (timedelta(0, settings.AUTO_LOGOUT_DELAY * 60, 0)):
                logout(request)
                del request.session['last_touch']
                print("User Auto Logged Out")
                return self.get_response(request)
            else:
                # time_now = datetime.now()
                # formatedDate = time_now.strftime("%Y-%m-%d %H:%M:%S")
                # request.session['last_touch'] = formatedDate
                return self.get_response(request)
        except KeyError:
            time_now = datetime.now()
            formatedDate = time_now.strftime("%Y-%m-%d %H:%M:%S")
            request.session['last_touch'] = formatedDate

        # request.session['last_touch'] = datetime.now()

        return self.get_response(request)
