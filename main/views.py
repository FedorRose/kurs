from datetime import datetime

from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.db.models import Q
from calendar import HTMLCalendar
from datetime import date
import calendar
from .forms import EventForm
from .models import *

menu = {'Главная': 'home', 'Тренировки': 'workouts', 'Упражнения': 'exercises', 'Рецепты': 'recipes',
        'Дневник тренировок': 'home'}


def home(request):
    active_workouts = None
    if request.user.is_authenticated:
        active_workouts = ActiveWorkout.objects.filter(user=request.user)
    workouts = Workout.objects.order_by('-views')[:12]
    recipes = Recipe.objects.all()
    return render(request, 'main/home.html', context={'workouts': workouts, 'title': 'Главная', 'menu': menu,
                                                      'active_workouts': active_workouts, 'recipes': recipes})


def workouts(request):
    active_workouts = None
    if request.user.is_authenticated:
        active_workouts = ActiveWorkout.objects.filter(user=request.user)
    workouts = Workout.objects.all()
    return render(request, 'main/workouts.html', context={'workouts': workouts, 'title': 'Тренировки', 'menu': menu,
                                                          'active_workouts': active_workouts})


def workout(request, slug=None):
    current_workout = Workout.objects.get(slug=slug)
    active = None
    if request.user.is_authenticated:
        active = ActiveWorkout.objects.filter(workout=current_workout, user=request.user)
    exercises_1 = ExerciseInWorkout.objects.filter(workout=current_workout, day=1)
    exercises_2 = ExerciseInWorkout.objects.filter(workout=current_workout, day=2)
    exercises_3 = ExerciseInWorkout.objects.filter(workout=current_workout, day=3)
    exercises_4 = ExerciseInWorkout.objects.filter(workout=current_workout, day=4)
    return render(request, 'main/workout.html', context={'workout': current_workout, 'title': 'Тренировки', 'menu': menu,
                                                         'exercises_1': exercises_1, 'exercises_2': exercises_2,
                                                         'exercises_3': exercises_3, 'exercises_4': exercises_4,
                                                         'active': active})


def exercises_page(request):
    query = request.GET.get('q')
    if query is not None:
        guide_exercises = Exercise.objects.filter(Q(name__iregex=query) | Q(desc__iregex=query))
    else:
        guide_exercises = Exercise.objects.all()
    return render(request, 'main/exercises.html', context={'guide_exercises': guide_exercises, 'title':
                                                           'Упражнения', 'menu': menu})


def exercise_page(request, slug=None):
    guide_exercise = Exercise.objects.get(slug=slug)
    return render(request, 'main/exercise.html', context={'guide_exercise': guide_exercise, 'title':
                                                           'Упражнения', 'menu': menu})


def user_workouts(request):
    if request.user.is_authenticated():
        # current_user = User.objects.get(pk=request.user)
        workouts = Workout.objects.filter(user=request.user)
        return render(request, 'main/index.html', context={'workouts': workouts})
    else:
        return render(request, 'main/403.html')


def add_workout(request):
    if request.method == 'POST':
        pass


def start_workout(request, slug=None):
    curr_workout = Workout.objects.get(slug=slug)
    ActiveWorkout.objects.create(workout=curr_workout, user=request.user).save()
    return redirect('workout', slug)


def recipes(request, slug=None):
    recipes, current_recipe = None, None
    if slug is None:
        recipes = Recipe.objects.all()
    else:
        current_recipe = Recipe.objects.get(slug=slug)
    return render(request, 'main/recipes.html', context={'recipe': current_recipe, 'recipes': recipes,
                                                         'title': 'Рецепты', 'menu': menu})


def diary(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return HttpResponseRedirect(reverse('diary'))

    year, month = None, None
    if request.method == 'GET':
        month = request.GET.get('month')
        year = request.GET.get('year')

    if year is None:
        year = datetime.now().year
    if month is None:
        month = datetime.now().month

    form = EventForm(initial={workout: ActiveWorkout.objects.filter(user=request.user)})
    a = calendar.LocaleHTMLCalendar().formatmonth(int(year), int(month), withyear=True)
    return render(request, 'main/diary.html', context={'title': 'Дневник тренировок', 'menu': menu,
                                                       'form': form, 'calendar': a})


def diary_note(request, curr_date):
    note = Event.objects.filter(date=curr_date).last()
    if note is not None:
        return HttpResponse("{} - {} ={}".format(note.date, note.workout, note.text))
    else:
        return HttpResponse("=")


def diary_note_exist(request, curr_date):
    return HttpResponse('0') if Event.objects.filter(date=curr_date).last() is None else HttpResponse('1')


def workout_day(request, pk, day):
    work = ActiveWorkout.objects.get(pk=pk).workout

    return HttpResponse(ExerciseInWorkout.objects.filter(workout=work, day=day))


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def logout_user(request):
    logout(request)
    return redirect('home')
