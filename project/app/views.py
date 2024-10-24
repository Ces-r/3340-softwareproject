from django.shortcuts import render, redirect


# Create your views here.

def login(request):
    return render(request, 'login.html')

def employee(request):
    return render(request, 'employee.html')

def manager(request):
    return render(request, 'manager.html')