from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    level = models.IntegerField(unique=True)

    def __str__(self):
        return f'{self.name}, level: {self.level}'


class UserManager(BaseUserManager):
    def create_user(self, username, password, role, email=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            role=role
        )

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
