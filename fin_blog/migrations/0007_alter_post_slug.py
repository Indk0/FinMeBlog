# Generated by Django 5.1.4 on 2024-12-31 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fin_blog', '0006_reaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, unique=True),
        ),
    ]