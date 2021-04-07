from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from advertiser_management.models import Advertiser, Ad, Click, View as ViewModel
from django.shortcuts import redirect
from .forms import AdForm
from datetime import datetime
from django.views.generic import View
from django.views.generic.base import TemplateView, RedirectView


class IndexView(TemplateView):
    template_name = 'ads.html'

    def get_context_data(self, **kwargs):
        advertisers = Advertiser.objects.all()
        for advertiser in advertisers:
            for ad in advertiser.ad_set.all():
                ViewModel.objects.create(ad=ad, datetime=datetime.now(), ip="")
        context = {'advertisers': advertisers}
        return context


class DetailView(RedirectView):

    permanent = False
    query_string = True
    pattern_name = 'ad-detail'

    def get_redirect_url(self, *args, **kwargs):
        ad = get_object_or_404(Ad, id=kwargs['object_id'])
        Click.objects.create(ad=ad, datetime=datetime.now(), ip="")
        return ad.link


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


class RecordView(View):
    def get(self, request, *args, **kwargs):
        clicks = Click.objects.all()
        views = ViewModel.objects.all()
        context = []
        for time in range(24):
            info = {
                'time': time,
                'number_of_clicks': clicks.filter(datetime__hour=time).count(),
                'number_of_views': views.filter(datetime__hour=time).count()
            }
            context.append(info)
        return render(request, 'record.html', {'context': context})
