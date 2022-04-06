from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from branch.models import Branch
from restaurant.models import Restaurant


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    level = models.IntegerField(unique=True)

    def __str__(self):
        return f'{self.name}, level: {self.level}'


class UserManager(BaseUserManager):
    def create_user(self, username, password, role, email=None, provider=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('Users must have an username')

        norm_email = self.normalize_email(email)
        if norm_email and User.objects.filter(email=norm_email).first():
            raise ValueError('User with that email already exists')

        user = self.model(
            username=username,
            email=norm_email,
            role=role,
        )

        if provider:
            user.authentication_provider = provider

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, email=None):
        """
        Creates and saves a super user with the given data and the
        Administrator role.
        """
        portal_manager = Role.objects.filter(level=0).first()
        user = self.create_user(
            username,
            password,
            portal_manager,
            email=self.normalize_email(email)
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    objects = UserManager()
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    authentication_provider = models.TextField(default='portal')

    def get_tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
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
                name='employee_profile_restaurant_branch_both_not_null'
            )
        ]
