from rest_framework import serializers

from pools.models import Publisher, Journal, Article, Book


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'address', 'journal_name']


class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = ['id', 'name', 'article_set']
        # fields = ['id', 'question_text', 'choices']

    # choices = ChoiceSerializer(many=True, read_only=True, source='choice_set')


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'name']


# class BookSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Book
#         fields = ['id', 'question', 'choice_text', 'count']
#
#
