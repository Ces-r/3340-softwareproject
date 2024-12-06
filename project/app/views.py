from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from app.models import Assignment, CustomUser
from django.contrib.auth.forms import UserCreationForm
from app.forms import SignUpForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required



# Test data for usernames and passwords
# CustomUser.objects.create_user(username='Cathy', password='pass123', is_admin=True)
# CustomUser.objects.create_user(username='Betty', password='1234', is_admin=True)
# CustomUser.objects.create_user(username='Leon', password='ok', is_admin=False)
# CustomUser.objects.create_user(username='John', password='uncommonPassword', is_admin=False)
# CustomUser.objects.create_user(username='NewTestUser', password='uncommonPassword', is_admin=False)

# used to hold our users
test_users = {}

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

# register view that adds new users into database
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
                messages.success(request, "Registration successful. You are now registered!")
                return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

# logout view
def logout_view(request):
    logout(request)
    return redirect('login')

# view for manager
def assigner_view(request):
    # Fetch all assignments and students
    assignments = Assignment.objects.all()
    students = CustomUser.objects.all()

    if request.method == 'POST':
        # Handle task deletion
        if 'delete_task' in request.POST:
            task_id = request.POST.get('delete_task')
            assignment = get_object_or_404(Assignment, id=task_id)
            assignment.delete()
            return redirect('assigner')

        # Handle task editing
        elif request.POST.get("taskToEdit"):
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

        # Handle new task creation
        else:
            title = request.POST.get('task')
            description = request.POST.get('description')
            due_date = request.POST.get('due_date')
            namelist = request.POST.getlist('teamMembers[]')
            slug = slugify(title)
            assignment = Assignment.objects.create(
                title=title,
                slug=slug,
                description=description,
                due_date=due_date
            )
            assignment.people_involved.set(namelist)
            assignment.save()
            return redirect('assigner')

    # Render the template with data
    return render(request, 'assigner.html', {
        'role': 'admin',
        'assignments': assignments,
        'students': students
    })

# view for employee tasks that shows a list of all tasks 
# an employee has to commit
def all_assignments_view(request):
    # Fetch all assignments from the database
    assignments = Assignment.objects.all()
    students = CustomUser.objects.all()
    return render(request, 'all_assignments.html', {'assignments': assignments, 'students': students, 'role': 'user'})

# view for detailed employee tasks
def assignment_view(request, assignment_slug):
    # Get the assignment by slug or return 404 if not found
    assignment = get_object_or_404(Assignment, slug=assignment_slug)

    if request.method == 'POST':
        if 'complete' in request.POST:
            assignment.completed = True  # Mark as completed
        elif 'incomplete' in request.POST:
            assignment.completed = False  # Mark as incomplete
        assignment.save()  # Save the updated status to the database
        return redirect('assignment', assignment_slug=assignment.slug)  # Redirect back to the same page

    return render(request, 'assignment.html', {'assignment': assignment})


