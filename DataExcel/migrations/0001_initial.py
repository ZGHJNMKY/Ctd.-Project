# Generated by Django 2.0.4 on 2018-07-24 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImportRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_by', models.CharField(max_length=100)),
                ('import_date', models.TimeField(auto_now=True)),
                ('import_name', models.CharField(max_length=100)),
                ('import_year', models.IntegerField()),
                ('import_month', models.IntegerField()),
                ('import_type', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
            ],
        ),
    ]
