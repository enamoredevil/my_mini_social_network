import os
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect
from .models import *

User = get_user_model()


@login_required()
def home_page(request):
    context = {
        'title': 'Home',
        'telegram': os.getenv('TELEGRAM_SUPPORT')
    }

    return render(request, 'diary/home_page.html', context=context)


def enter_page(request):
    if request.user.is_authenticated:
        return redirect('notes')
    return render(request, 'diary/enter_page.html')


def register_user(request):
    if request.method == "POST":
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password == password2:
            email = request.POST.get('email')
            username = request.POST.get('username')
            try:
                User.objects.create_user(username=username, email=email, password=password)
            except:
                messages.error(request, 'This nickname is already taken')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('notes')
        else:
            messages.error(request, 'Check your credentials, something went wrong')

    return render(request, 'diary/register.html')


def login_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('notes')
        else:
            messages.error(request, 'Check your credentials, something went wrong')

    return render(request, 'diary/login.html')


@login_required()
def notes(request):
    all_notes = Note.objects.filter(is_published=True).select_related('user')
    paginator = Paginator(all_notes, 2)
    page_number = request.GET.get('page')
    notes = paginator.get_page(page_number)
    context = {
        'title': "Notes",
        'notes': notes

    }

    return render(request, 'diary/notes.html', context=context)


@login_required()
def profile_notes(request, username):
    user = get_object_or_404(User, username=username)
    notes = Note.objects.filter(user=user)

    paginator = Paginator(notes, 2)
    page_number = request.GET.get('page')
    notes = paginator.get_page(page_number)

    context = {
        'title': "My notes",
        'notes': notes
    }
    return render(request, 'diary/profile_notes.html', context=context)


@login_required()
def user_profile(request, user_slug):
    context = {
        'title': "My profile",
        'user_slug': user_slug,
        'note': Note
    }
    return render(request, 'diary/profile.html', context=context)


def logout_user(request):
    logout(request)
    return redirect('enter_page')


@login_required()
def add_note(request):

    if request.method == "POST":
        title = request.POST.get('title')
        note = request.POST.get('note')
        is_published = request.POST.get('is_published')
        user = request.user
        Note.objects.create(title=title, note=note, user=user, is_published=is_published)
        return redirect('notes')
    context = {
        'title': 'Add Note'
    }
    return render(request, 'diary/add_note.html', context=context)


@login_required()
def edit_profile(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        biography = request.POST.get('biography')
        photo = request.FILES.get('photo')
        if photo is None:
            photo = request.user.photo
        else:
            photo = request.FILES.get('photo')
        user = User.objects.get(pk=request.user.pk)
        user.username = username
        user.email = email
        user.biography = biography
        user.photo = photo
        user.save()
        return redirect(user.get_absolute_url())

    context = {
        'title': 'Editing'
    }
    return render(request, 'diary/edit_profile.html', context=context)


@login_required()
def delete_note(request, note_slug):
    note = get_object_or_404(Note, pk=note_slug)
    note.delete()
    return redirect('notes')


@login_required()
def watch_user(request, user_slug):
    user = get_object_or_404(User, pk=user_slug)

    context = {
        'title': f"Profile - {user.username}",
        'user_profile': user
    }

    return render(request, 'diary/user_profile.html', context=context)


@login_required()
def delete_account(request, username):
    if request.method == "POST":
        try:
            user = User.objects.get(username=request.user.username)
            if user is not None:
                user.delete()
                logout(request)
                return redirect('enter_page')
            else:
                messages.error(request, 'The password is wrong')
        except User.DoesNotExist:
            messages.error(request, "User doesn't exist")

    context = {
        'title': f'Delete your account'
    }
    return render(request, 'diary/delete_profile.html', context=context)


