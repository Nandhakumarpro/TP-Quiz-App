# Generated by Django 3.1.4 on 2020-12-24 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_app', '0010_auto_20201224_0830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='username',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='password',
            field=models.CharField(max_length=255),
        ),
    ]
