from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone


class AdminInactivityTimeoutMiddleware:
    timeout_seconds = 120
    session_key = 'admin_last_activity'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        login_url = reverse('custom_admin_login')
        logout_url = reverse('custom_admin_logout')
        is_admin_area = request.path.startswith('/admin-panel/')
        is_login_or_logout = request.path in {login_url, logout_url}

        if is_admin_area and not is_login_or_logout and request.user.is_authenticated and request.user.is_staff:
            now = timezone.now().timestamp()
            last_activity = request.session.get(self.session_key)

            if last_activity and now - float(last_activity) > self.timeout_seconds:
                logout(request)
                messages.error(request, 'Your admin session expired after 2 minutes of inactivity.')
                return redirect(f'{login_url}?next={request.path}')

            request.session[self.session_key] = now

        return self.get_response(request)
