# Generated by Django 5.1 on 2024-09-19 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('amount', models.PositiveIntegerField()),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('category', models.CharField(choices=[('food', 'food'), ('travel', 'travel'), ('health', 'health'), ('other', 'other')], default='other', max_length=200)),
                ('user', models.CharField(max_length=200)),
            ],
        ),
    ]
