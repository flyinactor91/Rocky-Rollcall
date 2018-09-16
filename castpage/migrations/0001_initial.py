# Generated by Django 2.1.1 on 2018-09-16 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=200)),
                ('description', models.TextField()),
                ('external_url', models.URLField()),
                ('facebook_url', models.URLField()),
                ('twitter_user', models.CharField(max_length=15)),
                ('instagram_user', models.CharField(max_length=15)),
            ],
        ),
    ]
