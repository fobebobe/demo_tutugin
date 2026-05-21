from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile, CourseApplication
from .forms import RegistrationForm, LoginForm, ApplicationForm, ReviewForm, StatusForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('applications')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
            )
            Profile.objects.create(
                user=user,
                full_name=form.cleaned_data['full_name'],
                phone=form.cleaned_data['phone'],
            )
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('applications')
    else:
        form = RegistrationForm()

    return render(request, 'courses/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('applications')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # если это админ, то перенаправляем в панель администратора
                if user.is_staff:
                    return redirect('admin_panel')
                return redirect('applications')
            else:
                messages.error(request, 'Неверный логин или пароль.')
    else:
        form = LoginForm()

    return render(request, 'courses/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def applications_view(request):
    user_applications = CourseApplication.objects.filter(user=request.user)

    # обработка отзыва
    if request.method == 'POST':
        app_id = request.POST.get('app_id')
        application = get_object_or_404(CourseApplication, id=app_id, user=request.user)
        if application.status == 'completed':
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                application.review = review_form.cleaned_data['review']
                application.save()
                messages.success(request, 'Отзыв сохранен!')
                return redirect('applications')

    review_form = ReviewForm()
    return render(request, 'courses/applications.html', {
        'applications': user_applications,
        'review_form': review_form,
    })


@login_required
def create_application_view(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request, 'Заявка успешно отправлена!')
            return redirect('applications')
    else:
        form = ApplicationForm()

    return render(request, 'courses/create_application.html', {'form': form})


@login_required
def admin_panel_view(request):
    if not request.user.is_staff:
        messages.error(request, 'У вас нет доступа к панели администратора.')
        return redirect('applications')

    all_applications = CourseApplication.objects.select_related('user', 'user__profile').all()

    status_filter = request.GET.get('status', '')
    if status_filter:
        all_applications = all_applications.filter(status=status_filter)

    if request.method == 'POST':
        app_id = request.POST.get('app_id')
        application = get_object_or_404(CourseApplication, id=app_id)
        status_form = StatusForm(request.POST)
        if status_form.is_valid():
            application.status = status_form.cleaned_data['status']
            application.save()
            messages.success(request, f'Статус заявки #{application.id} изменен на «{application.get_status_display()}»')
            return redirect('admin_panel')

    status_form = StatusForm()
    return render(request, 'courses/admin_panel.html', {
        'applications': all_applications,
        'status_form': status_form,
        'status_filter': status_filter,
        'status_choices': CourseApplication.STATUS_CHOICES,
    })
