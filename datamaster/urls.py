from django.urls import include, path
from rest_framework.routers import DefaultRouter

from datamaster import views

router = DefaultRouter()
router.register("desa", views.DesaViewSet)

urlpatterns = [path("", include(router.urls))]
