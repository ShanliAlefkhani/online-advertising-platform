from django import forms

from .models import Ad


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = [
            'advertiser',
            'title',
            'img_url',
            'link'
        ]
