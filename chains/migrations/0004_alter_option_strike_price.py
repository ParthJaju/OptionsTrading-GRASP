# Generated by Django 4.2.2 on 2023-07-03 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chains", "0003_alter_optionprice_streamtime"),
    ]

    operations = [
        migrations.AlterField(
            model_name="option",
            name="strike_price",
            field=models.PositiveIntegerField(default=0),
        ),
    ]