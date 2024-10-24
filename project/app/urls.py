from django.urls import path
from . import views

# url config
urlpatterns = [
    path('login/', views.login, name = 'login'),
    path('employee/', views.employee, name = 'employee'),
    path('manager/', views.manager, name = 'manager')
]