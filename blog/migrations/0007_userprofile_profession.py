# Generated by Django 5.1.1 on 2024-09-28 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_blogpost_against_alter_blogpost_province'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='profession',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
