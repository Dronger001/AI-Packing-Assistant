import requests
import tkinter as tk
from tkinter import messagebox

class PackingAssistant:
    def __init__(self, api_key):
        self.api_key = api_key
        self.weather_api_url = "http://api.weatherstack.com/current"

    def get_weather(self, location):
        params = {
            'access_key': self.api_key,
            'query': location
        }
        response = requests.get(self.weather_api_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if "current" in data:
                return data
            else:
                raise Exception(f"Error in API response: {data.get('error', {}).get('info', 'Unknown error')}")
        else:
            raise Exception(f"Error fetching weather data: {response.status_code}")

    def suggest_packing_list(self, location):
        try:
            weather_data = self.get_weather(location)
            temp = weather_data['current']['temperature']
            weather_condition = weather_data['current']['weather_descriptions'][0]

            packing_list = []
            if temp < 10:
                packing_list += ["Warm jacket", "Gloves", "Scarf", "Thermal wear"]
            elif 10 <= temp <= 20:
                packing_list += ["Light jacket", "Sweater", "Jeans"]
            else:
                packing_list += ["T-shirts", "Shorts", "Sunglasses", "Hat"]

            if "rain" in weather_condition.lower():
                packing_list.append("Umbrella")
            elif "snow" in weather_condition.lower():
                packing_list.append("Snow boots")

            return packing_list
        except Exception as e:
            return [str(e)]

def get_packing_list():
    location = location_entry.get()
    if not location:
        messagebox.showerror("Error", "Please enter a location.")
        return

    try:
        packing_list = assistant.suggest_packing_list(location)
        result_text.set("\n".join(packing_list))
    except Exception as e:
        messagebox.showerror("Error", str(e))

API_KEY = "deb4bdf09cbf1fa2295d226d66520985"  
assistant = PackingAssistant(API_KEY)

root = tk.Tk()
root.title("Packing Assistant")

root.attributes("-fullscreen", True)

tk.Label(root, text="Enter Location:").pack(pady=5)
location_entry = tk.Entry(root, width=30)
location_entry.pack(pady=5)

tk.Button(root, text="Get Packing List", command=get_packing_list).pack(pady=10)

result_text = tk.StringVar()
tk.Label(root, text="Packing List:").pack(pady=5)
result_label = tk.Label(root, textvariable=result_text, justify="left", wraplength=300)
result_label.pack(pady=5)

def exit_fullscreen(event):
    root.attributes("-fullscreen", False)

root.bind("<Escape>", exit_fullscreen)

root.mainloop()