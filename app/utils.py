import aiohttp
import asyncio
import os
from app import db
from app.models import WeatherData, UserRequest
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

async def fetch_city_weather(session, user_id, city_id):
    async with session.get(BASE_URL, params={'id': city_id, 'appid': API_KEY, 'units': 'metric'}) as response:
        data = await response.json()
        if response.status == 200:
            weather_info = {
                "city_id": data['id'],
                "temperature": data['main']['temp'],
                "humidity": data['main']['humidity']
            }

            weather_data = WeatherData(
                user_id=user_id,
                weather_info=weather_info
            )

            db.session.add(weather_data)
            db.session.commit()
            user_request = UserRequest.query.filter_by(user_id=user_id).first()
            user_request.cities_processed += 1
            db.session.commit()

async def fetch_weather_data(user_id, city_ids):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for city_id in city_ids:
            task = fetch_city_weather(session, user_id, city_id)
            tasks.append(task)
            
            if len(tasks) % 60 == 0:
                await asyncio.gather(*tasks)
                tasks = []
                await asyncio.sleep(60)
        
        if tasks:
            await asyncio.gather(*tasks)
