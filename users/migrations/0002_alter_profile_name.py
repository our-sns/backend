# Generated by Django 3.2.13 on 2022-10-22 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(max_length=20, verbose_name='프로필 이름'),
        ),
    ]