from django.contrib import admin
from django.contrib.auth import logout
from django.urls import path, include

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('workouts/', workouts, name='workouts'),
    path('workouts/<slug:slug>/', workout, name='workout'),
    path('exercises/', exercises_page, name='exercises'),
    path('recipes/', recipes, name='recipes'),
    path('recipes/<slug:slug>/', recipes, name='recipe'),
    path('lk/add_workout/', add_workout, name='add_workout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('start_workout/<slug:slug>/', start_workout, name='start_workout'),
    path('diary/', diary, name='diary'),

    # path('logout/', logout, name='logout'),
]
