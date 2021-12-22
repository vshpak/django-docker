from rest_framework import serializers

from store.models import Publisher, Journal, Book, Article, Author


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ["id", "name", "address"]


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "first_name", "last_name"]


class ArticleSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(many=True, queryset=Author.objects.all())
    journal = serializers.PrimaryKeyRelatedField(queryset=Journal.objects.all())

    class Meta:
        model = Article
        fields = ["id", "name", "journal", "authors"]


class JournalSerializer(serializers.ModelSerializer):

    articles = ArticleSerializer(many=True, source='article_set', read_only=True)
    publisher = serializers.PrimaryKeyRelatedField(queryset=Publisher.objects.all())

    class Meta:
        model = Journal
        fields = ["id", "name", "publisher", "articles"]


class BookSerializer(serializers.ModelSerializer):

    authors = serializers.PrimaryKeyRelatedField(many=True, queryset=Author.objects.all())
    publisher = serializers.PrimaryKeyRelatedField(queryset=Publisher.objects.all())

    class Meta:
        model = Book
        fields = ["id", "name", "publisher", "authors"]
