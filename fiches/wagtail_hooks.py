from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import Technique, Atelier, Sequence, Materiel
from wagtail import hooks
from utilisateurs.permissions import (    can_view_atelier,    can_view_sequence,    can_view_fiche,
)
from django.urls import path
from . import views  # ou views si tu ajoutes dans views.py
from django.db import models


# fiches/wagtail_hooks.py
from django.templatetags.static import static
from django.utils.html import format_html
from wagtail.admin.menu import MenuItem
from django.urls import reverse

@hooks.register('insert_global_admin_css')
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static('css/wagtail_admin_custom.css'))


@hooks.register('insert_global_admin_html_head')
def add_favicon():
    return """
      <link rel="icon" href="/static/favicon.png" type="image/png">
      <link rel="shortcut icon" href="/static/favicon.ico" type="image/x-icon">
    """
    
@hooks.register('construct_main_menu')
def custom_menu(request, menu_items):
    # Exemple simplifié sans le menu qui cause l'erreur :
    menu_items[:] = [item for item in menu_items if item.name not in ['snippets', 'explorer']]
    if request.user.is_superuser or hasattr(request.user, "profile") and request.user.profile.role in ["animateur", "admin"]:
        menu_items.insert(0, MenuItem('Tableau de bord', reverse('wagtailadmin_home'), icon_name='site'))
    # Menu Statistiques : à ajouter plus tard, quand la vue/statistics sera créée


@hooks.register('construct_main_menu')
def custom_main_menu(request, menu_items):
    # Masquer les items "Snippets" et "Explorer" pour tous sauf superuser
    menu_items[:] = [item for item in menu_items if item.name not in ['snippets', 'explorer']]

    # Détection du rôle utilisateur (avec fallback)
    role = getattr(getattr(request.user, "profile", None), "role", None)
    is_admin = request.user.is_superuser or role == "admin"
    is_animateur = role == "animateur"

    # Ajoute "Tableau de bord" en tout premier (pointant vers l'accueil admin)
    menu_items.insert(0, MenuItem(
        'Tableau de bord',
        reverse('wagtailadmin_home'),
        icon_name='site',
        order=10,
    ))

    # Exemples d’ajout de menus selon le rôle
    if is_admin or is_animateur:
        # Exemples : Ajout menu Suivi global ou autres pages personnalisées
        menu_items.insert(1, MenuItem(
            'Suivi global',
            '/admin/suivi-global/',   # À personnaliser si besoin
            icon_name='group',
            order=20,
        ))
        # À activer plus tard si une vue "Statistiques" existe
        # menu_items.insert(2, MenuItem(
        #    'Statistiques',
        #    reverse('admin_stats'),  # Ne pas utiliser tant que la vue n’existe pas
        #    icon_name='order',
        #    order=30,
        # ))

    # Pour les pratiquants : menu minimal (pas d’ajout spécifique ici, adapter si besoin)

    # Possibilité d’ajouter un badge de rôle (cf. template navbar/user info si souhaité)



@hooks.register('register_admin_view')
def register_custom_dashboard():
    return path('admin/', views.dashboard_admin, name='wagtailadmin_home')




# ----------------------------
# Technique
# ----------------------------
class TechniqueAdmin(ModelAdmin):
    model = Technique
    menu_label = "Techniques"
    menu_icon = "list-ul"
    list_display = ("nom", "style", "zone")
    search_fields = ("nom", "style", "zone")

    # → Si vous voulez restreindre l’accès aux techniques, 
    #   implémentez ici can_view_technique()
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs  # tous publics ou à enrichir via can_view_technique

modeladmin_register(TechniqueAdmin)




class MaterielAdmin(ModelAdmin):
    model = Materiel
    menu_label = "Matériels"
    menu_icon = "list-ul"
    add_to_settings_menu = False
    list_display = ('nom',)
    search_fields = ('nom',)

modeladmin_register(MaterielAdmin)


