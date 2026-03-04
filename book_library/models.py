from django.db import models
from django.conf import settings


class Book(models.Model):
    """Defines a book model"""
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    publication_year = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='books'
    )

    def __str__(self):
        """Returns a string representation of the book"""
        return self.title
