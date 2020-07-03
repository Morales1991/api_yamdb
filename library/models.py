from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()

class Title(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="titles")
    text = models.TextField()
    rating = models.IntegerField(default=None)

class Review(models.Model):
    scores = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10)
    )
    text = models.TextField()
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name="reviews")
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    score = models.IntegerField(choices=scores)#max_value=10, min_value=1)
    
    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created = models.DateTimeField("Дата добавления", auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text
        