# ----------------------------
# Séquence
# ----------------------------
class SequenceAdmin(ModelAdmin):
    model = Sequence
    menu_label = "Séquences"
    menu_icon = "folder-open-inverse"
    list_display = ("titre", "type_sequence")
    search_fields = ("titre",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        allowed_ids = [obj.pk for obj in qs if can_view_sequence(request.user, obj)]
        return qs.filter(pk__in=allowed_ids)

modeladmin_register(SequenceAdmin)


# ----------------------------
# Hooks Wagtail
# ----------------------------
@hooks.register('construct_site_summary_items')
def filter_fiches(request, items):
    """
    Filtrer les fiches du site summary en fonction de la permission can_view_fiche.
    """
    return [item for item in items if can_view_fiche(request.user, item.instance)]


@hooks.register('construct_page_listing_query')
def restrict_fiches_to_animateurs_or_public(request, pages, parent_page):
    """
    Restriction de l'interface admin Wagtail :
    Seules les fiches publiques ou animées par l'utilisateur sont visibles.
    """
    from fiches.models import FichePage

    if request.user.is_superuser:
        return pages  # Accès total

    # Si la page listée est une FichePage
    if parent_page.specific_class == FichePage:
        return pages.filter(
            models.Q(is_public=True) |
            models.Q(animateurs__in=[request.user])
        ).distinct()

    # Pour les autres types de pages, fallback au comportement par défaut : owner
    return pages.filter(owner=request.user)

# ----------------------------
# Atelier
# ----------------------------
class AtelierAdmin(ModelAdmin):
    model = Atelier
    menu_label = "Ateliers"
    menu_icon = "form"
    list_display = ("__str__", "duree", "techniques_list")
    search_fields = ("technique__nom", "consigne")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # on ne garde que les ateliers autorisés
        allowed_ids = [obj.pk for obj in qs if can_view_atelier(request.user, obj)]
        return qs.filter(pk__in=allowed_ids)

    def techniques_list(self, obj):
        return ", ".join(t.nom for t in obj.techniques.all())
    techniques_list.short_description = "Techniques"

modeladmin_register(AtelierAdmin)

@hooks.register('insert_editor_js')
def custom_multiselect_js():
    return """
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('select[multiple]').forEach(function(select) {
            if (
                select.style.display === 'none' ||
                select.classList.contains('js-checkboxified') ||
                select.parentNode.querySelectorAll('.custom-multiselect-container').length > 0 ||
                select.closest('.object-multiselect-checkboxes')
            ) {
                return;
            }
            select.classList.add('js-checkboxified');

            // Conteneur principal
            let container = document.createElement('div');
            container.className = 'custom-multiselect-container w-full p-2 bg-gray-50 border rounded';
            // Champ recherche
            let search = document.createElement('input');
            search.type = 'search';
            search.placeholder = 'Filtrer...';
            search.className = 'mb-2 px-2 py-1 border border-gray-300 rounded w-full';
            container.appendChild(search);

            // Grille de cases à cocher
            let grid = document.createElement('div');
            grid.className = 'grid grid-cols-2 gap-2';
            container.appendChild(grid);

            // Ajoute toutes les options initiales
            Array.from(select.options).forEach(function(opt) {
                let label = document.createElement('label');
                label.className = 'flex items-center gap-2';
                let checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.value = opt.value;
                checkbox.checked = opt.selected;
                checkbox.dataset.optionText = opt.text; // Pour le filtre accent-insensitive
                checkbox.addEventListener('change', function() {
                    opt.selected = checkbox.checked;
                });
                label.appendChild(checkbox);
                let span = document.createElement('span');
                span.textContent = opt.text;
                label.appendChild(span);
                grid.appendChild(label);
            });
            select.style.display = 'none';
            select.parentNode.insertBefore(container, select.nextSibling);

            // Fonction de filtre accent-insensitive
            function normalizeString(str) {
                return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
            }
            search.addEventListener('input', function() {
                let val = normalizeString(search.value);
                grid.childNodes.forEach(function(label) {
                    let text = label.querySelector('span').textContent;
                    if (normalizeString(text).includes(val)) {
                        label.style.display = '';
                    } else {
                        label.style.display = 'none';
                    }
                });
            });
        });
    });
    </script>
    <style>
    .custom-multiselect-container label {
        cursor: pointer;
        background: #f8f8f8;
        border-radius: 0.5rem;
        padding: 0.3rem 0.8rem;
        transition: background 0.15s;
    }
    .custom-multiselect-container label:hover {
        background: #b22222;
        color: #fff;
    }
    .custom-multiselect-container input[type="search"] {
        outline: none;
    }
    </style>
    """

