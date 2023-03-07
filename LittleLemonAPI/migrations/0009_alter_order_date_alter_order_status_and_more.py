# Generated by Django 4.1.5 on 2023-03-05 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonAPI', '0008_alter_order_status_alter_order_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.BooleanField(db_index=True, default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]