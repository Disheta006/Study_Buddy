from operator import index

from django.shortcuts import render
import requests
from .model import Flashcard

# Create your views here.
api_key = "c2f301d0bcc650b430b3d1ed87cd585e"

def flashcards(request):
    city = request.GET.get("city","Hyderabad")
    index = int(request.GET.get("card",0))
    cards = list(Flashcard.objects.all())
    card = cards[index]
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
    }
    response = requests.get(url, params=params)
    data = response.json()
    print(data)

    if response.status_code != 200 or "weather" not in data:
        city = request.GET.get("city")
        if not city:
            city = "Hyderabad"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric",
        }
        response = requests.get(url, params=params)
        data = response.json()



    condition = data["weather"][0]["main"].lower()
    temp =data["main"]["temp"]
    description = data["weather"][0]["description"]

    if "rain" in condition:
        theme = "rainy"
        study_tip = "Rainy weather - perfect for deep study"
    elif "cloud" in condition:
        theme = "cloudy"
        study_tip = "Cloud weather - revise key concepts"
    elif "clear" in condition:
        theme = "sunny"
        study_tip = "Clear weather - stay productive"
    else:
        theme = "default"
        study_tip = "Unable to fetch weather, stay focused!"

    card.viewed = True
    card.save()

    context = {
        "city": city,
        "temp" : temp,
        "description" : description,
        "theme" : theme,
        "study_tip" : study_tip,
        "card" : card,
        "index" : index,
        "total" : len(cards),
    }
    return render(request,"dashboard/home.html",context)