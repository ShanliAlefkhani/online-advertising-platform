from django.shortcuts import render
from django.urls import reverse

from advertiser_management.models import Advertiser, Ad
from django.shortcuts import redirect
from .forms import AdForm


def index_view(request):
    advertisers = Advertiser.objects.all()
    for advertiser in advertisers:
        for ad in advertiser.ad_set.all():
            ad.views += 1
            ad.save()
    context = {'advertisers': advertisers}
    return render(request, 'ads.html', context)


def detail_view(request, object_id):
    ad = Ad.objects.get(id=object_id)
    ad.clicks += 1
    ad.save()
    return redirect(ad.link)


def ad_create_view(request):
    form = AdForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {'form': form}
    if request.method == 'GET':
        return render(request, 'ad_create.html', context)
    if request.method == 'POST':
        return redirect(reverse('index'))
