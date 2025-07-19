# utilisateurs/models.py
from django.conf import settings
from django.db import models

class Profile(models.Model):
    ROLE_CHOICES = [
        ('pratiquant', 'Pratiquant'),
        ('animateur',  'Animateur'),
        ('admin',      'Administrateur'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='pratiquant'
    )

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
