import 'package:flutter/material.dart';
import '../services/api_service.dart';

class AiAssistantScreen extends StatefulWidget {
  const AiAssistantScreen({super.key});

  @override
  State<AiAssistantScreen> createState() => _AiAssistantScreenState();
}

class _AiAssistantScreenState extends State<AiAssistantScreen> {
  final List<Map<String, String>> _messages = [
    {
      'sender': 'ai',
      'text': '🌤️ Welcome to SkySense AI Safety Assistant!\n\nI analyze live weather telemetry to keep you safe. Ask me about travel safety, rain risk, clothing, farming, or emergency advisories.',
      'risk': 'Green'
    }
  ];
  final TextEditingController _controller = TextEditingController();
  bool _loading = false;
  String _selectedLang = 'en';

  final List<String> _quickQuestions = [
    'Is it safe to travel today?',
    'Will it rain today?',
    'Should I carry an umbrella?',
    'Is there any cyclone warning?',
    'Is today safe for outdoor exercise?',
    'What precautions should I take today?'
  ];

  void _sendMessage([String? customText]) async {
    final text = customText ?? _controller.text.trim();
    if (text.isEmpty || _loading) return;

    setState(() {
      _messages.add({'sender': 'user', 'text': text});
      _loading = true;
    });
    _controller.clear();

    final response = await ApiService.askGroqAI(text, 'London');

    setState(() {
      _messages.add({
        'sender': 'ai',
        'text': response,
        'risk': text.toLowerCase().contains('cyclone') ? 'Red' : 'Green'
      });
      _loading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0B1329),
      appBar: AppBar(
        backgroundColor: const Color(0xFF0B1329),
        title: const Row(
          children: [
            Icon(Icons.auto_awesome, color: Colors.skyAccent, size: 20),
            SizedBox(width: 8),
            Text('SkySense AI Safety Assistant', style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
          ],
        ),
        elevation: 0,
      ),
      body: Column(
        children: [
          // Risk Level Indicator Banner
          Container(
            width: double.infinity,
            margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            decoration: BoxDecoration(
              color: Colors.emerald.withOpacity(0.15),
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: Colors.emerald.withOpacity(0.4)),
            ),
            child: const Row(
              children: [
                Icon(Icons.shield_outlined, color: Colors.emeraldAccent, size: 22),
                SizedBox(width: 10),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('RISK METER: 🟢 SAFE CONDITIONS', style: TextStyle(color: Colors.emeraldAccent, fontWeight: FontWeight.bold, fontSize: 12)),
                      Text('No severe storms or AQI hazards active for your location.', style: TextStyle(color: Colors.white70, fontSize: 11)),
                    ],
                  ),
                ),
              ],
            ),
          ),

          // Chat Messages List
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _messages.length,
              itemBuilder: (context, idx) {
                final msg = _messages[idx];
                final isUser = msg['sender'] == 'user';
                return Align(
                  alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
                  child: Container(
                    margin: const EdgeInsets.only(bottom: 12),
                    padding: const EdgeInsets.all(16),
                    constraints: const BoxConstraints(maxWidth: 310),
                    decoration: BoxDecoration(
                      color: isUser ? Colors.sky.shade600 : Colors.white.withOpacity(0.08),
                      borderRadius: BorderRadius.circular(20),
                      border: Border.all(color: isUser ? Colors.skyAccent : Colors.white.withOpacity(0.1)),
                    ),
                    child: Text(
                      msg['text']!,
                      style: const TextStyle(color: Colors.white, fontSize: 13, height: 1.4),
                    ),
                  ),
                );
              },
            ),
          ),

          // Quick Prompt Shortcuts
          SizedBox(
            height: 40,
            child: ListView.builder(
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.symmetric(horizontal: 16),
              itemCount: _quickQuestions.length,
              itemBuilder: (context, idx) {
                final q = _quickQuestions[idx];
                return Padding(
                  padding: const EdgeInsets.only(right: 8.0),
                  child: ActionChip(
                    backgroundColor: Colors.white.withOpacity(0.08),
                    side: BorderSide(color: Colors.sky.withOpacity(0.3)),
                    label: Text(q, style: const TextStyle(color: Colors.skyAccent, fontSize: 11)),
                    onPressed: () => _sendMessage(q),
                  ),
                );
              },
            ),
          ),
          const SizedBox(height: 8),

          if (_loading)
            const Padding(
              padding: EdgeInsets.all(8.0),
              child: CircularProgressIndicator(color: Colors.skyAccent),
            ),

          // Input Bar with Mic Button
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.05),
              border: Border(top: BorderSide(color: Colors.white.withOpacity(0.1))),
            ),
            child: Row(
              children: [
                IconButton(
                  icon: const Icon(Icons.mic, color: Colors.skyAccent),
                  onPressed: () => _sendMessage('Is it safe to travel today?'),
                ),
                Expanded(
                  child: TextField(
                    controller: _controller,
                    style: const TextStyle(color: Colors.white, fontSize: 14),
                    decoration: const InputDecoration(
                      hintText: 'Ask safety advice...',
                      hintStyle: TextStyle(color: Colors.white38),
                      border: InputBorder.none,
                    ),
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.send, color: Colors.skyAccent),
                  onPressed: () => _sendMessage(),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
