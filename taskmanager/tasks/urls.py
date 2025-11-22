from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'
    ), name='login'),
    path('logout/', views.logout_view, name='logout'),

    # CRUD PATH
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create', views.task_create, name='task_create'),
    path('tasks/<int:pk>', views.task_detail, name='task_detail'),
    path('tasks/<int:pk>/edit/', views.task_update, name='task_update'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('categories/add/', views.category_create, name='category_create'),

    # Profile
    path('profile/', views.profile, name='profile'),
]


