from django.template.defaulttags import url
from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', enter_page, name='enter_page'),
    path('home_page', home_page, name="home_page"),
    path('register/', register_user, name='register'),
    path('notes/', notes, name='notes'),
    path('login/', login_user, name='login'),
    path('your_profile/<slug:user_slug>', user_profile, name='user_profile'),
    path('logout/', logout_user, name='logout'),
    path('add_note/', add_note, name='add_note'),
    path('edit_your_profile', edit_profile, name="edit_profile"),
    path('delete_your_note/<slug:note_slug>', delete_note, name="delete_note"),
    path('user_profile/<slug:user_slug>', watch_user, name="watch_user"),
    path('delete_account/<slug:username>', delete_account, name="delete_account"),
    path('profile_notes/<slug:username>/', profile_notes, name="profile_notes"),
]