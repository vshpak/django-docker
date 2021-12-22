from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from store.models import Publisher, Journal, Book, Article
from store.serializers import (
    PublisherSerializer,
    JournalSerializer,
    BookSerializer,
    ArticleSerializer,
)


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer


class JournalViewSet(viewsets.ModelViewSet):
    queryset = Journal.objects.prefetch_related('article_set')
    serializer_class = JournalSerializer

    @action(detail=True)
    def articles(self, request, pk=None):
        article = Article.objects.filter(journal=self.kwargs["pk"])
        return Response(ArticleSerializer(article, many=True).data)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
