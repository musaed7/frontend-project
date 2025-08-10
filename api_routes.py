from flask import Blueprint, jsonify, request
from datetime import datetime
import json

# Create API blueprint
api_bp = Blueprint('api', __name__)

# Mock data - replace with your actual database queries
MOCK_STATS = {
    "totalViews": 54750,
    "totalRevenue": 1652.70,
    "totalFollowers": 90670,
    "contentGenerated": 65,
    "publishedToday": 17,
    "pendingPreviews": 8,
    "scheduledContent": 25
}

MOCK_CHANNELS = [
    {
        "id": "horror_stories",
        "name": "قصص الرعب",
        "platform": "TikTok",
        "status": "active",
        "followers": 15420,
        "todayViews": 8750,
        "revenue": 245.50,
        "contentGenerated": 12,
        "publishedToday": 3
    },
    {
        "id": "islamic_stories",
        "name": "القصص الإسلامية",
        "platform": "TikTok",
        "status": "active",
        "followers": 22100,
        "todayViews": 12300,
        "revenue": 380.75,
        "contentGenerated": 15,
        "publishedToday": 4
    },
    {
        "id": "home_design",
        "name": "تصميم المنازل والعقارات",
        "platform": "YouTube",
        "status": "active",
        "followers": 8900,
        "todayViews": 5600,
        "revenue": 195.25,
        "contentGenerated": 8,
        "publishedToday": 2
    },
    {
        "id": "motivation",
        "name": "التحفيز والاقتباسات",
        "platform": "TikTok",
        "status": "active",
        "followers": 31500,
        "todayViews": 18900,
        "revenue": 520.80,
        "contentGenerated": 20,
        "publishedToday": 5
    },
    {
        "id": "ai_chef",
        "name": "AI Chef",
        "platform": "YouTube",
        "status": "active",
        "followers": 12750,
        "todayViews": 9200,
        "revenue": 310.40,
        "contentGenerated": 10,
        "publishedToday": 3
    }
]

MOCK_PREVIEWS = [
    {
        "id": "preview_1",
        "channelId": "horror_stories",
        "title": "قصة الدمية المسكونة",
        "content": "في منزل قديم بالريف، وجدت سارة دمية قديمة في العلية...",
        "scheduledTime": "22:00",
        "timeLeft": "45 دقيقة",
        "mediaType": "video"
    },
    {
        "id": "preview_2",
        "channelId": "ai_chef",
        "title": "وصفة المعكرونة الإيطالية",
        "content": "اليوم سنتعلم طريقة عمل المعكرونة الإيطالية الأصلية...",
        "scheduledTime": "22:15",
        "timeLeft": "60 دقيقة",
        "mediaType": "video"
    },
    {
        "id": "preview_3",
        "channelId": "motivation",
        "title": "اقتباس عن النجاح",
        "content": "النجاح ليس نهاية الطريق، والفشل ليس نهاية العالم...",
        "scheduledTime": "22:30",
        "timeLeft": "75 دقيقة",
        "mediaType": "image"
    }
]

# System state
system_running = True

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "message": "AI Content Automation Backend is running",
        "version": "1.0.0"
    })

