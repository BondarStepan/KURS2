from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from polls.views import firstEnter
import django
from django.contrib.auth import views as auth_views
# from polls.views import CountryAutocomplete
import django_registration
urlpatterns = [
    path('', firstEnter),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('oauth/', include('social_django.urls', namespace='social')),
    # path('country-autocomplete/', CountryAutocomplete.as_view(), name='country-autocomplete'),
    path('search/', include('haystack.urls')),
    ]
    # path(r'^tagging/', include('tagging.urls')),




