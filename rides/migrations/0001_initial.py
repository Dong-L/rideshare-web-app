# Generated by Django 2.2.5 on 2019-12-02 00:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('origin', models.CharField(max_length=50)),
                ('origin_state', models.CharField(default='N/A', max_length=50)),
                ('destination', models.CharField(max_length=50)),
                ('destination_state', models.CharField(default='N/A', max_length=50)),
                ('departure_date', models.DateField()),
                ('asking_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('seats_available', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=0)),
                ('created_rides', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_rides', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owner', to=settings.AUTH_USER_MODEL)),
                ('passenger_list', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=250, null=True)),
                ('hometown', models.CharField(blank=True, max_length=30, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=10)),
                ('car', models.CharField(blank=True, max_length=30, null=True)),
                ('rides', models.ManyToManyField(blank=True, db_index=True, to='rides.Ride')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
