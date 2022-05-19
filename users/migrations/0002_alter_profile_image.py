# Generated by Django 3.2.13 on 2022-05-18 04:00

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='profile/default.png', upload_to=users.models.directory_path),
        ),
    ]