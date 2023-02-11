from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, CustomLoginView, RegisterRage, show_map  
from django.contrib.auth.views import LogoutView
from django.shortcuts import render

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),          # if 'logout' then next page 'login'
    path('register/', RegisterRage.as_view(), name='register'),
    path('', TaskList.as_view(), name='tasks'),                                     # looks for task_list.html in templates/base
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),                      # looks for task_detail.html in templates/base
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>', TaskDelete.as_view(), name='task-delete'),
    path('map/', show_map, name='map'),
] 