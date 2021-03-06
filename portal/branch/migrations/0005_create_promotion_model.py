# Generated by Django 3.2.12 on 2022-04-02 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0004_add_unique_constraint_to_inventory_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('branches', models.ManyToManyField(to='branch.Branch')),
            ],
        ),
    ]
