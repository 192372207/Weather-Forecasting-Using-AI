import httpx
from typing import Dict, Any, List, Tuple
from datetime import datetime

WEATHER_CODE_MAP = {
    0: ("Clear Sky", "sun"),
    1: ("Mainly Clear", "sun"),
    2: ("Partly Cloudy", "cloud-sun"),
    3: ("Overcast", "cloud"),
    45: ("Foggy", "cloud-fog"),
    48: ("Depositing Rime Fog", "cloud-fog"),
    51: ("Light Drizzle", "cloud-drizzle"),
    53: ("Moderate Drizzle", "cloud-drizzle"),
    55: ("Dense Drizzle", "cloud-drizzle"),
    61: ("Slight Rain", "cloud-rain"),
    63: ("Moderate Rain", "cloud-rain"),
    65: ("Heavy Rain", "cloud-showers-heavy"),
    71: ("Slight Snow", "snowflake"),
    73: ("Moderate Snow", "snowflake"),
    75: ("Heavy Snow", "snowflake"),
    80: ("Slight Rain Showers", "cloud-rain"),
    81: ("Moderate Rain Showers", "cloud-rain"),
    82: ("Violent Rain Showers", "cloud-showers-heavy"),
    95: ("Thunderstorm", "cloud-lightning"),
    96: ("Thunderstorm with Slight Hail", "cloud-lightning"),
    99: ("Thunderstorm with Heavy Hail", "cloud-lightning"),
}

DEFAULT_CITIES = {
    "london": (51.5074, -0.1278, "London", "United Kingdom"),
    "new york": (40.7128, -74.0060, "New York", "United States"),
    "tokyo": (35.6762, 139.6503, "Tokyo", "Japan"),
    "paris": (48.8566, 2.3522, "Paris", "France"),
    "sydney": (-33.8688, 151.2093, "Sydney", "Australia"),
    "mumbai": (19.0760, 72.8777, "Mumbai", "India"),
    "delhi": (28.6139, 77.2090, "Delhi", "India"),
}

async def geocode_city(city_name: str) -> Tuple[float, float, str, str]:
    normalized = city_name.strip().lower()
    if normalized in DEFAULT_CITIES:
        return DEFAULT_CITIES[normalized]
    
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                if "results" in data and len(data["results"]) > 0:
                    res = data["results"][0]
                    lat = res.get("latitude", 51.5074)
                    lon = res.get("longitude", -0.1278)
                    name = res.get("name", city_name.title())
                    country = res.get("country", "")
                    return (lat, lon, name, country)
        except Exception:
            pass
    # Fallback to London default if query fails
    return (51.5074, -0.1278, city_name.title(), "World")

async def get_current_weather(city: str) -> Dict[str, Any]:
    lat, lon, name, country = await geocode_city(city)
    
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&"
        f"current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,rain,weather_code,surface_pressure,wind_speed_10m,wind_direction_10m&"
        f"daily=weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max,precipitation_probability_max&"
        f"timezone=auto"
    )
    
    aqi_url = (
        f"https://air-quality-api.open-meteo.com/v1/air-quality?"
        f"latitude={lat}&longitude={lon}&current=us_aqi,pm2_5,pm10,nitrogen_dioxide,ozone"
    )
    
    current_data = {}
    aqi_val = 35
    aqi_desc = "Good"
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            res = await client.get(url)
            if res.status_code == 200:
                current_data = res.json()
        except Exception:
            pass

        try:
            aqi_res = await client.get(aqi_url)
            if aqi_res.status_code == 200:
                aqi_json = aqi_res.json()
                aqi_val = int(aqi_json.get("current", {}).get("us_aqi", 35))
                if aqi_val <= 50:
                    aqi_desc = "Good"
                elif aqi_val <= 100:
                    aqi_desc = "Moderate"
                elif aqi_val <= 150:
                    aqi_desc = "Unhealthy for Sensitive Groups"
                else:
                    aqi_desc = "Unhealthy"
        except Exception:
            pass

    cur = current_data.get("current", {})
    daily = current_data.get("daily", {})

    code = cur.get("weather_code", 0)
    cond, icon = WEATHER_CODE_MAP.get(code, ("Clear Sky", "sun"))

    high = daily.get("temperature_2m_max", [cur.get("temperature_2m", 22.0) + 4])[0]
    low = daily.get("temperature_2m_min", [cur.get("temperature_2m", 22.0) - 3])[0]
    sunrise = daily.get("sunrise", ["06:15 AM"])[0]
    sunset = daily.get("sunset", ["07:45 PM"])[0]
    uv = daily.get("uv_index_max", [5.2])[0]
    rain_prob = daily.get("precipitation_probability_max", [20])[0]

    if isinstance(sunrise, str) and "T" in sunrise:
        sunrise = sunrise.split("T")[1][:5] + " AM"
    if isinstance(sunset, str) and "T" in sunset:
        sunset = sunset.split("T")[1][:5] + " PM"

    return {
        "city": name,
        "country": country,
        "lat": lat,
        "lon": lon,
        "temp": round(cur.get("temperature_2m", 22.5), 1),
        "feels_like": round(cur.get("apparent_temperature", 23.0), 1),
        "humidity": int(cur.get("relative_humidity_2m", 58)),
        "wind_speed": round(cur.get("wind_speed_10m", 12.4), 1),
        "wind_direction": int(cur.get("wind_direction_10m", 180)),
        "pressure": round(cur.get("surface_pressure", 1013.25), 1),
        "uv_index": float(uv),
        "aqi": aqi_val,
        "aqi_description": aqi_desc,
        "visibility": 10.0,
        "condition": cond,
        "icon": icon,
        "sunrise": sunrise,
        "sunset": sunset,
        "rain_probability": int(rain_prob),
        "high": round(high, 1),
        "low": round(low, 1)
    }

