# Generated by Django 2.1.2 on 2018-10-28 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requestHandler', '0004_auto_20181028_0342'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='FilePath',
        ),
        migrations.AddField(
            model_name='song',
            name='File',
            field=models.FileField(null=True, upload_to='songs/'),
        ),
    ]