from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone_number, is_tutor, is_student, password=None):
        if not email:
            raise ValueError('You must have an email to continue')
        if not phone_number:
            raise ValueError('Users must have a phone number to continue')

        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
            is_student=is_student,
            is_tutor=is_tutor,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, phone_number, is_tutor=True, is_student=False, password=None):
        user = self.create_user(
            email,
            phone_number,
            password=password,
            is_student=is_student,
            is_tutor=is_tutor
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    first_name  = models.CharField(max_length = 30, blank = True, null =True)
    surname  = models.CharField(max_length = 30, blank = True, null =True)
    email = models.EmailField(verbose_name="email",
                              max_length=200, unique=True)
    phone_number = models.CharField(max_length=13)
    is_tutor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    image = models.ImageField(upload_to="files/profiles", blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', ]

    def __str__(self):
        return self.email

    def has_perm(self, perm, object=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_tutor
