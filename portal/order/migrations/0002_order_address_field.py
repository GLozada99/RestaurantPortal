# Generated by Django 3.2.12 on 2022-04-07 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.TextField(default='Here'),
            preserve_default=False,
        ),
    ]
