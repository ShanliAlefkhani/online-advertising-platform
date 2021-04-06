from django.shortcuts import render
from django.urls import reverse
from advertiser_management.models import Advertiser, Ad, Click, View as ViewModel
from django.shortcuts import redirect
from .forms import AdForm
from datetime import datetime
from django.views.generic import View


class IndexView(View):
    def get(self, request, *args, **kwargs):
        advertisers = Advertiser.objects.all()
        for advertiser in advertisers:
            for ad in advertiser.ad_set.all():
                ViewModel.objects.create(ad=ad, datetime=datetime.now(), ip="")
        context = {'advertisers': advertisers}
        return render(request, 'ads.html', context)


class DetailView(View):
    def get(self, request, object_id, *args, **kwargs):
        ad = Ad.objects.get(id=object_id)
        Click.objects.create(ad=ad, datetime=datetime.now(), ip="")
        return redirect(ad.link)


class AdCreateView(View):
    def get(self, request, *args, **kwargs):
        form = AdForm()
        context = {'form': form}
        return render(request, 'ad_create.html', context)

    def post(self, request, *args, **kwargs):
        form = AdForm(request.POST or None)
        if form.is_valid():
            form.save()
        return redirect(reverse('index'))
