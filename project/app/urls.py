from django.urls import path
from . import views

# url config
urlpatterns = [
    path('', views.login, name = 'login'),
    path('employee/', views.employee, name = 'employee'),
    path('manager/', views.manager, name = 'manager')
]