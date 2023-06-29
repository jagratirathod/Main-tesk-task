from django.urls import path
from . import views


urlpatterns = [
    path('', views.ExerciseView.as_view(),name='exercise'),
]