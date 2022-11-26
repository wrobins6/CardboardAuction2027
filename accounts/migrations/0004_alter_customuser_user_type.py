# Generated by Django 4.1.3 on 2022-11-25 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'buyer'), (2, 'consigner'), (3, 'curator')], default=1),
        ),
    ]