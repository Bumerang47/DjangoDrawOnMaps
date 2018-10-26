from django.shortcuts import render
from django.apps import apps


def index(request):
    """
    Get index page
    @param request: HttpRequest
    @return:  render() / HttpResponse
    """

    Roads = apps.get_model('roads', 'Roads')

    far_road_list = Roads.objects.order_by('-length_km')[:3]
    context = {'far_road_list': far_road_list}
    return render(request, 'static/index.html', context)
