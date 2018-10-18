import eel
import json
import os
import time
import requests

eel.init('web')

def pyCrData():
  if not os.path.exists('web/data'):
    os.makedirs('web/data')

@eel.expose()
def pyDelCity(city):
  with open('web/data/cities.json',"r") as json_file :
    cities= json.load(json_file)
    i=0
    for item in cities:
      if item == city:
        cities.pop(i)
      i=i+1
    with open('web/data/cities.json',"w") as json_file :
     json.dump(cities,json_file)
    
  if os.path.exists('web/data/data.json'):  
    with open('web/data/data.json',"r") as jsond_file :
      data= json.load(jsond_file)
      j=0
      for itemd in data:
        if itemd['city'] == city:
          data.pop(j)
        j+=1
      with open('web/data/data.json',"w") as jsond_file :
       json.dump(data,jsond_file)
      
    
@eel.expose
def pyAddCity(city):
    if os.path.exists('web/data/cities.json'):
      with open('web/data/cities.json',"r") as json_file :
        cities= json.load(json_file)
      with open('web/data/cities.json',"w") as json_file :
        cities.append(city)
        json.dump(cities,json_file)
      
    else:
      with open('web/data/cities.json' ,"w") as json_file:
        cities=[]
        cities.append(city)
        json.dump(cities,json_file)
      
 
@eel.expose
def pyGetWeather():
  try:
      with open('web/data/cities.json',"r") as json_file :
            cities= json.load(json_file)
      if cities != "":
        url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=1671ee130cf79df598d88b40c0361685'
        weather_data=[]
        try:
          for city in cities:
            try:
              response = requests.get(url.format(city)).json()
              weather = {
                      'city' : city,
                      'temperature' : round(response['main']['temp'],0) ,
                      'description' : response['weather'][0]['description'],
                      'icon' : response['weather'][0]['icon'],
              }
              weather_data.append(weather)
            except KeyError:
              eel.jsMessage("City name is not correct!")
              pyDelCity(city)
        except requests.ConnectionError:
            eel.jsMessage("Internet connection error!")
        
        with open('web/data/data.json',"w") as jsond_file:
          json.dump(weather_data,jsond_file)
                  
  except:
    return
    
@eel.expose
def pyLastMod():
	if os.path.exists('web/data/data.json'):
		lastMod = time.ctime(os.path.getmtime('web/data/data.json'))
		return lastMod
    
pyCrData()
eel.start('index.html',size=(500,600))

