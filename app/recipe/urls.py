from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

# /api/recipe/tags/1/
# DefaultRouter: it automatically registers the appropriate URLs for all of the actions in our viewset.
router = DefaultRouter()
router.register('tags', views.TagViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]

