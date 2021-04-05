from django.contrib import admin
from advertiser_management.models import Advertiser, Ad


class AdAdmin(admin.ModelAdmin):
    list_filter = ('approved',)
    search_fields = ('title',)


admin.site.register(Advertiser)
admin.site.register(Ad, AdAdmin)
