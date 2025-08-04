# fiches/migrations/0003_remove_fichepage_owner_alter_fichepage_animateurs.py

from django.db import migrations, models
from django.conf import settings

class Migration(migrations.Migration):

    dependencies = [
        ('fiches', '0002_update_fichepage_fields'),
    ]

    operations = [
        # Suppression de la suppression de 'owner' (déjà retiré)
        # migrations.RemoveField(
        #     model_name='fichepage',
        #     name='owner',
        # ),
        # Conserver uniquement la modification d'animateurs si nécessaire :
        migrations.AlterField(
            model_name='fichepage',
            name='animateurs',
            field=models.ManyToManyField(
                related_name='fiches_animateur',
                to=settings.AUTH_USER_MODEL,
                blank=True  # si vous aviez ajouté blank=True
            ),
        ),
    ]
