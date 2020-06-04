from django.db import models

INTERESTS = [
    ('int1','int1'), 
    ('int2','int2'), 
    ('int3','int3')
]

class UserInfo(models.Model):
    email = models.EmailField()
    interests = models.CharField(choices=INTERESTS, max_length=100)

    class Meta:
        ordering = ['email']
        verbose_name = 'User Info'
        verbose_name_plural = 'User Info'
