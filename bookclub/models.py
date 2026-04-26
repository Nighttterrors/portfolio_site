from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    birthday = models.DateField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to="covers/", null=True, blank=True)
    month = models.DateField() #Book of the month
    createdAt = models.DateTimeField(auto_now_add=True)

    def average_rating(self):
        return self.reviews.aggregate(models.Avg("rating"))["rating__avg"]

    def __str__(self):
        return f"{self.title} ({self.month})"
    


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("book", "user")  # one review per user per book

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
