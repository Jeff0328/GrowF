# Generated by Django 2.1.1 on 2018-10-13 09:01

import api.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20181013_0212'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('value', models.DecimalField(decimal_places=2, max_digits=9)),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Stock', to_field='ticker')),
            ],
        ),
        migrations.AlterField(
            model_name='closing',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Stock', to_field='ticker'),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='name',
            field=models.CharField(max_length=70, validators=[api.models.validate_portfolio_name]),
        ),
    ]