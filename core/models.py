## Core App
    # holds all of the central code that is important to the rest of the sub apps that we create in our system
    # creates anything that is shared between 1 or more apps so things like the migrations and the database. (All in One Place)

from django.db import models
# these ar all things that are required to extend the Django user model while making use of some of the features that come with the django user model out of the box.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


## User Manager Class:
    # A class that provides the helper functions for creating a user or a super user
class UserManager(BaseUserManager):
    # Overridden Functions

    # "password=None" = in case, you want to create a user that is not active, that does not have a password
    # "**extra_fields" = says: take any of the extra functions that are passed in,
                             # when you call the "create_user" and pass them into extra fields
                             # so that we can then just add any additional fields that we create without user model.
                             # Not Required
                             # Little more flexible bec. every time we add new fields to our user, it means we don't have to add them in here.
    def create_user(self, email, password=None, **extra_fields):
        """ Creates and Saves a new User """
        # the manager can access the model.
        # "self.model" = creating a new user model
        # "normalize_email" is a helper function that comes with the "BaseUserManager"
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)

        # "using=self._db" - supporting multiple databases (Good Practice)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """ Creates and Saves a new super user """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom User Model that supports using email instead of username """

    # fields of our database model
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """ Tag to be used for a recipe """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    """ Ingredient to be used in a recipe """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """ Recipe object """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    # this string here, you can actually remove the quotes and just pass i the class directly.
    # The issue with this is you would have to then have your classes in a correct order.
    # So the Django has this useful feature where you can just provide the name of the class in a string
    # and then it doesn't matter which order you place your models in.
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title
