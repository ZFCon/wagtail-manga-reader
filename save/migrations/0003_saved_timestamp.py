# Generated by Django 2.2.7 on 2019-12-12 04:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('save', '0002_auto_20191212_0513'),
    ]

    operations = [
        migrations.AddField(
            model_name='saved',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]