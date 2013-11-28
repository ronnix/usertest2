from django.contrib.auth.models import User

User.USERNAME_FIELD = 'email'