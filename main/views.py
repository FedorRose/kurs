from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Q
from calendar import HTMLCalendar
from datetime import date
from itertools import groupby
import calendar
import locale
from django.utils.html import conditional_escape as esc
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
    active_workouts = ActiveWorkout.objects.filter(user=request.user)
    workouts = Workout.objects.all()
    return render(request, 'main/workouts.html', context={'workouts': workouts, 'title': 'Тренировки', 'menu': menu,
                                                          'active_workouts': active_workouts})


def workout(request, slug=None):
    current_workout = Workout.objects.get(slug=slug)
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
    else:
        form = EventForm()

    a = calendar.LocaleHTMLCalendar()
    a = a.formatmonth(2022, 12, withyear=True)
    print(a)
    notes = Event.objects.filter(user=request.user)
    return render(request, 'main/diary.html', context={'notes': notes, 'title': 'Дневник тренировок',
                                                       'menu': menu, 'form': form, 'calendar': a})


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


# class WorkoutCalendar(HTMLCalendar):
#
#     def __init__(self, workouts):
#         super(WorkoutCalendar, self).__init__()
#         self.workouts = self.group_by_day(workouts)
#
#     def formatday(self, day, weekday):
#         if day != 0:
#             cssclass = self.cssclasses[weekday]
#             if date.today() == date(self.year, self.month, day):
#                 cssclass += ' today'
#             if day in self.workouts:
#                 cssclass += ' filled'
#                 body = ['<ul>']
#                 for workout in self.workouts[day]:
#                     body.append('<li>')
#                     body.append('<a href="%s">' % workout.get_absolute_url())
#                     body.append(esc(workout.title))
#                     body.append('</a></li>')
#                 body.append('</ul>')
#                 return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
#             return self.day_cell(cssclass, day)
#         return self.day_cell('noday', '&nbsp;')
#
#     def formatmonth(self, year, month):
#         self.year, self.month = year, month
#         return super(WorkoutCalendar, self).formatmonth(year, month)
#
#     def group_by_day(self, workouts):
#         field = lambda workout: workout.performed_at.day
#         return dict(
#             [(day, list(items)) for day, items in groupby(workouts, field)]
#         )
#
#     def day_cell(self, cssclass, body):
#         return '<td class="%s">%s</td>' % (cssclass, body)