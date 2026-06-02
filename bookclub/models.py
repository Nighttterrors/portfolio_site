from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    birthday = models.DateField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    isApproved = models.BooleanField(default=False)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return self.user.username


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to="covers/", null=True, blank=True)
    month = models.DateField() #Book of the month
    createdAt = models.DateTimeField(auto_now_add=True)
    is_current = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_current:
            Book.objects.filter(
                is_current=True
            ).exclude(
                pk=self.pk
            ).update(is_current=False)

        super().save(*args, **kwargs)

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



class DiscussionPost(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="posts"
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )



class Reply(models.Model):

    post = models.ForeignKey(
        DiscussionPost,
        on_delete=models.CASCADE,
        related_name="replies"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class PostLike(models.Model):

    post = models.ForeignKey(
        DiscussionPost,
        on_delete=models.CASCADE,
        related_name="likes"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            'post',
            'user'
        )
    @property
    def like_count(self):
        return self.likes.count()
    
    @property
    def reply_count(self):
        return self.replies.count()