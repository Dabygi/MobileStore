# Generated by Django 3.1.1 on 2020-09-29 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='url',
            new_name='slug',
        ),
        migrations.RenameField(
            model_name='notebook',
            old_name='url',
            new_name='slug',
        ),
        migrations.RenameField(
            model_name='smartphone',
            old_name='url',
            new_name='slug',
        ),
    ]