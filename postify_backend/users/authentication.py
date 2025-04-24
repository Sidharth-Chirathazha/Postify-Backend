from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken,TokenError

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
            user_id = access_token['user_id']
            user = User.objects.get(id=user_id)
            if not user.is_active:
                raise AuthenticationFailed({'detail': 'User account is deactivated'}, code='user_inactive')
        except TokenError as e:
            raise AuthenticationFailed({'detail': 'Token has expired or is invalid'}, code='token_not_valid')
        except User.DoesNotExist:
            raise AuthenticationFailed({'detail': 'User not found'}, code='user_not_found')
        except Exception:
            raise AuthenticationFailed({'detail': 'Authentication failed'}, code='authentication_failed')

        return (user, None)
    
    
