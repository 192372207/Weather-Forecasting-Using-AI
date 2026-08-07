import 'package:flutter/material.dart';
import '../models/weather_model.dart';
import '../services/api_service.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  String selectedCity = 'London';
  late Future<WeatherData> _weatherFuture;
  final TextEditingController _searchController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _weatherFuture = ApiService.fetchCurrentWeather(selectedCity);
  }

  void _search() {
    if (_searchController.text.trim().isNotEmpty) {
      setState(() {
        selectedCity = _searchController.text.trim();
        _weatherFuture = ApiService.fetchCurrentWeather(selectedCity);
      });
      _searchController.clear();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0B1329),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Header Search Bar
              Container(
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.08),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: Colors.white.withOpacity(0.15)),
                ),
                child: TextField(
                  controller: _searchController,
                  onSubmitted: (_) => _search(),
                  style: const TextStyle(color: Colors.white, fontSize: 14),
                  decoration: InputDecoration(
                    hintText: 'Search city (e.g. London, Tokyo)...',
                    hintStyle: TextStyle(color: Colors.white.withOpacity(0.5)),
                    prefixIcon: const Icon(Icons.search, color: Colors.skyAccent),
                    suffixIcon: IconButton(
                      icon: const Icon(Icons.arrow_forward, color: Colors.skyAccent),
                      onPressed: _search,
                    ),
                    border: InputBorder.none,
                    contentPadding: const EdgeInsets.symmetric(vertical: 14),
                  ),
                ),
              ),

              const SizedBox(height: 20),

              // Weather Hero Card
              FutureBuilder<WeatherData>(
                future: _weatherFuture,
                builder: (context, snapshot) {
                  if (snapshot.connectionState == ConnectionState.waiting) {
                    return const Center(
                      child: Padding(
                        padding: EdgeInsets.all(30.0),
                        child: CircularProgressIndicator(color: Colors.skyAccent),
                      ),
                    );
                  }

                  final weather = snapshot.data!;

                  return Column(
                    children: [
                      Container(
                        width: double.infinity,
                        padding: const EdgeInsets.all(24),
                        decoration: BoxDecoration(
                          gradient: LinearGradient(
                            colors: [
                              Colors.sky.shade600.withOpacity(0.3),
                              Colors.indigo.shade900.withOpacity(0.4),
                            ],
                            begin: Alignment.topLeft,
                            end: Alignment.bottomRight,
                          ),
                          borderRadius: BorderRadius.circular(24),
                          border: Border.all(color: Colors.sky.withOpacity(0.3)),
                        ),
                        child: Column(
                          children: [
                            Text(
                              weather.city,
                              style: const TextStyle(
                                fontSize: 32,
                                fontWeight: FontWeight.bold,
                                color: Colors.white,
                              ),
                            ),
                            Text(
                              weather.condition,
                              style: TextStyle(
                                fontSize: 16,
                                color: Colors.sky.shade200,
                              ),
                            ),
                            const SizedBox(height: 16),
                            const Icon(Icons.wb_sunny_rounded, size: 72, color: Colors.amberAccent),
                            const SizedBox(height: 16),
                            Text(
                              '${weather.temp.round()}°C',
                              style: const TextStyle(
                                fontSize: 56,
                                fontWeight: FontWeight.extrabold,
                                color: Colors.white,
                              ),
                            ),
                            Text(
                              'Feels like ${weather.feelsLike.round()}°C • H: ${weather.high.round()}° L: ${weather.low.round()}°',
                              style: TextStyle(fontSize: 13, color: Colors.white.withOpacity(0.7)),
                            ),
                          ],
                        ),
                      ),

                      const SizedBox(height: 20),

                      // Weather Details Grid
                      GridView.count(
                        shrinkWrap: true,
                        physics: const NeverScrollableScrollPhysics(),
                        crossAxisCount: 2,
                        crossAxisSpacing: 12,
                        mainAxisSpacing: 12,
                        childAspectRatio: 1.5,
                        children: [
                          _buildDetailCard('WIND SPEED', '${weather.windSpeed} km/h', Icons.air, Colors.skyAccent),
                          _buildDetailCard('HUMIDITY', '${weather.humidity}%', Icons.water_drop, Colors.cyanAccent),
                          _buildDetailCard('PRESSURE', '${weather.pressure} hPa', Icons.speed, Colors.indigoAccent),
                          _buildDetailCard('AIR QUALITY', '${weather.aqi} AQI', Icons.wb_twilight, Colors.emeraldAccent),
                        ],
                      ),
                    ],
                  );
                },
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildDetailCard(String title, String val, IconData icon, Color iconColor) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.05),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.white.withOpacity(0.1)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Row(
            children: [
              Icon(icon, size: 18, color: iconColor),
              const SizedBox(width: 8),
              Text(
                title,
                style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: Colors.white.withOpacity(0.5)),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Text(
            val,
            style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white),
          ),
        ],
      ),
    );
  }
}
