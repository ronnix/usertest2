from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

from rest_framework import serializers
from rest_framework.authtoken.models import Token

# @receiver(post_save, sender=user2.User)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)


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
    email = models.EmailField(_('email address'), max_length=255, unique=True, db_index=True)
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

   


    def save(self, *args, **kwargs):
    	super(User, self).save(*args, **kwargs)
    	c, _ = Container.objects.get_or_create(container_type='cellar', user=self) #Comment creer une cave unique? Utile?
    	c.save()
    	v, _ = Container.objects.get_or_create(container_type='vinibar', user=self)
    	v.save()
    	h, _ = Container.objects.get_or_create(container_type='history', user=self)
    	h.save()
    	m1, _ = Movement.objects.get_or_create(start=c, finish=v)
    	m1.save()
    	m2, _ = Movement.objects.get_or_create(start=v, finish=h)
    	m2.save()

        def __unicode__(self):
        	return self.email


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
    description = models.TextField()  #TODO: accepter accents
    added_on = models.DateTimeField(auto_now_add=True)


    def __unicode__(self):
        return u'%s %s' % (self.domaine, self.millesime)

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
	user = models.ForeignKey(User, related_name='user_id') #TODO: change related name to containers

	def __unicode__(self):
		return u'%s %s' % (self.container_type, self.user)

	# class Meta:
	# 	unique_together = ('container_type', 'user')

class Movement(models.Model):
    date = models.DateTimeField(null=True, blank=True, default=None)
    start = models.ForeignKey(Container, related_name='movement_start') #imposer start/user == finish.user
    finish = models.ForeignKey(Container, related_name='movement_finish') #TODO: change related name
    quantity = models.IntegerField(default=1)

    def __unicode__(self):
		return u'%s %s %s' % (self.start, "to", self.finish)

	# class Meta:
	# 	unique_together = ('start', 'finish') #TODO: Check for / remove duplicates 

class Bottle(models.Model):
	#id = ???
	wine = models.ForeignKey(Wine, null=False)
	user = models.ForeignKey(User, null=False)

	mounted = models.ForeignKey(Movement, null=True, blank=True, default=None, related_name='bottle_mounted') #TODO: change related name
	rated = models.ForeignKey(Movement, null=True, blank=True, default=None, related_name='bottle_rated') #TODO: change related name
	date_mounted = models.DateTimeField() #included in Movement but necessary for filter? #DateTime or Date?
	date_rated = models.DateTimeField(null=True, blank=True, default=None) #included in Movement but necessary for filter?
	
	rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=True, blank=True, default=None) #integer for 3.5? Blank=True?
	comment = models.TextField(null=True, blank=True, default=None)
	#tags = models.ManyToManyField('tags.Tag', related_name='posts')

	def __unicode__(self):
		return u'%s %s' % (self.wine.domaine, self.wine.millesime)

	def save(self, *args, **kwargs):
		d = datetime.now()
		# self.wine = wine #wine referencing issue
		# self.user = user
		self.mounted = Movement.objects.filter(start__user=self.user, 
			start__container_type='cellar', finish__container_type='vinibar')[0]
		self.date_mounted = d
		super(Bottle, self).save(*args, **kwargs)
		self.mounted.date = d


	def rate(self, rating, comment, *args, **kwargs): #interet de *args, **kwargs quand on connait l'input?
		d = datetime.now()
		self.rating = rating
		self.comment = comment
		date_rated = d
		#TODO: can only be rated if it has been mounted
		v = Container.objects.get(container_type='vinibar', user=self.user)
		#TODO: handle error
		h = Container.objects.get(container_type='history', user=self.user)
		#TODO: handle error 
		m = Movement(date=d, start=v, finish=h) #quantity=quantity?
		m.save()
		self.rated = m

	def current_bottles():
		b = Bottle.objects.filter(user=self.user and self.rated==null).order_by('date_mounted')

	def rated_bottles():
		b = Bottle.objects.filter(user=self.user and rated.finish.user==self.user).order_by('date_rated')

	# def save(self, *args, **kwargs):
	# 	d = datetime.now()
	# 	self.wine = wine #wine referencing issue
	# 	self.user = user
	# 	#TODO: stock alert: 
	# 	#q = Wine.objects.get("wine_id").quantity
	# 	#if(q<1) raiseError('No bottle available') send email? 
	# 	#Wine.objects.get("wine_id").quantity -= 1
	# 	v = Container.objects.get(container_type='vinibar', user=user)
	# 	#TODO: handle error
	# 	c = Container.objects.get(container_type='cellar', user=admin)
	# 	#TODO: handle error 
	# 	m = Movement(date=d, start=c, finish=v) #quantity=quantity?
	# 	m.save()
	# 	self.mounted = m
	# 	#m.save()
	# 	self.date_mounted = d
	# 	super(Bottle, self).save(self, self.wine, self.user, *args, **kwargs)
