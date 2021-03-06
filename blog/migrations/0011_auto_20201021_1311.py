# Generated by Django 3.1.2 on 2020-10-21 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20201018_0904'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='activation_key',
            field=models.CharField(default=1, max_length=255),
        ),
        migrations.AddField(
            model_name='author',
            name='email_validated',
            field=models.BooleanField(default=False),
        ),
    ]
