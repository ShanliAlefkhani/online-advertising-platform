from django.shortcuts import render
from django.urls import reverse
from advertiser_management.models import Advertiser, Ad, Click, View
from django.shortcuts import redirect
from .forms import AdForm
from datetime import datetime


def index_view(request):
    advertisers = Advertiser.objects.all()
    for advertiser in advertisers:
        for ad in advertiser.ad_set.all():
            View.objects.create(ad=ad, datetime=datetime.now(), ip="")
    context = {'advertisers': advertisers}
    return render(request, 'ads.html', context)


def detail_view(request, object_id):
    ad = Ad.objects.get(id=object_id)
    Click.objects.create(ad=ad, datetime=datetime.now(), ip="")
    return redirect(ad.link)


def ad_create_view(request):
    form = AdForm(request.POST or None)
    if form.is_valid():
        form.save()
    if request.method == 'GET':
        context = {'form': form}
        return render(request, 'ad_create.html', context)
    else:
        return redirect(reverse('index'))
