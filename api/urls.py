from django.conf.urls import url

from api import views

urlpatterns = [
    url(r'^vessels$', views.VesselListView.as_view(),
        name=views.VesselListView.view_name),

    url(r'^vessels/(?P<code>[A-Za-z0-9]+)$',
        views.VesselDetailView.as_view(),
        name=views.VesselDetailView.view_name),

    url(r'^vessels/(?P<vessel_code>[A-Za-z0-9]+)/equipments$',
        views.EquipmentListView.as_view(),
        name=views.EquipmentListView.view_name),

    url(r'^vessels/(?P<vessel_code>[A-Za-z0-9]+)/equipments/(?P<code>[A-Za-z0-9]+)$',
        views.EquipmentDetailView.as_view(),
        name=views.EquipmentDetailView.view_name),

    url(r'^equipments/activate$',
        views.EquipmentActivateView.as_view(),
        name=views.EquipmentActivateView.view_name),

    url(r'^equipments/inactivate$',
        views.EquipmentInactivateView.as_view(),
        name=views.EquipmentInactivateView.view_name),

]
