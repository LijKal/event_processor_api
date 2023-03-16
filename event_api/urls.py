from django.conf.urls import url
from . import views

urlpatterns =[url(r'^event/collect', views.collect_event, name='collect_event'), url(r'event/validate', views.validate_event, name='validate_event')]