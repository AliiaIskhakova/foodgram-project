# Generated by Django 3.0.7 on 2020-10-08 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_auto_20201008_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='tag',
            field=models.ManyToManyField(related_name='tag', to='recipes.Tag'),
        ),
    ]
