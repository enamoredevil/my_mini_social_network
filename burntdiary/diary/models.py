from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    username = models.CharField(max_length=230, unique=True)
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    biography = models.TextField(blank=True, verbose_name="Биография")
    register_time = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(blank=True, null=True, verbose_name="Фото профиля", default='default.png')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'user_slug': self.username})

    def get_url_to_watch_profile(self):
        return reverse('watch_user', kwargs={'user_slug': self.pk})

    def get_url_to_delete_account(self):
        return reverse('delete_account', kwargs={'username': self.username})


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=230, verbose_name="Заголовок")
    note = models.TextField(verbose_name="Запись")
    note_create_time = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False, verbose_name='Для публикации')

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = "Записи"
        ordering = ['-note_create_time']

    def get_absolute_url(self):
        return reverse('delete_note', kwargs={'note_slug': self.id})

    def get_url_to_profile_notes(self):
        return reverse("profile_notes", kwargs={'username': self.user})

    def __str__(self):
        return self.title
