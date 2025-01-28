# Generated by Django 5.1.5 on 2025-01-28 07:01

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voter_encoding', '0005_remove_partyleader_cluster_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='supporters',
            name='party_legend',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='supporters',
            name='supporter_legend',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
