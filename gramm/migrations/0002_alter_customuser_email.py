# Generated by Django 4.2.10 on 2024-04-01 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gramm', '0007_remove_customuser_social_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, unique=True),
        ),
    ]
