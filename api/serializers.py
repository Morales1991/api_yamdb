from rest_framework import serializers

from library.models import Review, Comment, Title, Category, Genre
from .models import User


from django.utils.translation import ugettext_lazy as _


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'id', 'first_name', 'last_name', 'email', 'role', 'bio')
        model = User



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}
        model = Genre


class CategoryField(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = CategorySerializer(value)
        return serializer.data


class GenreField(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = GenreSerializer(value)
        return serializer.data


class TitleSerializer(serializers.ModelSerializer):
    category = CategoryField(slug_field='slug', queryset=Category.objects.all(), required=False)
    genre = GenreField(slug_field='slug', queryset=Genre.objects.all(), many=True)

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category',)
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'title', 'pub_date', 'author', 'score')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = '__all__'
        model = Comment
        