import os
import requests
from datetime import datetime, timedelta


WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

CITY = "Tokyo"

def get_weather():

    current_url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric&lang=ja"
    current_res = requests.get(current_url)
    
 
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={WEATHER_API_KEY}&units=metric&lang=ja"
    forecast_res = requests.get(forecast_url)
    
    if current_res.status_code == 200 and forecast_res.status_code == 200:
        current_data = current_res.json()
        forecast_data = forecast_res.json()
        
       
        curr_temp = current_data["main"]["temp"]
        curr_desc = current_data["weather"][0]["description"]
        
      
        next_forecast = forecast_data["list"][0]
        future_temp = next_forecast["main"]["temp"]
        future_desc = next_forecast["weather"][0]["description"]
        
   
        dt_txt = next_forecast["dt_txt"]  # 例: "2023-10-01 12:00:00"
        dt_obj = datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S")
        jst_time = dt_obj + timedelta(hours=9)
        time_str = jst_time.strftime("%H:%M") # "21:00" のような形式にする

      
        message = (
            f"🌦️ **【{CITY}の天気情報】**\n"
            f"▶ **現在**: {curr_desc} / 気温: {curr_temp}℃\n"
            f"▶ **{time_str}頃の予想**: {future_desc} / 気温: {future_temp}℃"
        )
        return message
    else:
        print(f"エラーが発生しました。Current: {current_res.status_code}, Forecast: {forecast_res.status_code}")
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
