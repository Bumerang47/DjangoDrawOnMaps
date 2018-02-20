# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from models import Roads, Azs
from django.http import JsonResponse
from django.core import serializers


def roads_list(request):
    """
    Returns Json list of all roads
    @param request: HttpRequest
    @return:  Full list roads at json
    """

    if request.method == "GET":
        fields = ('road_code', 'geomtype', 'coordinates', 'name', 'length_km')
        list_roads = Roads.objects.all()
        data = serializers.serialize('json_road', list_roads, fields=fields)
        return JsonResponse(data, safe=False)

    return JsonResponse({'message': 'error request'}, status=500)


def get_azs(request, road_code):
    """
    Returns json list Azs at code of road
    @param request: HttpRequest
    @param road_code: code for find Azs from road
    @return: List Azs at json
    """

    if request.method == "GET":
        fields = ('road_code', 'geomtype', 'coordinates')
        list_azs = Azs.objects.filter(road_code_id__road_code=road_code)
        if list_azs.count() > 0:
            data = serializers.serialize('json_road', list_azs, fields=fields)
            return JsonResponse(data, safe=False)
        return JsonResponse([], safe=False)
    return JsonResponse({'message': 'error request'}, status=500)


def get_road(request, road_code):
    """
    Returns json object of road at code
    @param request: HttpRequest
    @param road_code: code for find road
    @return: road at json
    """

    try:
        road = Roads.objects.get(road_code=road_code)
        fields = ('road_code','name','length_km','geomtype','coordinates')
        data = serializers.serialize('json_road', [road], fields=fields)
        return JsonResponse(data, safe=False)
    except Roads.DoesNotExist:
        return JsonResponse({'message': 'error request'}, status=500)
