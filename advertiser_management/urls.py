from django.urls import path
from advertiser_management import views

urlpatterns = [
    path('index', views.index_view, name='index'),
    path('click/<int:object_id>/', views.detail_view, name='detail'),
    path('create_ad', views.ad_create_view, name='ad_create')
]
