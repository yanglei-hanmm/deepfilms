from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import View
from django_redis import get_redis_connection

from film.models import Film, FilmType, IndexFilmsBanner,IndexPromotionBanner


class IndexView(View):
    def get(self,request):
        # 尝试从缓存中获取数据
        context = cache.get('index_page_data')
        if context is None:
            types = FilmType.objects.all()
            for type in types:
                film = Film.objects.filter(film_type=type)
                type.film = film

            # 轮播电影
            films_banners = IndexFilmsBanner.objects.all().order_by('index')
            promotion_banners = IndexPromotionBanner.objects.all().order_by('index')
            context = {'types':types,'films_banners':films_banners,'promotion_banners':promotion_banners}

            # 设置缓存
            cache.set('index_page_data', context, 3600)

        # 获取用户收藏夹影片数量
        favorites_count = 0
        user = request.user
        if user.is_authenticated:
            conn = get_redis_connection('default')

            favorites_key = 'favorites_%d'% user.id
            favorites_count = conn.zcard(favorites_key)
        context.update(favorites_count=favorites_count)
        return render(request,'index.html',context)


# 影片详情
class DetailView(View):
    def get(self, request, film_id):
        try:
            film = Film.objects.get(id=film_id)
        except Film.DoesNotExist:
            # 影片不存在
            return redirect(reverse('film:index'))

        film_spu = -1 # -1表示SPU为空

        if film.spu is not None:
            film_spu = film.spu

        # 影片系列
        series_films = Film.objects.filter(spu=film_spu).exclude(id=film_id)

        # 新片推荐
        new_films = Film.objects.filter(film_region=film.film_region).exclude(id=film_id).order_by('-create_time')[:2]

        # 影片分类信息
        types = FilmType.objects.all()

        # 影片是否收藏
        # zrank favorites_1 film_id,返回下标，如果没有找到返回null
        is_collected = False
        user = request.user

        if user.is_authenticated:
            conn = get_redis_connection('default')
            favorites_id = 'favorites_%d' % user.id
            if conn.zrank(favorites_id,film_id):
                is_collected=True

        # print(user.id, film_id, type(user.id), type(film_id),is_collected)
        context = {'film':film,'types':types,'new_films':new_films,'series_films':series_films,'is_collected':is_collected }
        return render(request,'detail.html',context)

# 种类id 页码 排序方式(评分、热度)
# 影片列表/list/id/page?sort=排序
class ListView(View):
    def get(self,request,type_id,page):
        try:
            type = FilmType.objects.get(id=type_id)
        except FilmType.DoesNotExist:
            # 影片分类不存在
            return redirect(reverse('film:index'))
        # 排序default按照时间先后倒序,score按照评分高低,hot按照播放量高低
        sort = request.GET.get("sort")
        if sort=='score':
            films = Film.objects.filter(film_type=type).order_by('-score')
        elif sort=='hot':
            films = ''
        else:
            sort = 'default'
            films = Film.objects.filter(film_type=type).order_by('-create_time')



        # 影片分类信息
        types = FilmType.objects.all()

        # 数据分页
        paginator = Paginator(films,1)

        #获取第page页的内容
        try:
            page = int(page)
        except Exception as e:
            page = 1
        if page > paginator.num_pages :
            page = 1

        # 获取第page页的数据
        films_page = paginator.page(page)

        # 新片推荐
        new_films = Film.objects.filter(film_type=type).order_by('-create_time')[:2]


        context = {'type':type,'types':types,'films_page':films_page,'new_films':new_films,'sort':sort}
        return render(request,'list.html',context)