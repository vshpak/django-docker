from django.urls import path, include
from rest_framework.routers import DefaultRouter
from pools.views import PublisherViewSet, JournalViewSet, BookViewSet

router = DefaultRouter()
router.register('publishers', PublisherViewSet)
router.register('journals', JournalViewSet)
router.register('books', BookViewSet)

urlpatterns = [
    path('', include(router.urls))
]