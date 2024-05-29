from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image


class Place(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='places/')  # Adjust based on your media settings
    is_popular = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # ... other fields like rating

    # ... any other methods you might need
class Destination(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=[('beach', 'Beach'), ('mountain', 'Mountain'), ('city', 'City'), ('historical', 'Historical'), ('food', 'Food'), ('drink', 'Drink')], blank=True)
    average_rating = models.FloatField(default=0.0)
    number_of_reviews = models.IntegerField(default=0)
    popularity_count = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images', blank=True, null=True)

    def __str__(self):
        return self.name

    def update_rating(self):
        reviews = self.reviews.all()
        total_rating = sum(review.rating for review in reviews)
        self.number_of_reviews = reviews.count()
        self.average_rating = total_rating / self.number_of_reviews if self.number_of_reviews > 0 else 0
        self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 500 or img.width > 500:
                output_size = (500, 500)
                img.thumbnail(output_size)
                img.save(self.image.path)




# media files are to be uploaded under MEDIA_ROOT/reviews
review_image_storage = FileSystemStorage(location=settings.MEDIA_ROOT, base_url='/media/')

class Review(models.Model):
    place = models.ForeignKey(Destination, related_name='reviews', on_delete=models.CASCADE)
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE, null=True)
    image = models.ImageField(storage=review_image_storage, upload_to='images', blank=True)
    title = models.CharField(max_length=200, blank=True)
    rating = models.IntegerField(default=1, choices=[(i, str(i)) for i in range(1, 6)])
    pros = models.TextField(blank=True)
    cons = models.TextField(blank=True)

    class Meta:
        unique_together = ('place', 'user')

    def __str__(self):
        return f'Review for {self.place.name} by {self.user.username}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.place.update_rating()

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    query = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.query