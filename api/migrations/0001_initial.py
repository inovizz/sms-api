# Generated by Django 2.1.1 on 2018-09-10 19:00

import api.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(db_column='auth_id', max_length=100)),
            ],
            options={
                'db_table': 'account',
            },
            managers=[
                ('objects', api.models.MyUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='PhoneNumberModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('number', models.IntegerField()),
                ('account_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SmsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_from', models.CharField(db_column='from', max_length=16, validators=[django.core.validators.MinLengthValidator(6)])),
                ('to', models.CharField(max_length=16, validators=[django.core.validators.MinLengthValidator(6)])),
                ('text', models.CharField(max_length=120, validators=[django.core.validators.MinLengthValidator(1)])),
            ],
        ),
    ]