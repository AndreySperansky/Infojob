# Generated by Django 3.1.7 on 2021-03-24 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_auto_20210323_2345'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobexp',
            name='employer_link',
        ),
    ]
