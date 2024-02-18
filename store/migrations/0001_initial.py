# Generated by Django 4.2.6 on 2023-10-23 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('books', '0006_book_cover'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookInventory',
            fields=[
                ('book', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='books.book')),
                ('quantity_in_hand', models.PositiveIntegerField(default=0)),
                ('quantity_to_be_delivered', models.PositiveIntegerField(default=0)),
                ('min_stock_limit', models.PositiveIntegerField(default=0)),
                ('max_stock_limit', models.PositiveIntegerField(default=0)),
                ('reorder_point', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]