from django.db import models
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=1000, blank=True)
    rating = models.IntegerField(blank=True, null=True)
    genre = models.ManyToManyField(Genre, verbose_name='Жанр')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Категория'
    )

    def update_rating(self):
        self.rating = self.reviews.all().aggregate(Avg('score'))['score__avg'] 
        self.save()


class Review(models.Model):
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    text = models.TextField()
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='reviews')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', blank=True)

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', blank=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField('Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text
