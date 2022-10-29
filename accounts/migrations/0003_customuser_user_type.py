# Generated by Django 4.1.2 on 2022-10-27 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_customer_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'buyer'), (2, 'consigner'), (3, 'curator')], default=11111),
            preserve_default=False,
        ),
    ]
