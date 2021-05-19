from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from datetime import datetime
import requests
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, "main/index.html")

def register(request):
    form = request.POST
    errors = Register.objects.basic_validator(form)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/')
    else:
        user = Register.objects.create(first_name=form['first_name'], last_name=form['last_name'], email=form['email'], password=(form['password'] ))
        request.session['user_id'] = user.id #Save user ID in session
        return redirect("/dashboard")

def login(request):
    form = request.POST
    try: 
        user = Register.objects.get(email=form['email'])
    except: 
        messages.error(request, "Invalid email")
        return redirect("/")
    if user.password != form['password']:
        messages.error(request, "Invalid password")
        return redirect("/")
    request.session['user_id'] = user.id
    return redirect("/dashboard")

def logout(request):
    request.session.clear()
    return redirect("/")

def dashboard(request):
    return render(request, "main/dashboard.html", {
        "cities": City.objects.all(),
        "user": Register.objects.get(id=request.session['user_id'])
    })

def selectCity(request):
    selectedCity = City.objects.get(id=request.POST['city.id'])

def processCity(request):
    form = request.POST
    result_city = form['city'].title() #Get city name from search input
    cities = City.objects.all()
    for city in cities:
        if city.cityName == result_city: #If search input is already in db
            return redirect(f"/city/{city.id}")
    new = City.objects.create(cityName=request.POST['city']) #Else create new object
    new.save()
    return redirect(f"/city/{new.id}")

def cityDetail(request, city_id):
    cName = City.objects.get(id=city_id)
    city = f"{cName.cityName}"
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=146919892bc99f219a7c25fb96ef21de")
    if response.status_code == 404: #Delete invalid object
        City.objects.get(id=city_id).delete()
        return redirect('/error')
    temp = response.json()['main']['temp'] #Get temperature in Kelvin
    convertTemp = (temp - 273.15) * 9 / 5 + 32 #Convert Kelvin to Fahrenheit
    finalTemp = int(str(convertTemp)[:2]) #Get first 2 digits of the temp
    sunriseTime = response.json()['sys']['sunrise'] #Get and convert sunrise/sunset time from unix to pst military time
    finalSunriseTime = datetime.fromtimestamp(sunriseTime).strftime('%H:%M %p')
    sunsetTime = response.json()['sys']['sunset']
    finalSunsetTime = datetime.fromtimestamp(sunsetTime).strftime('%H:%M %p')
    windSpeed = response.json()['wind']['speed'] * 2.237 #Get wind speed in m/s and convert it to mph
    finalWindSpeed = int(str(windSpeed)[:1])
    return render(request, "main/cityDetail.html", {
        "weather": response.json(),
        "user": Register.objects.get(id=request.session['user_id']),
        "events": Event.objects.all(),
        "city": City.objects.get(id=city_id),
        "attendance": Attendance.objects.all(),
        "cityTemp": finalTemp,
        "sunriseTime": finalSunriseTime,
        "sunsetTime": finalSunsetTime,
        "windSpeed": finalWindSpeed
    })

def error(request):
    return render(request, 'main/404.html')

def removeCity(request, city_id):
    City.objects.get(id=city_id).delete()
    return redirect('/dashboard')

def processEvent(request, city_id):
    form = request.POST
    errors = Event.objects.event_validator(form)
    eventUser = Register.objects.get(id=request.session['user_id'])
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect(f'/city/{city_id}')
    else: 
        Event.objects.create(event_title=form['event_title'], event_description=form['event_description'], event_user=Register.objects.get(id=request.session['user_id']), event_user_firstName=eventUser.first_name, event_user_lastName=eventUser.last_name[0], event_city=City.objects.get(id=form['event_city']))
        return redirect(f'/city/{city_id}')

def removeEvent(request, event_id):
    form = request.POST
    cityID = City.objects.get(id=form['event_city']) # Get City id through hidden input
    Event.objects.get(id=event_id).delete()
    return redirect(f"/city/{cityID.id}")

def add_user_to_event(request, city_id):
    form = request.POST
    user = Register.objects.get(id=request.session['user_id'])
    Attendance.objects.create(join_event=True, user_name=user.first_name, name_users=Register.objects.get(id=request.session['user_id']), name_city=City.objects.get(id=form['name_city']), name_event=Event.objects.get(id=form['name_event']))
    return redirect(f"/city/{city_id}")

def delete_user_from_event(request, a_id):
    form = request.POST
    cityID = City.objects.get(id=form['event_city'])
    Attendance.objects.get(id=a_id).delete()
    return redirect(f"/city/{cityID.id}")
