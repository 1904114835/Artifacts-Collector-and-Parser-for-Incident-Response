# Generated by Django 4.0.4 on 2022-08-03 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_host'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='amount',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='host',
            name='event_log',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='host',
            name='icon_cache',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='host',
            name='img_url',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='host',
            name='isActive',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='host',
            name='last24h',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='host',
            name='last24h_isIncrease',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='host',
            name='last7d',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='host',
            name='last7d_isIncrease',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='host',
            name='registry',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
