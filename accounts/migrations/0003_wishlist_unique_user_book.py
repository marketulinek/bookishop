# Generated by Django 4.2.10 on 2024-03-12 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_wishlist'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='wishlist',
            constraint=models.UniqueConstraint(fields=('user', 'book'), name='unique_user_book'),
        ),
    ]