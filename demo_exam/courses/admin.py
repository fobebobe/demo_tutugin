from django.contrib import admin
from .models import Profile, CourseApplication


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone')
    search_fields = ('full_name', 'phone')


@admin.register(CourseApplication)
class CourseApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'desired_date', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'course', 'payment_method')
    list_editable = ('status',)
    search_fields = ('user__username',)
