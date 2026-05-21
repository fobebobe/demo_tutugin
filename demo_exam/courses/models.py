from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField('ФИО', max_length=255)
    phone = models.CharField('Телефон', max_length=20)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.full_name


class CourseApplication(models.Model): #заявка на обучение
    COURSE_CHOICES = [
        ('bus', 'Вождение автобуса'),
        ('electrobus', 'Вождение электробуса'),
        ('tram', 'Вождение трамвая'),
    ]

    PAYMENT_CHOICES = [
        ('cash', 'Наличными'),
        ('transfer', 'Перевод по номеру телефона'),
    ]

    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Идет обучение'),
        ('completed', 'Обучение завершено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    course = models.CharField('Курс', max_length=50, choices=COURSE_CHOICES)
    desired_date = models.DateField('Желаемая дата начала обучения')
    payment_method = models.CharField('Способ оплаты', max_length=20, choices=PAYMENT_CHOICES)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    review = models.TextField('Отзыв', blank=True, null=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.get_course_display()} — {self.user.username} ({self.get_status_display()})'
