# Generated by Django 2.1 on 2018-10-15 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_coment_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='language',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='users',
            name='style',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='compendium',
            name='rating',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
