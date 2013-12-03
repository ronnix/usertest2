from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from rest_framework import serializers

class UserManager(models.Manager):
    @classmethod
    def normalize_email(cls, email):
        """
        Normalize the address by lowercasing the domain part of the email
        address.
        """
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name, domain_part.lower()])
        return email

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves an User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = UserManager.normalize_email(email)
        user = self.model(email=email, is_staff=False, is_active=True,
                          is_superuser=False, last_login=now,
                          date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def make_random_password(self, length=10, allowed_chars='abcdefghjkmnpqrstuvwxyz'
                             'ABCDEFGHJKLMNPQRSTUVWXYZ' '23456789'):
        """
        Generates a random password with the given length and given
        allowed_chars. Note that the default value of allowed_chars does not
        have "I" or "O" or letters and digits that look similar -- just to
        avoid confusion.
        """
        return get_random_string(length, allowed_chars)

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})



class User(AbstractBaseUser, PermissionsMixin):
    """
    Abstract User with the same behaviour as Django's default User but
    without a username field. Uses email as the USERNAME_FIELD for
    authentication.

    Inherits from both the AbstractBaseUser and PermissionMixin.
    The following attributes are inherited from the superclasses:
        * password
        * last_login
        * is_superuser
    """
    email = models.EmailField(_('email address'), max_length=255,
                              unique=True, db_index=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)

    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    # def get_full_name(self):
    #     """
    #     Returns the email.
    #     """
    #     return self.first_name

    def get_short_name(self):
        """
        Returns the email.
        """
        return self.email

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])


class Wine(models.Model):
	#How to reference wines when creating a bottle (domaine_millesime?)
    couleur = models.CharField(max_length=100, blank=True)
    pays = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    appellation = models.CharField(max_length=100, blank=True)
    domaine = models.CharField(max_length=100, blank=True)
    cuvee = models.CharField(max_length=100, blank=True)
    millesime = models.IntegerField()
    price = models.IntegerField()
    quantity = models.IntegerField()
    description = models.TextField()
    added_on = models.DateTimeField()


    def __unicode__(self):
        return self.domaine #concatenate?

    def update_qty(self, quantity):
        self.quantity -= quantity
        self.save()

    def qty(self):
        return self.quantity

class Container(models.Model):

	CONTAINER_TYPE = (
	('cellar', 'Cellar'),
	('vinibar', 'Vinibar'),
	('history', 'History'),
	)

	container_type = models.CharField(max_length=10, choices=CONTAINER_TYPE)
	user = models.ForeignKey(User, related_name='user_id')

# class Vinibar(Container):
# 	user = models.ForeignKey(User)
# 	#container_type = vinibar

# class History(Container):
# 	user = models.ForeignKey(User)

	#Vinibar & History must be created when a user is created?

class Movement(models.Model):
    date = models.DateTimeField()
    start = models.ForeignKey(Container, related_name='movement_start')
    finish = models.ForeignKey(Container, related_name='movement_finish')
    quantity = models.IntegerField(default=1)
