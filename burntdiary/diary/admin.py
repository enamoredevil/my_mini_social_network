from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'register_time']


class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'note_create_time']


admin.site.register(User, UserAdmin)
admin.site.register(Note, NoteAdmin)
