from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from django.contrib.auth import views as auth_views
from search import views as search_views
from home.views import signup, accueil
from modules import views as modules_views
from utilisateurs import views as user_views
from modules import views as modules_views

urlpatterns = [
    # Django admin
    path("django-admin/", admin.site.urls),

    path('', accueil, name='accueil'),

    # Wagtail admin & documents
    path("admin/", include("wagtail.admin.urls")),
    path("documents/", include("wagtail.documents.urls")),

    # Authentification standard
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html"
        ),
        name="login",
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(next_page="/"),
        name="logout",
    ),
    path("signup/", signup, name="signup"),

    # Recherche et espace utilisateur
    path("search/", search_views.search, name="search"),
    path("espace/",                   user_views.espace_utilisateur, name="espace_utilisateur"),
    
    path("espace/fiche/<path:slug>/valider/", user_views.valider_fiche, name="valider_fiche"),
    path("espace/fiche/<path:slug>/", user_views.fiche_detail, name="fiche_detail"),


    # Lecture des données dans modules
    path('modules/', include('modules.urls')),
    # path('utilisateurs/', include('utilisateurs.urls')),




    # Suivi progression (regroupement de progression/urls.py)
    path("suivi/", include("progression.urls")),

    

    path("modules/", modules_views.liste_modules, name="liste_modules"),


]

# Statics et médias en debug
if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Wagtail doit rester à la fin
urlpatterns += [
    path("", include(wagtail_urls)),
]
