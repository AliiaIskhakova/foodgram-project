# Generated by Django 3.0.7 on 2020-10-08 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_auto_20201008_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='Имя в шаблоне'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='style',
            field=models.CharField(max_length=50, null=True, verbose_name='Цвет в шаблоне'),
        ),
    ]
