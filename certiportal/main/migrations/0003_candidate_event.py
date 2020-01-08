# Generated by Django 3.0.1 on 2020-01-07 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20200107_2100'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='event',
            field=models.CharField(choices=[('Dance', 'Electric Heels'), ('Music', 'Raga High'), ('Drama', 'Street Play')], default='', max_length=30),
        ),
    ]