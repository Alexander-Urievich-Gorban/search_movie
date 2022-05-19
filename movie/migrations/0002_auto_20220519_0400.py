# Generated by Django 3.2.13 on 2022-05-19 01:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_profile_image'),
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='description',
        ),
        migrations.RemoveField(
            model_name='category',
            name='description_en',
        ),
        migrations.RemoveField(
            model_name='category',
            name='description_ru',
        ),
        migrations.RemoveField(
            model_name='reviews',
            name='email',
        ),
        migrations.RemoveField(
            model_name='reviews',
            name='name',
        ),
        migrations.AddField(
            model_name='reviews',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
        migrations.AlterField(
            model_name='actor',
            name='slug',
            field=models.SlugField(default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='genre',
            name='slug',
            field=models.SlugField(default='', max_length=100),
        ),
    ]
