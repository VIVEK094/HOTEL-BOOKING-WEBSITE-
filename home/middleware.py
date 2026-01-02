# filepath: home/middleware.py

from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import logout

class NoCacheMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

class LogoutOnFirstVisitMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and not request.session.get('has_visited', False):
            logout(request)
            request.session['has_visited'] = True