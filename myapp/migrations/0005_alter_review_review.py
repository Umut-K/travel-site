# Generated by Django 5.0.4 on 2024-04-30 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_rename_text_review_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review',
            field=models.TextField(blank=True),
        ),
    ]
