from django.db import models


class Advertiser(models.Model):
    name = models.CharField(max_length=100)


class Ad(models.Model):
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE)
    clicks = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=100)
    img_url = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
