# Generated by Django 3.0.8 on 2020-07-31 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_question_credit'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
    ]