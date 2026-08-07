import 'package:flutter/material.dart';

class CommunityScreen extends StatelessWidget {
  const CommunityScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0B1329),
      appBar: AppBar(
        backgroundColor: const Color(0xFF0B1329),
        title: const Text('Community Weather Reports', style: TextStyle(color: Colors.white, fontSize: 16)),
        elevation: 0,
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _buildReportCard('Elena Rostova', 'Paris', 'Heavy Rain', 'Heavy rainfall near Eiffel Tower area.', 14),
          _buildReportCard('Marcus Vance', 'Sydney', 'Storm', 'High winds approaching Darling Harbour.', 29),
        ],
      ),
    );
  }

  Widget _buildReportCard(String user, String city, String type, String desc, int likes) {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.05),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.white.withOpacity(0.1)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.between,
            children: [
              Text(user, style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white)),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: Colors.amber.withOpacity(0.2),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(type, style: const TextStyle(fontSize: 11, color: Colors.amberAccent, fontWeight: FontWeight.bold)),
              ),
            ],
          ),
          const SizedBox(height: 4),
          Text(city, style: TextStyle(fontSize: 12, color: Colors.white.withOpacity(0.6))),
          const SizedBox(height: 10),
          Text(desc, style: const TextStyle(fontSize: 13, color: Colors.white70)),
          const SizedBox(height: 12),
          Row(
            children: [
              const Icon(Icons.thumb_up_alt_outlined, size: 16, color: Colors.skyAccent),
              const SizedBox(width: 6),
              Text('$likes Likes', style: const TextStyle(fontSize: 12, color: Colors.skyAccent)),
            ],
          ),
        ],
      ),
    );
  }
}
