# Generated by Django 3.1.7 on 2021-03-30 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Packet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_ip_address', models.CharField(max_length=39, null=True)),
                ('destination_ip_address', models.CharField(max_length=39, null=True)),
                ('source_host_name', models.CharField(max_length=256, null=True)),
                ('destination_host_name', models.CharField(max_length=256, null=True)),
                ('version', models.CharField(max_length=256, null=True)),
                ('header_length', models.IntegerField(default=0)),
                ('ttl', models.CharField(max_length=256, null=True)),
                ('protocol', models.IntegerField(default=0)),
                ('source_port', models.CharField(max_length=5, null=True)),
                ('destination_port', models.CharField(max_length=5, null=True)),
                ('sequence_number', models.CharField(max_length=256, null=True)),
                ('acknowledgement', models.CharField(max_length=256, null=True)),
                ('urg', models.BooleanField(default=False)),
                ('ack', models.BooleanField(default=False)),
                ('psh', models.BooleanField(default=False)),
                ('rst', models.BooleanField(default=False)),
                ('syn', models.BooleanField(default=False)),
                ('fin', models.BooleanField(default=False)),
                ('payload', models.TextField(default=None)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Scan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('command', models.TextField(default=None)),
                ('scan', models.TextField(default='{}')),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
            options={
                'managed': True,
            },
        ),
    ]