@api_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get dashboard statistics"""
    return jsonify(MOCK_STATS)

@api_bp.route('/channels', methods=['GET'])
def get_channels():
    """Get all channels data"""
    return jsonify(MOCK_CHANNELS)

@api_bp.route('/channels/<channel_id>', methods=['GET'])
def get_channel(channel_id):
    """Get specific channel data"""
    channel = next((c for c in MOCK_CHANNELS if c['id'] == channel_id), None)
    if not channel:
        return jsonify({"error": "Channel not found"}), 404
    return jsonify(channel)

@api_bp.route('/previews', methods=['GET'])
def get_previews():
    """Get pending content previews"""
    return jsonify(MOCK_PREVIEWS)

@api_bp.route('/content/<content_id>/approve', methods=['POST'])
def approve_content(content_id):
    """Approve content for publishing"""
    global MOCK_PREVIEWS
    
    # Find and remove the content from previews
    content = next((p for p in MOCK_PREVIEWS if p['id'] == content_id), None)
    if not content:
        return jsonify({"error": "Content not found"}), 404
    
    # Remove from previews list
    MOCK_PREVIEWS = [p for p in MOCK_PREVIEWS if p['id'] != content_id]
    
    # Here you would typically:
    # 1. Add content to publication queue
    # 2. Update database
    # 3. Schedule actual posting
    
    return jsonify({
        "status": "approved",
        "content_id": content_id,
        "message": f"Content '{content['title']}' approved for publishing",
        "scheduled_time": content['scheduledTime']
    })

@api_bp.route('/content/<content_id>/reject', methods=['POST'])
def reject_content(content_id):
    """Reject content"""
    global MOCK_PREVIEWS
    
    # Find and remove the content from previews
    content = next((p for p in MOCK_PREVIEWS if p['id'] == content_id), None)
    if not content:
        return jsonify({"error": "Content not found"}), 404
    
    # Remove from previews list
    MOCK_PREVIEWS = [p for p in MOCK_PREVIEWS if p['id'] != content_id]
    
    # Here you would typically:
    # 1. Log rejection reason
    # 2. Update database
    # 3. Optionally regenerate content
    
    return jsonify({
        "status": "rejected",
        "content_id": content_id,
        "message": f"Content '{content['title']}' rejected"
    })

@api_bp.route('/system/toggle', methods=['POST'])
def toggle_system():
    """Toggle system running state"""
    global system_running
    
    data = request.get_json()
    if data and 'running' in data:
        system_running = data['running']
    else:
        system_running = not system_running
    
    return jsonify({
        "status": "success",
        "system_running": system_running,
        "message": f"System {'started' if system_running else 'stopped'}",
        "timestamp": datetime.now().isoformat()
    })

@api_bp.route('/system/status', methods=['GET'])
def get_system_status():
    """Get current system status"""
    return jsonify({
        "system_running": system_running,
        "uptime": "2 hours 15 minutes",  # You can calculate actual uptime
        "last_content_generated": datetime.now().isoformat(),
        "next_preview_time": "21:00",
        "next_publish_time": "22:00",
        "active_channels": len([c for c in MOCK_CHANNELS if c['status'] == 'active']),
        "pending_previews": len(MOCK_PREVIEWS)
    })

@api_bp.route('/content/generate', methods=['POST'])
def generate_content():
    """Generate new content for a specific channel"""
    data = request.get_json()
    
    if not data or 'channel_id' not in data:
        return jsonify({"error": "Channel ID required"}), 400
    
    channel_id = data['channel_id']
    
    # Find the channel
    channel = next((c for c in MOCK_CHANNELS if c['id'] == channel_id), None)
    if not channel:
        return jsonify({"error": "Channel not found"}), 404
    
    # Here you would typically:
    # 1. Call your AI content generation
    # 2. Create new content based on channel type
    # 3. Add to preview queue
    
    new_content = {
        "id": f"preview_{len(MOCK_PREVIEWS) + 1}",
        "channelId": channel_id,
        "title": f"محتوى جديد - {channel['name']}",
        "content": "محتوى تم توليده بواسطة الذكاء الاصطناعي...",
        "scheduledTime": "22:30",
        "timeLeft": "90 دقيقة",
        "mediaType": "video" if channel['platform'] == 'YouTube' else "image"
    }
    
    MOCK_PREVIEWS.append(new_content)
    
    return jsonify({
        "status": "success",
        "message": "Content generated successfully",
        "content": new_content
    })

@api_bp.route('/analytics/<channel_id>', methods=['GET'])
def get_channel_analytics(channel_id):
    """Get analytics for specific channel"""
    channel = next((c for c in MOCK_CHANNELS if c['id'] == channel_id), None)
    if not channel:
        return jsonify({"error": "Channel not found"}), 404
    
    # Mock analytics data
    analytics = {
        "channel_id": channel_id,
        "channel_name": channel['name'],
        "daily_stats": {
            "views": channel['todayViews'],
            "revenue": channel['revenue'],
            "content_published": channel['publishedToday'],
            "engagement_rate": 0.85
        },
        "weekly_trend": [
            {"day": "الأحد", "views": 5200, "revenue": 180},
            {"day": "الإثنين", "views": 6800, "revenue": 220},
            {"day": "الثلاثاء", "views": 7200, "revenue": 245},
            {"day": "الأربعاء", "views": 8100, "revenue": 280},
            {"day": "الخميس", "views": 8750, "revenue": 310},
            {"day": "الجمعة", "views": 9200, "revenue": 340},
            {"day": "السبت", "views": channel['todayViews'], "revenue": channel['revenue']}
        ]
    }
    
    return jsonify(analytics)

@api_bp.route('/config', methods=['GET'])
def get_config():
    """Get system configuration"""
    return jsonify({
        "preview_time": "21:00-22:00",
        "auto_publish_time": "22:00",
        "timezone": "UTC+3",
        "content_generation_enabled": system_running,
        "max_content_length": 500,
        "min_content_length": 100,
        "active_ai_provider": "gemini",
        "fallback_providers": ["deepseek", "openai"]
    })

@api_bp.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@api_bp.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500
