from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 


# Test data for usernames and passwords

DB = [
    {'username': 'Cathy', 'password': 'pass123', 'admin': True},
    {'username': 'Betty', 'password': '1234', 'admin': True},
    {'username': 'Leon', 'password': 'ok', 'admin': False},
    {'username': 'Bob', 'password': 'nice', 'admin': False},
    {'username': 'Tom', 'password': 'test', 'admin': False},
    {'username': 'Christy', 'password': 'cool', 'admin': False},
    {'username': '1', 'password': '1', 'admin': False},
]

# Test data for tasks

ASSIGNMENTS = [
    {'id': 1, 'title': 'Group Project','slug': 'cleaning', 'description': 'Start working on your group project', 'due_date': '10-30-2024', 'completed': False, 'people_involved': 'Bob, Jane, Mary, Walter'},
    {'id': 2, 'title': 'Math Test','slug': 'math test', 'description': 'Make sure to take test', 'due_date': '11-05-2024', 'completed': True, 'people_involved': 'Alice, Mark'},
]

# used to hold our users
test_users = {}

# creates a user and assigns it a username, passwords, and gives it
# an admin marker

def create_user():
    global test_users
    for user in DB:
        username = user['username']
        password = user['password']
        admin = user['admin']
        test_users[username] = {'password': password, 'admin': admin}    

# calls funtion to create our users

create_user()

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
        

        user = test_users.get(username)

        if user and user['password'] == password:
            if user['admin']:
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

def all_assignments_view(request):
    return render(request, 'all_assignments.html', {'assignments': ASSIGNMENTS, 'role': 'user'})

# view for detailed employee tasks

def assignment_view(request, assignment_slug):
    
    assignment = None

    for a in ASSIGNMENTS:
        if a['slug'] == assignment_slug:
            assignment = a
            break


    if request.method == 'POST':
        if 'complete' in request.POST:
            assignment['completed'] = True
        elif 'incomplete' in request.POST:
            assignment['completed'] = False
    
    return render(request, 'assignment.html', {'assignment': assignment})
