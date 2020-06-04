from django.db import models

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

class UserInfo(models.Model):
    email = models.EmailField()
    # Get interests from the Interest table
    interests = models.ManyToManyField(Interest)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['email']
        verbose_name = 'User Info'
        verbose_name_plural = 'User Info'
