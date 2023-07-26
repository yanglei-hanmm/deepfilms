from django.contrib import admin

# Register your models here.
from django.core.cache import cache

from film.models import Film, FilmType, FilmRegion,FilmSPU,IndexFilmsBanner,IndexPromotionBanner

class IndexFilmsBannerAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        '''新增或更新表中的数据时调用'''
        super().save_model(request,obj,form,change)

        # 发出任务让Celery worker重新生成首页静态页面
        from celery_tasks.tasks import generate_static_index_html
        generate_static_index_html.delay()

        # 清除首页的缓存数据
        cache.delete('index_page_data')

    def delete_model(self, request, obj):
        '''删除表中的数据时调用'''
        super().delete_model(request,obj)

        # 发出任务让Celery worker重新生成首页静态页面
        from celery_tasks.tasks import generate_static_index_html
        generate_static_index_html.delay()

        # 清除首页的缓存数据
        cache.delete('index_page_data')

admin.site.register(Film)
admin.site.register(FilmType)
admin.site.register(FilmRegion)
admin.site.register(FilmSPU)
admin.site.register(IndexPromotionBanner)
admin.site.register(IndexFilmsBanner,IndexFilmsBannerAdmin)