# Generated by Django 3.1.3 on 2021-05-19 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biomechlabwebapp', '0002_auto_20210519_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='attachment',
            field=models.FileField(upload_to=''),
        ),
    ]
