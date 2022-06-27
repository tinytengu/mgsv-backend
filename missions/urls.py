from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register("characters", CharacterViewSet, basename="characters")
router.register("missions", MissionViewSet, basename="missions")
router.register("objectives", ObjectiveViewSet, basename="objectives")
router.register("facts", FactViewSet, basename="facts")
router.register("dialogs", DialogViewSet, basename="dialogs")

urlpatterns = [path("", include(router.urls))]
