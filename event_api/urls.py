from django.urls import path
from . import views

urlpatterns =[path('event/collect', views.collect_event, name='collect_event'), 
path('event/validate', views.validate_event, name='validate_event')]