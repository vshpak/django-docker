from django.http import HttpResponseBadRequest
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from store.integrations.clients import increment_access_counter, StatisticClient
from store.models import Publisher, Journal, Book, Article
from store.serializers import PublisherSerializer, JournalSerializer, BookSerializer, ArticleSerializer


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

    # def get_queryset(self):
    #     return (
    #         Publisher.objects.all()
    #     )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        statistics_client = StatisticClient()
        # statistics_client.increment_access_counter(model_name='Publisher', object_id=instance.pk)
        # is_metric_sent_succeeded = increment_access_counter('Publisher', instance.pk)
        # if not is_metric_sent_succeeded:
        #     return HttpResponseBadRequest()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class JournalViewSet(viewsets.ModelViewSet):
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer

    @action(detail=True)
    def articles(self, request, pk=None):
        kw = self.kwargs['pk']
        article = Article.objects.filter(journal=kw)
        return Response(ArticleSerializer(article, many=True).data)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
