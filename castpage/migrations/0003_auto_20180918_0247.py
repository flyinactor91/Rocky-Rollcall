# Generated by Django 2.1.1 on 2018-09-18 02:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('castpage', '0002_auto_20180916_2037'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pagesection',
            options={'ordering': ['created_date']},
        ),
        migrations.AddField(
            model_name='cast',
            name='managers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
