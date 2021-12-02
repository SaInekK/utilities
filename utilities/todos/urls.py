from django.urls import path

from .views import *


urlpatterns = [
    path('', TaskListView.as_view(), name='tasks'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('create/', CreateTaskView.as_view(), name='task_create'),
    path('edit/<int:pk>', UpdateTaskView.as_view(), name='task_update'),
    path('delete/<int:pk>', DeleteTaskView.as_view(), name='task_delete'),
]
