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
    ip = models.GenericIPAddressField()


class View(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    ip = models.GenericIPAddressField()


class Summary(models.Model):
    clicks_count = models.PositiveIntegerField()
    views_count = models.PositiveIntegerField()

    class Meta:
        abstract = True


class ClicksAndViewsPerHour(Summary):
    datetime = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.datetime = self.datetime.replace(minute=0, second=0, microsecond=0)
        super(ClicksAndViewsPerHour, self).save(*args, **kwargs)


class ClicksAndViewsPerDay(Summary):
    date = models.DateField()
