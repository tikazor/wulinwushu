# utilisateurs/apps.py
from django.apps import AppConfig

class UtilisateursConfig(AppConfig):
    name = "utilisateurs"
    verbose_name = "Utilisateurs"

    def ready(self):
        import utilisateurs.signals
