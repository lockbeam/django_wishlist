# Generated by Django 5.0.3 on 2024-03-27 20:09

from django.db import migrations, models

# migration is a set of instruction for how to create a database table
# or modidy a table that already exists

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('visited', models.BooleanField(default=False)),
            ],
        ),
    ]
