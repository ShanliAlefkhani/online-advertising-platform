from django.shortcuts import render
from advertiser_management.models import Advertiser, Ad
from django.shortcuts import redirect


def index(request):
    advertisers = Advertiser.objects.all()
    for advertiser in advertisers:
        for ad in advertiser.ad_set.all():
            ad.views += 1
            ad.save()
    context = {'advertisers': advertisers}
    return render(request, 'ads.html', context)


def detail(request, object_id):
    ad = Ad.objects.get(id=object_id)
    ad.clicks += 1
    ad.save()
    return redirect(ad.link)
