from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('fiches', '0001_initial'),
    ]

    operations = [
        # 1️⃣ Supprime l’ancien champ participants (TextField)
        migrations.RemoveField(
            model_name='fichepage',
            name='participants',
        ),

        # 2️⃣ Ajoute owner et is_public
        # migrations.AddField(
        #     model_name='fichepage',
        #     name='owner',
        #     field=models.ForeignKey(
        #         settings.AUTH_USER_MODEL,
        #         null=True, blank=True,
        #         on_delete=models.SET_NULL,
        #         related_name='fiches_owned'
        #     ),
        # ),
        migrations.AddField(
            model_name='fichepage',
            name='is_public',
            field=models.BooleanField(
                default=False,
                help_text='Rendre la fiche visible à tous (ex: Wubuquan)'
            ),
        ),

        # 3️⃣ Ré-ajoute participants sous forme de M2M
        migrations.AddField(
            model_name='fichepage',
            name='participants',
            field=models.ManyToManyField(
                settings.AUTH_USER_MODEL,
                related_name='fiches_participées',
                blank=True
            ),
        ),
    ]
