from django.urls import path
from . import views

# url config
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('assigner/', views.assigner_view, name='assigner'),
    path('all_assignments/', views.all_assignments_view, name='all_assignments'),
    path('<str:assignment_slug>/', views.assignment_view, name='assignment'),
]