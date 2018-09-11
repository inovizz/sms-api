"""Models file defining database schema and Custom auth user"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinLengthValidator


class MyUserManager(BaseUserManager):
    """Custom auth user class which inherits BaseUserManager to override few
    things and define UserModel."""
    use_in_migrations = True

    def create_superuser(self, username, password):
        """Overridden create_superuser method."""
        user = self.model(
            username=username,
            password=password
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class UserModel(AbstractBaseUser):
    """Custom auth user model which inherits AbstractBaseUser to add custom
    fields in Auth user. This model only has three fields - id, username and
    password(auth_id)."""
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
        """method to return str representation."""
        return self.username


class SmsModel(models.Model):
    """SmsModel class which defines the inboud and outbound sms schema."""
    _from = models.CharField(max_length=16, blank=False, db_column='from',
                             validators=[MinLengthValidator(6)])
    to = models.CharField(max_length=16, blank=False,
                          validators=[MinLengthValidator(6)])
    text = models.CharField(max_length=120, blank=False,
                            validators=[MinLengthValidator(1)])


class PhoneNumberModel(models.Model):
    """PhoneNumbers model which defines the phone_numbers table schema and
    defined account_id as foreign key to UserModel table."""
    id = models.AutoField(primary_key=True, blank=False)
    number = models.IntegerField(blank=False)
    account_id = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, null=True)
