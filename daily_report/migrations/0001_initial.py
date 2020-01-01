


import datetime
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
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField(default=datetime.datetime.now, verbose_name='時間')),
                ('end_time', models.TimeField(default=datetime.datetime.now, verbose_name='時間')),
                ('memo', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'activity',
            },
        ),
        migrations.CreateModel(
            name='DailyReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime.now, verbose_name='日付')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'daily_report',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'employee',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('order_amount', models.IntegerField()),
                ('budget', models.IntegerField()),
                ('outsourcing_budget', models.IntegerField()),
                ('start_date', models.DateField(default=datetime.datetime.now, verbose_name='日付')),
                ('end_date', models.DateField(default=datetime.datetime.now, verbose_name='日付')),
                ('client', models.CharField(max_length=30)),
                ('outsourcing_cost', models.IntegerField()),
                ('employee', models.ManyToManyField(to='daily_report.Employee')),
            ],
            options={
                'db_table': 'project',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('wage', models.IntegerField()),
            ],
            options={
                'db_table': 'status',
            },
        ),
        migrations.AddField(
            model_name='employee',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='daily_report.Status'),
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activity',
            name='daily_report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='daily_report.DailyReport', verbose_name='project'),
        ),
        migrations.AddField(
            model_name='activity',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='daily_report.Project'),
        ),
        migrations.AlterUniqueTogether(
            name='dailyreport',
            unique_together={('date', 'user')},
        ),
    ]
