# Generated by Django 3.0.5 on 2020-05-17 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dishes', '0005_auto_20200514_0857'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.DeleteModel(
            name='DishImage',
        ),
    ]