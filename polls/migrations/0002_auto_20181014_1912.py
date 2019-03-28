# Generated by Django 2.1 on 2018-10-14 16:12

from django.db import migrations, models
import tagging.fields


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comentary',
            name='compendiums',
        ),
        migrations.RemoveField(
            model_name='comentary',
            name='users',
        ),
        migrations.RemoveField(
            model_name='comentary_rate',
            name='comentarys',
        ),
        migrations.RemoveField(
            model_name='comentary_rate',
            name='users',
        ),
        migrations.AddField(
            model_name='compendium',
            name='tags',
            field=tagging.fields.TagField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='compendium',
            name='rating',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.DeleteModel(
            name='comentary',
        ),
        migrations.DeleteModel(
            name='comentary_rate',
        ),
    ]