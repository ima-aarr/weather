import os
import requests


WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")


CITY = "Tokyo"

def get_weather():
   
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric&lang=ja"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"【{CITY}の現在の天気】: {desc} / 気温: {temp}℃"
    else:
        print(f"Error fetching weather: {response.text}")
        return None

def send_discord(message):
    if not message:
        return
    
    data = {"content": message}
    response = requests.post(WEBHOOK_URL, json=data)
    
    if response.status_code == 204:
        print("Discordへの送信が成功しました！")
    else:
        print(f"Discordへの送信に失敗しました: {response.status_code}")

if __name__ == "__main__":
    msg = get_weather()
    send_discord(msg)
