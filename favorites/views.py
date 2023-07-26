import time

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import View

# /favorites/add
from django_redis import get_redis_connection

from film.models import Film


class FavoritesAddView(View):
    '''影片收藏记录添加'''
    def post(self,request):
        # 数据接收
        film_id = request.POST.get('film_id')

        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res':0,'errmsg':'用户未登录'})
        # 数据验证
        if not all([film_id]):
            return JsonResponse({'res':1,'errmsg':'数据不完整'})

        try:
            Film.objects.get(id=film_id)
        except Film.DoesNotExist:
            return JsonResponse({'res':2,'errmsg':'未找到该影片'})

        # 业务处理 添加到收藏
        conn = get_redis_connection('default')
        favorites_id = 'favorites_%d'% user.id
        k_score = round(time.time())
        conn.zadd(favorites_id,{film_id:k_score})

        # zadd favorites_3 2 two
        # zrange favorites_3 0 -1 withscores

        return JsonResponse({'res':3,'msg':'影片完成添加'})

class FavoritesRemoveView(View):
    '''影片收藏记录添加'''
    def post(self,request):
        # 数据接收
        film_id = request.POST.get('film_id')

        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res':0,'errmsg':'用户未登录'})
        # 数据验证
        if not all([film_id]):
            return JsonResponse({'res':1,'errmsg':'数据不完整'})

        try:
            Film.objects.get(id=film_id)
        except Film.DoesNotExist:
            return JsonResponse({'res':2,'errmsg':'未找到该影片'})

        # 业务处理 添加到收藏
        conn = get_redis_connection('default')
        favorites_id = 'favorites_%d'% user.id
        conn.zrem(favorites_id,film_id)

        # zadd favorites_3 2 two
        # zrange favorites_3 0 -1 withscores

        return JsonResponse({'res':3,'msg':'影片已移除'})
