# Generated by Django 4.2 on 2023-06-01 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('film', '0010_indexpromotionbanner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indexpromotionbanner',
            name='url',
            field=models.CharField(max_length=256, verbose_name='活动链接'),
        ),
    ]