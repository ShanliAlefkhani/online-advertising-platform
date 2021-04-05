from django.db import models


class Advertiser(models.Model):
    name = models.CharField(max_length=100)


class Ad(models.Model):
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    img_url = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    approved = models.BooleanField(default=False)


class Click(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    ip = models.CharField(max_length=100)


class View(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    ip = models.CharField(max_length=100)
