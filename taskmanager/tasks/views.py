from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Task, Category
from .forms import TaskForm, CategoryForm


# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # login the user
            return redirect('home')
        
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


@login_required
def home(request):
    return render(request, 'home.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def task_list(request):
    tasks = Task.objects.filter(owner=request.user)

    # Get filter values from query parameters
    status = request.GET.get('status')
    priority = request.GET.get('priority')
    due = request.GET.get('due_at')
    sort = request.GET.get('sort')
    search = request.GET.get('search')
    category_id = request.GET.get('category')

    # Category filter
    if category_id:
        tasks = tasks.filter(category_id=category_id)

    # filter by status
    if status in ['pending', 'in progress', 'completed']:
        tasks = tasks.filter(status=status)

    # filter by priority
    if priority in ['low', 'medium', 'high']:
        tasks = tasks.filter(priority=priority)

    # filter by due date
    today = timezone.now().date()

    if due == 'today':
        tasks = tasks.filter(due=today)
    elif due == 'week':
        week_later = today + timedelta(days=7)
        tasks = tasks.filter(due_date__gte=today, due_date__lte=week_later)
    elif due == 'overdue':
        tasks = tasks.filter(due_date__lt=today)

    # Sorting: newest / oldest
    if sort == 'oldest':
        tasks = tasks.order_by('created_at')
    else:  # default or 'newest'
        tasks = tasks.order_by('-created_at')

    # Search
    if search:
        tasks = tasks.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )

    # Pagination
    paginator = Paginator(tasks, 5)  # tasks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'tasks': page_obj,
        'page_obj': page_obj,
        'current_status': status,
        'current_priority': priority,
        'current_due': due,
        'current_sort': sort,
        'current_search': search,
        'current_category': category_id,
    }

    return render(request, 'task_list.html', context)


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    return render(request, 'task_detail.html', {'task': task})


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            return redirect('task_list')
        
    else:
        form = TaskForm()

    return render(request, 'task_form.html', {'form': form})


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
        
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'task_form.html', {'form':form})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    
    return render(request, 'task_confirm_delete.html', {'task': task})


@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_create')
        
    else:
        form = CategoryForm()

    return render(request, 'category_form.html', {'form': form})


@login_required
def profile(request):
    user = request.user

    tasks = Task.objects.filter(owner=user)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='completed').count()
    pending_tasks = tasks.filter(status='pending').count()
    in_progress_tasks = tasks.filter(status='in_progress').count()

    today = timezone.now().date()
    overdue_tasks = tasks.filter(
        due_at__lt=today,
    ).exclude(status='completed').count()

    context = {
        'user': user,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'overdue_tasks': overdue_tasks,
    }
    return render(request, 'profile.html', context)


