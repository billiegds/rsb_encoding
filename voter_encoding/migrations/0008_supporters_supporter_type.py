# Generated by Django 5.1.4 on 2025-01-28 10:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voter_encoding', '0007_alter_supporters_party_legend_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='supporters',
            name='supporter_type',
            field=models.TextField(default=django.utils.timezone.now, max_length=20),
            preserve_default=False,
        ),
    ]
