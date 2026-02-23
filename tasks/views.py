from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Task, Employee
from .forms import TaskForm, EmployeeForm


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if form.is_valid():
        login(request, form.get_user())
        return redirect('dashboard')

    return render(request, 'tasks/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    search = request.GET.get('search')
    priority = request.GET.get('priority')
    status = request.GET.get('status')

    if request.user.is_superuser:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(assigned_to=request.user)

    if search:
        tasks = tasks.filter(title__icontains=search)

    if priority:
        tasks = tasks.filter(priority=priority)

    if status:
        tasks = tasks.filter(status=status)

    context = {
        'tasks': tasks,
        'total': tasks.count(),
        'completed': tasks.filter(status='Completed').count(),
        'pending': tasks.filter(status='Pending').count(),
    }

    return render(request, 'tasks/dashboard.html', context)


@login_required
def add_task(request):
    if not request.user.is_superuser:
        return redirect('dashboard')

    form = TaskForm(request.POST or None)

    if form.is_valid():
        task = form.save(commit=False)
        task.created_by = request.user
        task.save()
        return redirect('dashboard')

    return render(request, 'tasks/add_task.html', {'form': form})


@login_required
def edit_task(request, id):
    task = get_object_or_404(Task, id=id)

    if not request.user.is_superuser:
        return redirect('dashboard')

    form = TaskForm(request.POST or None, instance=task)

    if form.is_valid():
        form.save()
        return redirect('dashboard')

    return render(request, 'tasks/add_task.html', {'form': form})


@login_required
def delete_task(request, id):
    task = get_object_or_404(Task, id=id)

    if not request.user.is_superuser:
        return redirect('dashboard')

    task.delete()
    return redirect('dashboard')


@login_required
def add_employee(request):
    if not request.user.is_superuser:
        return redirect('dashboard')

    form = EmployeeForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('dashboard')

    return render(request, 'tasks/add_employee.html', {'form': form})