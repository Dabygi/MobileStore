# Generated by Django 3.2.9 on 2021-11-13 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_customer_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='order',
            field=models.ManyToManyField(related_name='related_customer', to='store.Order', verbose_name='Заказы покупателя'),
        ),
    ]
