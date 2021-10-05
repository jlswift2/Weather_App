from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

# Create your models here.
class Location(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=200)

    class Meta:
        unique_together = ['user', 'name']

    @property
    def url(self):
        return reverse('home') + '?city=' + self.name

    def __str__(self):
        return self.name
