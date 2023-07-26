import os

from django.conf import settings
from django.template import loader,RequestContext
from celery import Celery

# worker端需要打开注释，启用django环境
# import os
# import django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE','deepfilms.settings')
# django.setup()

from film.models import Film, FilmType, IndexFilmsBanner
# 创建Celery实例对象
app = Celery('celery_tasks.tasks',broker='redis://172.30.2.250:6379/7')

@app.task
def generate_static_index_html():
    types = FilmType.objects.all()
    for type in types:
        film = Film.objects.filter(film_type=type)
        type.film = film

    # 轮播电影
    films_banners = IndexFilmsBanner.objects.all().order_by('index')
    context = {'types': types, 'films_banners': films_banners}

    # 1 加载模板文件,
    temp = loader.get_template('static_index.html')
    # 2 模板渲染
    static_index_html = temp.render(context)
    # 3 生成静态文件
    save_path = os.path.join(settings.BASE_DIR,'film/static/index.html')

    with open(save_path,'w') as f:
        f.write(static_index_html)