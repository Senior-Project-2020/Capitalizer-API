from django.db import models
from django.contrib.auth.models import AbstractUser

INTERESTS = [
    ('tech', 'Tech'), 
    ('real_estate','Real Estate'), 
    ('healthcare','Healthcare'),
]

class Interest(models.Model):
    interest = models.CharField(choices=INTERESTS, max_length=100)

    def __str__(self):
        return self.interest

    class Meta:
        ordering = ['interest']

class PCUser(AbstractUser):
    # Get interests from the Interest table
    interests = models.ManyToManyField(Interest)
