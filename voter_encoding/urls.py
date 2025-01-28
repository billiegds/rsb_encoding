# voter_encoding/urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),  # Built-in login view
    path('', views.index, name='index'),  # Index view
    # Add other URL patterns if you have them
    path('voters-autocomplete/', views.voters_autocomplete, name='voters_autocomplete'),
    path('add-party-leader/', views.add_party_leader, name='add_party_leader'), # Add URL pattern
    path('party-leader-autocomplete/', views.party_leader_autocomplete, name='party_leader_list'),
    path('autocomplete-name/', views.autocomplete_supporter, name='autocomplete_supporter'),
    path('add-supporter/', views.add_supporter, name='add_supporter'),
    path('supporters/', views.supporters_list, name='supporters_list'),
    path('login/voter_encoding/view_list/', views.view_list, name='view_list'),
    path('party-leader-ajax/', views.party_leader_list_ajax, name='party_leader_list_ajax'),
    path('find_cluster_by_precinct/', views.find_cluster_by_precinct, name='find_cluster_by_precinct'),
     # other paths...
]
