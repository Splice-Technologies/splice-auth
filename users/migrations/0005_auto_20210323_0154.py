# Generated by Django 3.1.7 on 2021-03-23 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210322_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password_reset_code',
            field=models.CharField(max_length=36, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='password_reset_expiration',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]