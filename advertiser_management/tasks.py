from celery import shared_task
from advertiser_management.models import ClicksAndViewsPerHour, Click, View
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
