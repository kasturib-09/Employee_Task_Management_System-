from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('add-task/', views.add_task, name='add_task'),
    path('edit-task/<int:id>/', views.edit_task, name='edit_task'),
    path('delete-task/<int:id>/', views.delete_task, name='delete_task'),

    path('add-employee/', views.add_employee, name='add_employee'),
]