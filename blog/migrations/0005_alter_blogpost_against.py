# Generated by Django 5.1.1 on 2024-09-21 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_delete_userfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='against',
            field=models.CharField(choices=[('Eastern Cape', 'Eastern Cape'), ('Free State', 'Free State'), ('Gauteng', 'Gauteng'), ('KwaZulu-Natal', 'KwaZulu-Natal'), ('Limpopo', 'Limpopo'), ('Mpumalanga', 'Mpumalanga'), ('North West', 'North West'), ('Western Cape', 'Western Cape'), ('Northern Cape', 'Northern Cape,')], max_length=100),
        ),
    ]
