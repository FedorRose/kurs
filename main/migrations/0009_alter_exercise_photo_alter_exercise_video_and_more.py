# Generated by Django 4.1.2 on 2022-12-03 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_activeworkout'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='video',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='exerciseinworkout',
            name='weight',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
