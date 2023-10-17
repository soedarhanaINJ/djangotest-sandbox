from django.urls import path

from core import views

urlpatterns = [path("q-status/<str:identifier>/", views.QStatusView.as_view())]
