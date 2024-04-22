"""
URL configuration for teamPlanner project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,include
from .views import *

urlpatterns = [
   path('create_team/', CreateTeamAPIView.as_view(), name='create-team'),
   path('team_list/', ListTeamView.as_view(), name='team-list'),
   path('describe_team/', DescribeTeamView.as_view(), name='describe-team'),
   path('update_team/', UpdateTeamAPIView.as_view(), name='update-team'),
   path('add_users_to_team/', AddUsersToTeamView.as_view(), name='add-users-to-team'),
   path('remove_users_from_team/', RemoveUsersFromTeamView.as_view(), name='remove-users-from-team'),
   path('list_team_users/', ListTeamUsersView.as_view(), name='list-team-users'),
]

