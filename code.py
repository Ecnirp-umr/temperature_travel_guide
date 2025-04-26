import requests
import google.generativeai as genai
from geopy.geocoders import Nominatim       #Into longitude and Latitude Know as Forwarding Geocoding

# Replace this with your actual API key
GEMINI_API_KEY = ""
genai.configure(api_key=GEMINI_API_KEY)

def get_coordinates(city_name):
    try:
        geolocator = Nominatim(user_agent="weather_app")    #Similar to name tag, send request ot OpenStreetMap Server
        location = geolocator.geocode(city_name)
        if location:
            return location.latitude, location.longitude
        else:
            print("Could not find coordinates for the city.")
            return None, None
    except Exception as e:
        print(f"Geocoding error: {e}")
        return None, None

def get_temperature(city_name):
    lat, lon = get_coordinates(city_name)
    if lat is None or lon is None:
        return None

    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current_weather=true"
        )
        response = requests.get(url)
        response.raise_for_status()     #checking for error
        data = response.json()          #dicttionary response
        return data["current_weather"]["temperature"]
    except Exception as e:
        print(f" Weather API error: {e}")
        return None

def generate_places(city_name, temperature):
    prompt = (
        f"The current temperature in {city_name} is {temperature}°C. "
        f"Suggest three specific, real tourist places someone can visit in {city_name}, considering the current {temperature}. "
        f"Suggest the dress code based on the {temperature}."
    )

    try:
        #model = genai.GenerativeModel(model_name="gemini-2.0-flash-lite")
        model = genai.GenerativeModel(model_name="gemini-2.0-pro-exp")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Gemini API error: {e}"

def main():
    city = input("Enter city name: ").strip()
    if not city:
        print(" Please enter a valid city name.")
        return

    temp = get_temperature(city)
    if temp is not None:
        places = generate_places(city, temp)
        print(f"\n Current Temperature in {city}: {temp}°C")
        print(" Suggested places and dress code:\n")
        print(places)

if __name__ == "__main__":
    main()
