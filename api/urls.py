from django.conf.urls import url

from api import views

urlpatterns = [
    url(r'^vessels$', views.VesselListView.as_view(), name=views.VesselListView.view_name),
    url(r'^vessels/(?P<code>[A-Za-z0-9]+)$', views.VesselDetailView.as_view(), name=views.VesselDetailView.view_name),
]