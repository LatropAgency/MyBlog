# Generated by Django 3.0.3 on 2020-02-27 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20200228_0028'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('text', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
