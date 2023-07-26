# Generated by Django 4.2 on 2023-06-01 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('film', '0009_indexfilmsbanner'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndexPromotionBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('name', models.CharField(max_length=20, verbose_name='活动名称')),
                ('url', models.URLField(max_length=256, verbose_name='活动链接')),
                ('image', models.ImageField(upload_to='banner', verbose_name='活动图片')),
                ('index', models.SmallIntegerField(default=0, verbose_name='展示顺序')),
            ],
            options={
                'verbose_name': '首页促销活动',
                'verbose_name_plural': '首页促销活动',
                'db_table': 'df_ind_films_promotion',
            },
        ),
    ]