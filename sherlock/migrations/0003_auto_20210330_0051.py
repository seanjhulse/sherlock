# Generated by Django 3.1.7 on 2021-03-30 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sherlock', '0002_auto_20210327_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='packet',
            name='destination_host_name',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='packet',
            name='source_host_name',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
