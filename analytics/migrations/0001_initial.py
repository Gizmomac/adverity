# Generated by Django 2.2.5 on 2019-09-08 05:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('clicks', models.IntegerField()),
                ('impressions', models.IntegerField(blank=True, null=True)),
                ('campaign', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='analytics.Campaign')),
                ('source', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='analytics.Source')),
            ],
        ),
    ]
