from django.db import models
from django.db.models import SET_NULL, CASCADE
from django.contrib.auth.models import User


complexity = (
    ('light', 'light'),
    ('middle', 'middle'),
    ('hard', 'hard'),
)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    inventory = models.CharField(max_length=100)

    def __str__(self):
        return self.inventory


class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gym = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Workout(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True)
    desc = models.TextField()
    views = models.PositiveIntegerField(default=0)
    photo = models.ImageField(null=True)
    complexity = models.CharField(max_length=100, choices=complexity)
    inventory = models.ForeignKey('Inventory', null=True, on_delete=SET_NULL)
    category = models.ForeignKey('Category', null=True, on_delete=SET_NULL)
    trainer = models.ForeignKey('Trainer', null=True, on_delete=SET_NULL)

    def __str__(self):
        return self.name


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True)
    desc = models.TextField()
    photo = models.ImageField(null=True, blank=True)
    video = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class ExerciseInWorkout(models.Model):
    approaches = models.PositiveSmallIntegerField()
    repetitions = models.PositiveSmallIntegerField()
    weight = models.PositiveSmallIntegerField(null=True, blank=True)
    day = models.CharField(max_length=100)
    number = models.PositiveSmallIntegerField()
    workout = models.ForeignKey('Workout', null=True, on_delete=SET_NULL)
    exercise = models.ForeignKey('Exercise', null=True, on_delete=SET_NULL)

    def __str__(self):
        return f'{self.exercise.name}\n' \
               f'Подходы: {self.approaches}\n' \
               f'Повторения: {self.repetitions}\n\n'


class UserWorkout(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    workout = models.ForeignKey('Workout', on_delete=CASCADE)


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=500)
    slug = models.SlugField(null=True)
    photo = models.ImageField(null=True)
    author = models.ForeignKey(User, null=True, on_delete=SET_NULL)

    def __str__(self):
        return self.title


class RecipeStep(models.Model):
    text = models.TextField()
    recipe = models.ForeignKey('Recipe', null=True, on_delete=SET_NULL)


class ActiveWorkout(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    workout = models.ForeignKey('Workout', on_delete=CASCADE)

    def __str__(self):
        return self.workout.name


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    workout = models.ForeignKey('ActiveWorkout', null=True, on_delete=SET_NULL)
    date = models.DateField()
    text = models.TextField()
