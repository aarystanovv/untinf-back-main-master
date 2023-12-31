# Generated by Django 4.1.9 on 2023-09-19 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_question_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answer',
            field=models.CharField(max_length=10000),
        ),
        migrations.AlterField(
            model_name='question',
            name='format',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='question',
            name='task',
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='topic',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.CharField(max_length=1000),
        ),
    ]
