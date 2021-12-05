from django.urls import path, include
from rest_framework.routers import DefaultRouter
from pools.views import PublisherViewSet, JournalViewSet

router = DefaultRouter()
router.register('publishers', PublisherViewSet)
router.register('journals', JournalViewSet)

urlpatterns = [
    path('', include(router.urls))
]