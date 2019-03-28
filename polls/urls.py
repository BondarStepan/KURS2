from django.conf.urls import url, include
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# from polls.views import CountryAutocomplete
app_name = 'polls'
urlpatterns = [
    path('new/era/', views.new_era),
    path('', views.firstEnter, name='index'),
    path('logged', views.main_logged, name='index'),
    path('save_like', views.save_like, name='index'),
    path('change_val', views.change_val, name='index'),
    path('change_language', views.change_language, name='index'),
    path('change_theme', views.change_theme, name='index'),
    path('refresh_comment', views.refresh_comment, name='index'),
    path('change_rate', views.change_rate, name='index'),
    path('send_picture', views.send_picture, name='index'),
    path('add_compendium/', views.add_compendium, name='index'),
    path('add_comment/', views.add_comment, name='index'),
    path('save_compendium/', views.save_compendium, name='index'),
    path('profile/', views.main_logged, name='index'),
    path('logout', views.log_out, name='index'),
    path('delete', views.delete, name='index'),
    path('private', views.private_office, name='index'),
    path('signup/', views.signup_page, name='contact'),
    path('register/', views.signup, name='contact'),
    path('auth/', views.signin, name='contact'),
    path('signup/signin/', views.signin, name='contact'),
    path('signin/', views.signin_page, name='contact'),
    path('<int:compendium_id>/view_compendium', views.veiw_compendium, name='contact'),
    path('<int:compendium_id>/view_compendium_logged', views.veiw_compendium_logged, name='contact'),
    path('signin/registration', views.signin, name='contact'),
    # path('signup/unlock/', views.unlock, name='contact'),
    path(r'^signup/$', views.signup, name='signup'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        views.activate, name='activate'),
    path('search/', include('haystack.urls')),
]
