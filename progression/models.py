from django.db import models
from django.conf import settings
from fiches.models import FichePage

class ValidationFiche(models.Model):
    fiche = models.ForeignKey(FichePage, on_delete=models.CASCADE, related_name="validations")
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    valide = models.BooleanField(default=True)
    date_validation = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("fiche", "utilisateur")

    def __str__(self):
        return f"{self.utilisateur} → {self.fiche.title} ({'✔' if self.valide else '✘'})"
    

