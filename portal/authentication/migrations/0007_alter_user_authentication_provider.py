# Generated by Django 3.2.12 on 2022-04-09 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_authentication_provider_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='authentication_provider',
            field=models.TextField(default='portal'),
        ),
    ]
