# Generated by Django 3.0.5 on 2020-05-10 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dishes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='adds_on',
            field=models.TextField(blank=True, null=True),
        ),
    ]