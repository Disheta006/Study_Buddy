from django.urls import path
from .views import  flashcards

urlpatterns = [
    path('',flashcards,name='flashcards'),
]