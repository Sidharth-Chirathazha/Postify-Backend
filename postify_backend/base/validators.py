import re
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from rest_framework import serializers


def username_validator(username):
    if not re.match(r"^[A-Za-z][A-Za-z0-9]*$", username):
        raise serializers.ValidationError("Username must start with a letter and contain only letters and numbers.")
    
def email_validator(email):
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        raise serializers.ValidationError("Enter a valid email address.")
    
def password_validator(password):
    if len(password) < 5:
        raise serializers.ValidationError("Password must be at least 5 characters long.")
    if " " in password:
        raise serializers.ValidationError("Password cannot contain spaces.")
    
def author_validator(value):
    for author in value:
        name = author["name"].strip()
        if not name:
            raise serializers.ValidationError("Author name cannot be empty.")
        
        if not re.match(r"^[A-Za-z]", name):
            raise serializers.ValidationError("Author name must start with an alphabet.")

        if not re.match(r"^[A-Za-z][A-Za-z\s.]*$", name):
            raise serializers.ValidationError("Author name can only contain alphabets, spaces, and periods.")

    return value

def text_validator(value, field="This field"):
    if not re.match(r"^[A-Za-z0-9]", value):
        raise serializers.ValidationError(f"{field} must start with an alphabet or a number and not a space or special character.")
    
def name_validator(value, field="This field"):
    if not re.match(r"^[A-Za-z]+$", value):
        raise serializers.ValidationError(f"{field} must contain only alphabets and no spaces or special characters.")
    

def date_validator(value):
    if value > now().date():
            raise serializers.ValidationError("Publication date cannot be in the future.")