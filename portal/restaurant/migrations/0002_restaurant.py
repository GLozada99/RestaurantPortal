# Generated by Django 3.2.12 on 2022-03-30 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('active_branches', models.IntegerField()),
                ('active_administrators', models.IntegerField()),
                ('is_active', models.BooleanField()),
                ('food_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='restaurant.foodtype')),
            ],
        ),
    ]