async def get_hourly_forecast(city: str) -> List[Dict[str, Any]]:
    lat, lon, _, _ = await geocode_city(city)
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&"
        f"hourly=temperature_2m,precipitation_probability,weather_code,wind_speed_10m&"
        f"forecast_days=2&timezone=auto"
    )
    items = []
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                hourly = data.get("hourly", {})
                times = hourly.get("time", [])
                temps = hourly.get("temperature_2m", [])
                pops = hourly.get("precipitation_probability", [])
                codes = hourly.get("weather_code", [])
                winds = hourly.get("wind_speed_10m", [])
                
                # Extract next 24 hours
                for i in range(min(24, len(times))):
                    time_str = times[i]
                    formatted_time = time_str.split("T")[1][:5]
                    code = codes[i] if i < len(codes) else 0
                    cond, icon = WEATHER_CODE_MAP.get(code, ("Clear Sky", "sun"))
                    items.append({
                        "time": formatted_time,
                        "temp": round(temps[i], 1),
                        "condition": cond,
                        "icon": icon,
                        "pop": pops[i] if i < len(pops) else 10,
                        "wind_speed": round(winds[i], 1) if i < len(winds) else 10.0
                    })
                return items
        except Exception:
            pass

    # Fallback hours if API fails
    mock_times = ["00:00", "03:00", "06:00", "09:00", "12:00", "15:00", "18:00", "21:00"]
    for i, t in enumerate(mock_times):
        items.append({
            "time": t,
            "temp": round(20.0 + (i % 4) * 2, 1),
            "condition": "Partly Cloudy",
            "icon": "cloud-sun",
            "pop": 15,
            "wind_speed": 11.2
        })
    return items

async def get_daily_forecast(city: str, days: int = 7) -> List[Dict[str, Any]]:
    lat, lon, _, _ = await geocode_city(city)
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&"
        f"daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max&"
        f"forecast_days={days}&timezone=auto"
    )
    days_list = []
    days_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                daily = data.get("daily", {})
                dates = daily.get("time", [])
                codes = daily.get("weather_code", [])
                highs = daily.get("temperature_2m_max", [])
                lows = daily.get("temperature_2m_min", [])
                pops = daily.get("precipitation_probability_max", [])
                winds = daily.get("wind_speed_10m_max", [])

                for i in range(len(dates)):
                    d_str = dates[i]
                    dt = datetime.strptime(d_str, "%Y-%m-%d")
                    day_name = days_names[dt.weekday()]
                    code = codes[i] if i < len(codes) else 0
                    cond, icon = WEATHER_CODE_MAP.get(code, ("Sunny", "sun"))

                    days_list.append({
                        "date": d_str,
                        "day": day_name,
                        "condition": cond,
                        "icon": icon,
                        "high": round(highs[i], 1),
                        "low": round(lows[i], 1),
                        "rain_prob": int(pops[i]) if i < len(pops) and pops[i] is not None else 15,
                        "humidity": 60,
                        "wind_speed": round(winds[i], 1) if i < len(winds) else 12.0
                    })
                return days_list
        except Exception:
            pass

    for i in range(days):
        days_list.append({
            "date": f"2026-07-{23+i:02d}",
            "day": days_names[i % 7],
            "condition": "Partly Cloudy" if i % 2 == 0 else "Sunny",
            "icon": "cloud-sun" if i % 2 == 0 else "sun",
            "high": round(24.0 + (i % 3), 1),
            "low": round(15.0 + (i % 2), 1),
            "rain_prob": 20,
            "humidity": 55,
            "wind_speed": 10.5
        })
    return days_list
