from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from portal.branch.models import Branch
from portal.restaurant.models import Restaurant


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    level = models.IntegerField(unique=True)

    def __str__(self):
        return f'{self.name}, level: {self.level}'


class UserManager(BaseUserManager):
    def create_user(
            self, username,
            password, role,
            email, change_password_token=None,
            provider=None,
    ):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('Username is required')
        if not email:
            raise ValueError('Email is required')

        norm_email = self.normalize_email(email)
        if User.objects.filter(email=norm_email).exists():
            raise ValueError('User with that email already exists')
        user = self.model(
            username=username,
            email=norm_email,
            role=role,
            change_password_token=change_password_token,
        )

        if provider:
            user.authentication_provider = provider

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, email=None):
        """
        Creates and saves a superuser with the given data and the
        Administrator role.
        """
        portal_manager = Role.objects.get(level=0)
        user = self.create_user(
            username,
            password,
            portal_manager,
            email=self.normalize_email(email),
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    objects = UserManager()
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    authentication_provider = models.TextField(default='portal')
    email = models.EmailField(_('email address'), blank=True)
    change_password_token = models.CharField(
        _('change_password_token'), max_length=128, blank=True, null=True,
    )

    def get_tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,
                                   blank=True, null=True, default=None)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE,
                               blank=True, null=True, default=None)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(restaurant__isnull=False) | models.Q(
                    branch__isnull=False),
                name='employee_profile_restaurant_branch_both_not_null',
            )
        ]
