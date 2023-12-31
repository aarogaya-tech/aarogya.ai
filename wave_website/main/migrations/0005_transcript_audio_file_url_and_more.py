# Generated by Django 4.2.6 on 2023-10-17 03:23

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_sessionnote'),
    ]

    operations = [
        migrations.AddField(
            model_name='transcript',
            name='audio_file_url',
            field=models.FileField(null=True, upload_to=main.models.transcript_file_upload),
        ),
        migrations.AlterField(
            model_name='transcript',
            name='text_file_url',
            field=models.FileField(null=True, upload_to=main.models.transcript_file_upload),
        ),
    ]
