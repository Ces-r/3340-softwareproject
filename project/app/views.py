from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from app.models import Assignment
from django.shortcuts import get_object_or_404


# Test data for usernames and passwords
# CustomUser.objects.create_user(username='Cathy', password='pass123', is_admin=True)
# CustomUser.objects.create_user(username='Betty', password='1234', is_admin=True)
# CustomUser.objects.create_user(username='Leon', password='ok', is_admin=False)

# Test data for tasks

ASSIGNMENTS = [
    {'id': 1, 'title': 'Group Project','slug': 'cleaning', 'description': 'Start working on your group project', 'due_date': '10-30-2024', 'completed': False, 'people_involved': 'Bob, Jane, Mary, Walter'},
    {'id': 2, 'title': 'Math Test','slug': 'math test', 'description': 'Make sure to take test', 'due_date': '11-05-2024', 'completed': True, 'people_involved': 'Alice, Mark'},
]

# used to hold our users
test_users = {}

# creates a user and assigns it a username, passwords, and gives it
# an admin marker

# def create_user():
#     global test_users
#     for user in DB:
#         username = user['username']
#         password = user['password']
#         admin = user['admin']
#         test_users[username] = {'password': password, 'admin': admin}    

# # calls funtion to create our users

# create_user()

# home view

def home(request):
    return redirect('login')

# login view that checks username and password
# then depending on admin status 
# redirects to either employee view or manager view
# also displays an error message for invalid usernames or passwords

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

# logout view

def logout_view(request):
    logout(request)
    return redirect('login')

# view for manager

def assigner_view(request):
    return render(request, 'assigner.html', {'role': 'admin'})

# view for employee tasks that shows a list of all tasks 
# an employee has to commit

# def all_assignments_view(request):
#    return render(request, 'all_assignments.html', {'assignments': ASSIGNMENTS, 'role': 'user'})

def all_assignments_view(request):
    # Fetch all assignments from the database
    assignments = Assignment.objects.all()
    return render(request, 'all_assignments.html', {'assignments': assignments, 'role': 'user'})

# view for detailed employee tasks

# def assignment_view(request, assignment_slug):
    
#     assignment = None

#     for a in ASSIGNMENTS:
#         if a['slug'] == assignment_slug:
#             assignment = a
#             break


#     if request.method == 'POST':
#         if 'complete' in request.POST:
#             assignment['completed'] = True
#         elif 'incomplete' in request.POST:
#             assignment['completed'] = False
    
#     return render(request, 'assignment.html', {'assignment': assignment})

def assignment_view(request, assignment_slug):
    # Get the assignment by slug or return 404 if not found
    assignment = get_object_or_404(Assignment, slug=assignment_slug)

    if request.method == 'POST':
        if 'complete' in request.POST:
            assignment.status = True  # Update the status field
            assignment.save()
        elif 'incomplete' in request.POST:
            assignment.status = False  # Update the status field
            assignment.save()

    return render(request, 'assignment.html', {'assignment': assignment})