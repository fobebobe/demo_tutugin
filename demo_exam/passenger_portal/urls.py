from django.contrib import admin
from django.urls import path
from courses import views

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', views.login_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('applications/', views.applications_view, name='applications'),
    path('applications/create/', views.create_application_view, name='create_application'),
    path('panel/', views.admin_panel_view, name='admin_panel'),
]
