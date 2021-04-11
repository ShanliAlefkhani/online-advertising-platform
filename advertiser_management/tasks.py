from celery import shared_task
from django.db.models import Sum

from advertiser_management.models import ClicksAndViewsPerHour, Click, View, ClicksAndViewsPerDay
from django.utils import timezone


@shared_task
def save_clicks_and_views_per_hour():
    clicks = Click.objects.all()
    views = View.objects.all()
    ClicksAndViewsPerHour.objects.create(clicks_count=clicks.filter(
        datetime__gte=timezone.now()-timezone.timedelta(hours=1)).count(),
                                         views_count=views.filter(
                                             datetime__gte=timezone.now()-timezone.timedelta(hours=1)).count(),
                                         datetime=timezone.now())


@shared_task
def save_clicks_and_views_per_day():
    data = ClicksAndViewsPerHour.objects.filter(datetime__gte=timezone.now()-timezone.timedelta(days=1)).aggregate(
        clicks_count=Sum('clicks_count'), views_count=Sum('views_count')
    )

    ClicksAndViewsPerDay.objects.create(clicks_count=data['clicks_count'],
                                        views_count=data['views_count'], date=timezone.now())
