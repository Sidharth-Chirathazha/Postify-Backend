from rest_framework import serializers
import logging
from django.contrib.auth import get_user_model
from base.validators import email_validator,username_validator,password_validator,name_validator
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()
logger = logging.getLogger(__name__) 

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "confirm_password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_username(self, value):
        username_validator(value)
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already taken")
        return value
    
    def validate_email(self, value):
        email_validator(value)
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
    
    def validate_password(self, value):
        password_validator(value)
        return value
    
    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords doesn't match")
        return data
    
    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(**validated_data)
        return user
    

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[lambda value: username_validator(value)])
    first_name = serializers.CharField(validators=[lambda value: name_validator(value, "First Name")])
    last_name = serializers.CharField(validators=[lambda value: name_validator(value, "Last Name")])
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "role", "profile_pic"]
        extra_kwargs = {
            "email": {"read_only": True}
        }
    

class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        
        if user is None:
            raise serializers.ValidationError("Invalid credentials. Please try again")
        if not user.is_active:
            raise serializers.ValidationError("Your account has been deactivated. Please contact support")
        
        return user
    
class LogoutSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        self.request = kwargs['context']['request']
        super().__init__(*args, **kwargs)

    def validate(self, data):
        refresh_token = self.request.COOKIES.get('refresh_token')
        if not refresh_token:
            raise serializers.ValidationError("Refresh token not found in cookies.")
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            raise serializers.ValidationError("Invalid or expired refresh token.")
        
        return {}