# Generated by Django 4.2.2 on 2023-07-02 08:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=30, null=True, unique=True)),
                ('expiration', models.DateField()),
                ('strike_price', models.FloatField(default=0.0)),
                ('option_type', models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='OptionPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ltp', models.FloatField(default=0.0)),
                ('ltq', models.PositiveIntegerField(default=0)),
                ('volume', models.PositiveIntegerField(default=0)),
                ('bid_price', models.FloatField(default=0.0)),
                ('bid_qty', models.PositiveIntegerField(default=0)),
                ('ask_price', models.FloatField(default=0.0)),
                ('ask_qty', models.PositiveIntegerField(default=0)),
                ('oi', models.PositiveIntegerField(default=0)),
                ('prev_close', models.FloatField(default=0.0)),
                ('prev_oi', models.PositiveIntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('streamtime', models.DateTimeField()),
                ('option', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chains.option')),
            ],
        ),
    ]