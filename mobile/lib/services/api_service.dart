import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/weather_model.dart';

class ApiService {
  static const String baseUrl = 'http://10.0.2.2:8000/api/v1'; // 10.0.2.2 for Android Emulator to localhost

  static Future<WeatherData> fetchCurrentWeather(String city) async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/weather/current?city=$city')).timeout(const Duration(seconds: 5));
      if (response.statusCode == 200) {
        return WeatherData.fromJson(jsonDecode(response.body));
      }
    } catch (_) {}

    // Offline / Fallback Data
    return WeatherData(
      city: city,
      country: 'World',
      temp: 24.5,
      feelsLike: 25.0,
      humidity: 55,
      windSpeed: 11.4,
      pressure: 1014.0,
      uvIndex: 4.5,
      aqi: 28,
      aqiDescription: 'Good',
      condition: 'Partly Cloudy',
      rainProbability: 10,
      high: 26.0,
      low: 17.0,
    );
  }

  static Future<String> askGroqAI(String message, String city) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/ai/chat'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'message': message, 'city': city, 'current_temp': 24.5, 'condition': 'Partly Cloudy'}),
      ).timeout(const Duration(seconds: 5));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['response'] ?? 'SkySense AI: Weather conditions are favorable today.';
      }
    } catch (_) {}

    return 'SkySense AI: Weather in $city is clear with pleasant temperatures.';
  }
}
