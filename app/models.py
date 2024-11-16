from django.db import models

# Create your models here.
class Author(models.Model):
    name=models.CharField(max_length=150, unique=True)
    profile_picture=models.ImageField(
        upload_to='profile_pictures',
        blank=True,
        null=True
    )

class Message(models.Model):
    author=models.ForeignKey(Author, on_delete=models.CASCADE)
    content=models.TextField()
    create_at=models.DateTimeField(auto_now_add=True)