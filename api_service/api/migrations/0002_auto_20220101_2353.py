# Generated by Django 3.1.7 on 2022-01-01 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrequesthistory',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
