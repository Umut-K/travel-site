# Generated by Django 5.0.4 on 2024-05-29 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_review_updated_at_alter_review_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='destination',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
