# Generated by Django 5.0.1 on 2024-01-14 14:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
        ('users', '0005_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='answer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.answer'),
        ),
    ]