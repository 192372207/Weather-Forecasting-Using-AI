import React, { createContext, useContext, useState, useEffect } from 'react';
import { weatherApi } from '../services/api';

const WeatherContext = createContext();

export const WeatherProvider = ({ children }) => {
  const [city, setCity] = useState('London');
  const [unit, setUnit] = useState('C'); // 'C' or 'F'
  const [theme, setTheme] = useState('dark'); // 'dark' or 'light'
  const [weather, setWeather] = useState(null);
  const [hourly, setHourly] = useState([]);
  const [daily7, setDaily7] = useState([]);
  const [daily15, setDaily15] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isGpsActive, setIsGpsActive] = useState(false);

  const fetchWeather = async (targetCity) => {
    setLoading(true);
    try {
      const cur = await weatherApi.getCurrent(targetCity);
      if (cur) setWeather(cur);

      const h = await weatherApi.getHourly(targetCity);
      setHourly(h);

      const d7 = await weatherApi.getDaily(targetCity, 7);
      setDaily7(d7);

      const d15 = await weatherApi.getDaily(targetCity, 15);
      setDaily15(d15);
    } catch (err) {
      console.error("Weather fetch error", err);
    } finally {
      setLoading(false);
    }
  };

  const fetchByGPS = () => {
    if (navigator.geolocation) {
      setLoading(true);
      navigator.geolocation.getCurrentPosition(
        async (position) => {
          const { latitude, longitude } = position.coords;
          const liveData = await weatherApi.getByCoords(latitude, longitude);
          if (liveData) {
            setWeather(liveData);
            setCity(liveData.city);
            setIsGpsActive(true);

            // Fetch forecast for detected city
            const h = await weatherApi.getHourly(liveData.city);
            setHourly(h);
            const d7 = await weatherApi.getDaily(liveData.city, 7);
            setDaily7(d7);
            const d15 = await weatherApi.getDaily(liveData.city, 15);
            setDaily15(d15);
          } else {
            fetchWeather(city);
          }
          setLoading(false);
        },
        (error) => {
          console.warn("GPS Permission denied or unavailable, defaulting to city search.", error);
          fetchWeather(city);
        },
        { timeout: 10000 }
      );
    } else {
      fetchWeather(city);
    }
  };

  // Initial load: Attempt GPS auto-detection
  useEffect(() => {
    fetchByGPS();
  }, []);

  const changeCity = (newCity) => {
    setIsGpsActive(false);
    setCity(newCity);
    fetchWeather(newCity);
  };

  const toggleTheme = () => {
    const next = theme === 'dark' ? 'light' : 'dark';
    setTheme(next);
    if (next === 'light') {
      document.documentElement.classList.remove('dark');
      document.documentElement.classList.add('light');
    } else {
      document.documentElement.classList.remove('light');
      document.documentElement.classList.add('dark');
    }
  };

  const convertTemp = (tempC) => {
    if (tempC === undefined || tempC === null) return '--';
    if (unit === 'F') {
      return Math.round((tempC * 9/5) + 32);
    }
    return Math.round(tempC);
  };

  return (
    <WeatherContext.Provider value={{
      city,
      setCity: changeCity,
      unit,
      setUnit,
      theme,
      toggleTheme,
      weather,
      hourly,
      daily7,
      daily15,
      loading,
      isGpsActive,
      detectGPSLocation: fetchByGPS,
      refreshWeather: () => fetchWeather(city),
      convertTemp
    }}>
      {children}
    </WeatherContext.Provider>
  );
};

export const useWeather = () => useContext(WeatherContext);
