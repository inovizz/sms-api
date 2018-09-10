from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinLengthValidator


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def create_superuser(self, username, password):
        user = self.model(
            username=username,
            password=password
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class UserModel(AbstractBaseUser):
    id = models.AutoField(primary_key=True, blank=False)
    username = models.CharField(max_length=100, blank=False, unique=True)
    password = models.CharField(max_length=100, blank=False,
                                db_column='auth_id')

    objects = MyUserManager()

    USERNAME_FIELD = "username"

    class Meta:
        app_label = "api"
        db_table = "account"

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username


class SmsModel(models.Model):
    _from = models.CharField(max_length=16, blank=False, db_column='from',
                             validators=[MinLengthValidator(6)])
    to = models.CharField(max_length=16, blank=False,
                          validators=[MinLengthValidator(6)])
    text = models.CharField(max_length=120, blank=False,
                            validators=[MinLengthValidator(1)])


class PhoneNumberModel(models.Model):
    id = models.AutoField(primary_key=True, blank=False)
    number = models.IntegerField(blank=False)
    account_id = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, null=True)
