from django.shortcuts import render
from django.urls import reverse
from advertiser_management.models import Advertiser, Ad, Click, View as ViewModel, ClicksAndViewsPerHour
from django.shortcuts import redirect
from datetime import datetime
from django.views.generic import View
from rest_framework import generics
from .serializers import AdSerializer, AdvertiserSerializer, ClicksAndViewsPerHourSerializer


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

        sorted_clicks_views = sorted(clicks_views, key=lambda i: i['number'], reverse=True)

        sum_of_time = 0
        print(sum_of_time)
        for click in Click.objects.all():
            sum_of_time += click.datetime.minute - ViewModel.objects.filter(ip=click.ip).first().datetime.minute
        average = 0
        if Click.objects.all().count() != 0:
            average = sum_of_time / Click.objects.all().count()
        total_clicks_views = 0
        if total_views != 0:
            total_clicks_views = (total_clicks / total_views).__round__(2)
        return render(request, 'record.html',
                      {'total_clicks_views': total_clicks_views,
                       'clicks_views': sorted_clicks_views,
                       'average': average
                       })


class ClicksAndViewsPerHourView(generics.ListAPIView):
    serializer_class = ClicksAndViewsPerHourSerializer

    def get_queryset(self):
        clicks = Click.objects.all()
        views = ViewModel.objects.all()

        for time in range(24):
            if ClicksAndViewsPerHour.objects.count() == 24:
                print(views.filter(datetime__hour=time+1).count())
                clicks_and_views_per_hour = ClicksAndViewsPerHour.objects.filter(time=time+1).first()
                clicks_and_views_per_hour.clicks_count = clicks.filter(datetime__hour=time+1).count()
                clicks_and_views_per_hour.views_count = views.filter(datetime__hour=time+1).count()
                clicks_and_views_per_hour.save()
            else:
                print("salam")
                ClicksAndViewsPerHour.objects.create(clicks_count=clicks.filter(datetime__hour=time+1).count(),
                                                     views_count=views.filter(datetime__hour=time+1).count(),
                                                     time=time+1)

        queryset = ClicksAndViewsPerHour.objects.all()
        return queryset
