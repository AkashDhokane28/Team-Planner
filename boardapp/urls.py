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
   path('create_board/', CreateBoardView.as_view(), name='create-board'),
   path('closed_board/', CloseBoardView.as_view(), name='closed-board'),
   path('add_task/',AddTaskView.as_view(), name='add-task'),
   path('update_task_status/', UpdateTaskStatusAPIView.as_view(), name='update-task-status'),
   path('list_boards/', ListBoardsAPIView.as_view(), name='list-boards'),
   path('export_board/', ExportBoardAPIView.as_view(), name='export-board')

]

