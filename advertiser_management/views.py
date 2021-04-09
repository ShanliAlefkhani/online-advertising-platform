from django.shortcuts import render
from django.urls import reverse
from advertiser_management.models import Advertiser, Ad, Click, View as ViewModel
from django.shortcuts import redirect
from datetime import datetime
from django.views.generic import View
from rest_framework import generics
from .serializers import AdSerializer, AdvertiserSerializer

from django.shortcuts import HttpResponse

from .tasks import celery_task


def celery_view(request):
    for counter in range(2):
        celery_task.delay(counter)
    return HttpResponse("FINISH PAGE LOAD")


class IndexView(generics.ListAPIView):
    queryset = Advertiser.objects.all()
    serializer_class = AdvertiserSerializer

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        advertisers = Advertiser.objects.all()
        for advertiser in advertisers:
            for ad in advertiser.ad_set.all():
                ViewModel.objects.create(ad=ad, datetime=datetime.now(), ip=request.ip)
        return self.list(request, *args, **kwargs)


class DetailView(View):
    def get(self, request, object_id, *args, **kwargs):
        ad = Ad.objects.get(id=object_id)
        Click.objects.create(ad=ad, datetime=datetime.now(), ip=request.ip)
        return redirect(ad.link)


class AdCreateView(generics.CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)
        return redirect(reverse('index'))


class RecordView(View):
    def get(self, request, *args, **kwargs):
        clicks = Click.objects.all()
        views = ViewModel.objects.all()
        context = []
        total_clicks = 0
        total_views = 0
        clicks_views = []

        for time in range(24):
            clicks_count = clicks.filter(datetime__hour=time).count()
            views_count = views.filter(datetime__hour=time).count()
            total_clicks += clicks_count
            total_views += views_count
            number = 0
            if views_count != 0:
                number = (clicks_count / views_count).__round__(2)

            clicks_views.append({
                'time': time,
                'number': number
            })

            info = {
                'time': time,
                'number_of_clicks': clicks_count,
                'number_of_views': views_count

            }
            context.append(info)

        sorted_clicks_views = sorted(clicks_views, key=lambda i: i['number'], reverse=True)

        sum_of_time = 0
        print(sum_of_time)
        for click in Click.objects.all():
            sum_of_time += click.datetime.minute - ViewModel.objects.filter(ip=click.ip).first().datetime.minute
        average = sum_of_time / Click.objects.all().count()

        return render(request, 'record.html',
                      {'context': context,
                       'total_clicks_views': (total_clicks / total_views).__round__(2),
                       'clicks_views': sorted_clicks_views,
                       'average': average
                       })
