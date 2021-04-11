from rest_framework import serializers
from advertiser_management.models import Advertiser, Ad, Click, View, ClicksAndViewsPerHour, ClicksAndViewsPerDay


class AdvertiserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertiser
        fields = '__all__'


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class ClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Click
        fields = '__all__'


class ViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = View
        fields = '__all__'


class ClicksAndViewsPerHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClicksAndViewsPerHour
        fields = '__all__'


class ClicksAndViewsPerDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClicksAndViewsPerDay
        fields = '__all__'
