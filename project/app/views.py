from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from app.models import Assignment, CustomUser
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from app.forms import SignUpForm
from django.utils.text import slugify

# Test data for usernames and passwords
# CustomUser.objects.create_user(username='Cathy', password='pass123', is_admin=True)
# CustomUser.objects.create_user(username='Betty', password='1234', is_admin=True)
# CustomUser.objects.create_user(username='Leon', password='ok', is_admin=False)
# CustomUser.objects.create_user(username='John', password='uncommonPassword', is_admin=False)

# Test data for tasks

# ASSIGNMENTS = [
#     {'id': 1, 'title': 'Group Project','slug': 'cleaning', 'description': 'Start working on your group project', 'due_date': '10-30-2024', 'completed': False, 'people_involved': 'Bob, Jane, Mary, Walter'},
#     {'id': 2, 'title': 'Math Test','slug': 'math test', 'description': 'Make sure to take test', 'due_date': '11-05-2024', 'completed': True, 'people_involved': 'Alice, Mark'},
# ]

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
    assignments = Assignment.objects.all()
    students = CustomUser.objects.all()

    if request.method == 'POST':
        # if it already exists
        if request.POST.get("taskToEdit"):
            task_to_edit = request.POST.get("taskToEdit")
            team_member_ids = request.POST.getlist('teamMembers[]')
            description = request.POST.get('editDescription')
            due_date = request.POST.get('editDueDate')
            status = request.POST.get('status')

            assignment = get_object_or_404(Assignment, id=task_to_edit)
            assignment.description = description
            assignment.due_date = due_date
            assignment.completed = status == 'Complete'
            assignment.people_involved.set(team_member_ids)
            assignment.save()
            return redirect('assigner')

            # create a new assignment
        else:
            title = request.POST.get('task')
            description = request.POST.get('description')
            due_date = request.POST.get('due_date')
            namelist = request.POST.getlist('teamMembers[]')
            slug = slugify(title)
            # create
            assignment = Assignment.objects.create(
                title=title,
                slug=slug,
                description=description,
                due_date=due_date
            )
            assignment.people_involved.set(namelist)
            assignment.save()
            return redirect('assigner') 


    return render(request, 'assigner.html', 
    {
        'role': 'admin',
        'assignments': assignments,
        'students': students
    })

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