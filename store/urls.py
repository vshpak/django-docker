from django.urls import path, include
from rest_framework.routers import DefaultRouter
from store.views import PublisherViewSet, JournalViewSet, BookViewSet, ArticleViewSet

router = DefaultRouter() #trailing_slash=False
router.register('publishers', PublisherViewSet)
router.register('journals', JournalViewSet)
router.register('books', BookViewSet)
router.register('articles', ArticleViewSet)


urlpatterns = [
    path('', include(router.urls))
]