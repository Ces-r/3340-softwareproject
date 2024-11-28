from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from app.models import Assignment, CustomUser
from app.forms import SignUpForm


# Home view
def home(request):
    return redirect('login')

# Login view that checks username and password, redirects based on admin status
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            if user.is_admin:
                return redirect('assigner')
            else:
                return redirect('all_assignments')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    return render(request, 'login.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

# Manager view for assigning tasks
def assigner_view(request):
    assignments = Assignment.objects.all()
    students = CustomUser.objects.filter(is_admin=False)  # Only non-admin users
    return render(request, 'assigner.html', {'assignments': assignments, 'students': students, 'role': 'admin'})

# Employee tasks view
def all_assignments_view(request):
    assignments = Assignment.objects.all()
    return render(request, 'all_assignments.html', {'assignments': assignments, 'role': 'user'})

# Detailed assignment view
def assignment_view(request, assignment_slug):
    assignment = get_object_or_404(Assignment, slug=assignment_slug)

    if request.method == 'POST':
        if 'complete' in request.POST:
            assignment.completed = True  # Update the status field
            assignment.save()
        elif 'incomplete' in request.POST:
            assignment.completed = False  # Update the status field
            assignment.save()

    return render(request, 'assignment.html', {'assignment': assignment})

# User registration view
def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "Registration successful. You are now signed in!")
                return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})
