# Generated by Django 2.2.23 on 2021-05-21 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20210522_0331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=models.SlugField(max_length=150, unique=True, verbose_name='Адрес группы'),
        ),
    ]
