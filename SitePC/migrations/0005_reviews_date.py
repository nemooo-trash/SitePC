# Generated by Django 3.2.18 on 2023-03-26 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SitePC', '0004_reviews'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
