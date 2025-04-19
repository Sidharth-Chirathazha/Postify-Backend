from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()

class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username = None, password = None, **kwargs):
        try:
            user = User.objects.get(Q(email=username) | Q(username=username))
        except User.DoesNotExist:
            return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None
    
class JWTAuthenticationFromCookie(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('access_token')
        if not token:
            return None  # No token found

        try:
            access_token = AccessToken(token)
            user = User.objects.get(id=access_token['user_id'])
        except Exception:
            raise AuthenticationFailed('Invalid or expired token')

        return (user, None)
    
    
