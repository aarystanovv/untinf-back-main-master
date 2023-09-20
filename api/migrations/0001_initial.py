# Generated by Django 4.1.9 on 2023-09-19 18:20

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=1000)),
                ('options', models.JSONField()),
                ('content', models.URLField(blank=True, null=True)),
                ('task', models.CharField(blank=True, max_length=1000, null=True)),
                ('taskContent', models.URLField(blank=True, null=True)),
                ('type', models.CharField(max_length=100)),
                ('topic', models.CharField(max_length=100)),
                ('answer', models.CharField(max_length=1000)),
                ('format', models.CharField(max_length=100)),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
        ),
    ]
