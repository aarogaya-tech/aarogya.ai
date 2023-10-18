# Generated by Django 4.2.6 on 2023-10-18 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_transcript_generated_transcript'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='emergency_contact',
        ),
        migrations.AddField(
            model_name='patient',
            name='address',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='education',
            field=models.CharField(max_length=511, null=True),
        ),
        migrations.AddField(
            model_name='transcript',
            name='transcript_generation_in_progress',
            field=models.BooleanField(default=True),
        ),
    ]