from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import serializers
from reviews.models import (Category, Comments, Genres, GenresTitle, Review,
                            Title)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug', )
        lookup_field = 'slug'


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('name', 'slug', )
        lookup_field = 'slug'


class GenresTitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = GenresTitle
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(), slug_field='slug', many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category')

    def validate_year(self, value):
        if value > timezone.now().year:
            raise ValidationError(
                'Год выпуска не может быть больше текущего')
        return value


class ReadTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    genre = GenresSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category', 'rating',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'author', 'text', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        if self.context.get('request').method == 'PATCH':
            return data
        if Review.objects.filter(
                title_id=self.context['view'].kwargs.get('title_id'),
                author=self.context.get('request').user).exists():
            raise serializers.ValidationError(
                'Нельзя оставлять отзыв дважды!')
        return data


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comments
