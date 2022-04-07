# Generated by Django 3.2.12 on 2022-04-07 17:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('branch', '0010_add_restaurant_to_promotion'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dish', '0007_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_cost', models.FloatField()),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='branch.branch')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderPromotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
                ('promotion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='branch.promotion')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dish.dish')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='dishes',
            field=models.ManyToManyField(through='order.OrderDish', to='dish.Dish'),
        ),
        migrations.AddField(
            model_name='order',
            name='promotions',
            field=models.ManyToManyField(through='order.OrderPromotion', to='branch.Promotion'),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='order.orderstatus'),
        ),
        migrations.AddConstraint(
            model_name='orderpromotion',
            constraint=models.UniqueConstraint(fields=('order', 'promotion'), name='order_promotion_unique_constraint'),
        ),
        migrations.AddConstraint(
            model_name='orderdish',
            constraint=models.UniqueConstraint(fields=('order', 'dish'), name='order_dish_unique_constraint'),
        ),
    ]
