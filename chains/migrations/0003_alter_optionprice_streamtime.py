# Generated by Django 4.2.2 on 2023-07-02 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chains", "0002_alter_option_symbol"),
    ]

    operations = [
        migrations.AlterField(
            model_name="optionprice",
            name="streamtime",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
