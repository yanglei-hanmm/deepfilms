from django.db import models


# Create your models here.

# 电影表
from db.base_model import BaseModel


class Film(BaseModel):
    name = models.CharField(verbose_name='电影名称', max_length=100)
    spu = models.ForeignKey('FilmSPU',verbose_name='影片SPU',blank=True, null=True, on_delete=models.SET_NULL)
    score = models.DecimalField(max_digits=10, decimal_places=1, verbose_name='评分')
    director = models.CharField(verbose_name='导演', max_length=100)
    actor = models.CharField(verbose_name='主要演员', max_length=2000)
    production = models.CharField(verbose_name='制片国家或地区', max_length=100)
    year = models.CharField(verbose_name='年代', max_length=10)
    description = models.CharField(verbose_name='简介', max_length=2000)
    film_type = models.ManyToManyField('FilmType', verbose_name='电影类型')
    film_region = models.ForeignKey('FilmRegion', verbose_name='地区',blank=True, null=True, on_delete=models.SET_NULL)  # 如欧美、日韩等
    poster = models.ImageField(verbose_name='电影海报', upload_to='film')
    view_count = models.PositiveIntegerField(verbose_name='影片播放数',default=0)
    video = models.FileField(verbose_name='片源', upload_to='video',default=None)

    class Meta:
        verbose_name = '影片'
        verbose_name_plural = verbose_name
        db_table = 'df_film'


# 影片类型表
class FilmType(BaseModel):
    name = models.CharField(verbose_name='种类名称', max_length=20)

    class Meta:
        verbose_name = '影片类型'
        verbose_name_plural = verbose_name
        db_table = 'df_film_type'


# 影片发行地区表
class FilmRegion(BaseModel):
    name = models.CharField(verbose_name='地区', max_length=20)

    class Meta:
        verbose_name = '影片发行地区'
        verbose_name_plural = verbose_name
        db_table = 'df_film_region'

# 影片类型SPU,如蚁人1-3属于一类
class FilmSPU(BaseModel):
    name = models.CharField(verbose_name='名称', max_length=100)

    class Meta:
        verbose_name = '影片SPU'
        verbose_name_plural = verbose_name
        db_table = 'df_film_spu'

# 轮播电影列表
class IndexFilmsBanner(BaseModel):
    film = models.ForeignKey('Film',verbose_name='电影名称',max_length=100,on_delete=models.CASCADE  )
    poster = models.ImageField(verbose_name='电影海报', upload_to='banner')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')  # 0 1 2 3

    class Meta:
        verbose_name = '首页轮播影片'
        verbose_name_plural = verbose_name
        db_table = 'df_ind_films_banner'

class IndexPromotionBanner(BaseModel):
    '''首页促销活动模型类'''
    name = models.CharField(max_length=20, verbose_name='活动名称')
    url = models.CharField(max_length=256, verbose_name='活动链接')
    image = models.ImageField(upload_to='banner', verbose_name='活动图片')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'df_ind_films_promotion'
        verbose_name = "首页促销活动"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name