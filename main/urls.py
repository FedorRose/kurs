from django.contrib import admin
# from django.contrib.auth import logout
from django.template.defaulttags import url
from django.urls import path, include

from kurs import settings
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('workouts/', workouts, name='workouts'),
    path('workouts/<slug:slug>/', workout, name='workout'),
    path('exercises/', exercises_page, name='exercises'),
    path('exercise/<slug:slug>/', exercise_page, name='exercise'),
    path('recipes/', recipes, name='recipes'),
    path('recipes/<slug:slug>/', recipes, name='recipe'),
    path('lk/add_workout/', add_workout, name='add_workout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', logout_user, name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('start_workout/<slug:slug>/', start_workout, name='start_workout'),
    path('diary/', diary, name='diary'),
    path('diary_note/<str:curr_date>/', diary_note, name='diary_note'),
    path('workout_day/<int:pk>/<int:day>/', workout_day, name='workout_day'),
    path('diary_note_exist/<str:curr_date>/', diary_note_exist, name='diary_note_exist'),

    # path('logout/', logout, name='logout'),
]
