from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic.base import TemplateView

from . import views
from .forms import LoginForm

# Auth related paths
urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="login.html"),
        name="login",
    ),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(
            template_name="login.html", authentication_form=LoginForm
        ),
        name="login",
    ),
    path("accounts/logout/", views.logout_sucess, name="logout"),
    path(
        "registration/",
        views.CustomerRegistrationView.as_view(),
        name="registration",
    ),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/google/", include("social_django.urls", namespace="social")),
]

# App related paths
urlpatterns += [
    path("home/", views.home, name="home"),
    path("", views.home, name="home"),
    path("search/", views.search_results, name="search"),
    path(
        "item-detail/<int:pk>/",
        views.lost_item_detail_view,
        name="item-detail",
    ),
    path("claim/<int:item_id>/", views.ClaimItemView.as_view(), name="claim"),
    path("claims/", views.claims, name="claims"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("newsletter/", views.newsletter, name="newsletter"),
    path("hawkeye/", views.hawkeye, name="hawkeye"),
]

# Static files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
