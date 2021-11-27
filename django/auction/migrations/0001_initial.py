# Generated by Django 3.2.9 on 2021-11-27 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp_id', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('bidders', models.ManyToManyField(related_name='bid_items', to='auction.Player')),
                ('reg_player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reg_items', to='auction.player')),
            ],
        ),
    ]
