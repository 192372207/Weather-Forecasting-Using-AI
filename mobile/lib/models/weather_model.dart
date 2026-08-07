class WeatherData {
  final String city;
  final String country;
  final double temp;
  final double feelsLike;
  final int humidity;
  final double windSpeed;
  final double pressure;
  final double uvIndex;
  final int aqi;
  final String aqiDescription;
  final String condition;
  final int rainProbability;
  final double high;
  final double low;

  WeatherData({
    required this.city,
    required this.country,
    required this.temp,
    required this.feelsLike,
    required this.humidity,
    required this.windSpeed,
    required this.pressure,
    required this.uvIndex,
    required this.aqi,
    required this.aqiDescription,
    required this.condition,
    required this.rainProbability,
    required this.high,
    required this.low,
  });

  factory WeatherData.fromJson(Map<String, dynamic> json) {
    return WeatherData(
      city: json['city'] ?? 'London',
      country: json['country'] ?? 'UK',
      temp: (json['temp'] as num?)?.toDouble() ?? 22.0,
      feelsLike: (json['feels_like'] as num?)?.toDouble() ?? 22.5,
      humidity: json['humidity'] ?? 58,
      windSpeed: (json['wind_speed'] as num?)?.toDouble() ?? 12.0,
      pressure: (json['pressure'] as num?)?.toDouble() ?? 1013.2,
      uvIndex: (json['uv_index'] as num?)?.toDouble() ?? 5.0,
      aqi: json['aqi'] ?? 35,
      aqiDescription: json['aqi_description'] ?? 'Good',
      condition: json['condition'] ?? 'Clear Sky',
      rainProbability: json['rain_probability'] ?? 15,
      high: (json['high'] as num?)?.toDouble() ?? 25.0,
      low: (json['low'] as num?)?.toDouble() ?? 16.0,
    );
  }
}
