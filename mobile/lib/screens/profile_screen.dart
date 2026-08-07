import 'package:flutter/material.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0B1329),
      appBar: AppBar(
        backgroundColor: const Color(0xFF0B1329),
        title: const Text('SkySense User Profile', style: TextStyle(color: Colors.white, fontSize: 16)),
        elevation: 0,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            const CircleAvatar(
              radius: 40,
              backgroundColor: Colors.skyAccent,
              child: Icon(Icons.person, size: 40, color: Colors.white),
            ),
            const SizedBox(height: 12),
            const Text('Alex Vance', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white)),
            Text('alex@skysense.ai', style: TextStyle(fontSize: 12, color: Colors.white.withOpacity(0.6))),
            const SizedBox(height: 24),
            ListTile(
              leading: const Icon(Icons.notifications_active, color: Colors.skyAccent),
              title: const Text('Push Notifications', style: TextStyle(color: Colors.white)),
              trailing: Switch(value: true, onChanged: (_) {}),
            ),
            ListTile(
              leading: const Icon(Icons.thermostat, color: Colors.amberAccent),
              title: const Text('Temperature Unit', style: TextStyle(color: Colors.white)),
              trailing: const Text('Celsius (°C)', style: TextStyle(color: Colors.skyAccent)),
            ),
          ],
        ),
      ),
    );
  }
}
