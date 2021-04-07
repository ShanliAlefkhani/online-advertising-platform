from django.urls import path
from advertiser_management import views

urlpatterns = [
    path('index', views.IndexView.as_view(), name='index'),
    path('click/<int:object_id>/', views.DetailView.as_view(), name='detail'),
    path('ad_create', views.AdCreateView.as_view(), name='ad_create'),
    path('record', views.RecordView.as_view(), name='record')
]
