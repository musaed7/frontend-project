"""
Preview and Scheduling System for AI Content Automation
Handles content preview between 9-10 PM and automatic publishing after 10 PM
"""

import json
import os
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
import logging
from dataclasses import dataclass, asdict
from enum import Enum
import schedule

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentStatus(Enum):
    DRAFT = "draft"
    PREVIEW = "preview"
    APPROVED = "approved"
    REJECTED = "rejected"
    PUBLISHED = "published"
    FAILED = "failed"

@dataclass
class ScheduledContent:
    """Represents scheduled content with preview and publishing information"""
    id: str
    channel_id: str
    title: str
    content: str
    hashtags: List[str]
    media_files: Dict[str, str]
    created_at: datetime
    status: ContentStatus
    scheduled_time: Optional[datetime] = None
    preview_deadline: Optional[datetime] = None
    auto_publish_time: Optional[datetime] = None
    approval_user: Optional[str] = None
    rejection_reason: Optional[str] = None
    publish_attempts: int = 0
    max_publish_attempts: int = 3

class PreviewNotificationSystem:
    """Handles notifications for content preview"""
    
    def __init__(self):
        self.notification_callbacks = []
        
    def add_notification_callback(self, callback: Callable):
        """Add a callback function for notifications"""
        self.notification_callbacks.append(callback)
    
    def notify_preview_available(self, content: ScheduledContent):
        """Notify that content is available for preview"""
        message = f"محتوى جديد متاح للمعاينة: {content.title} (قناة: {content.channel_id})"
        self._send_notification("preview_available", message, content)
    
    def notify_preview_deadline_approaching(self, content: ScheduledContent, minutes_left: int):
        """Notify that preview deadline is approaching"""
        message = f"تنتهي فترة المعاينة خلال {minutes_left} دقيقة للمحتوى: {content.title}"
        self._send_notification("preview_deadline", message, content)
    
    def notify_auto_publish_scheduled(self, content: ScheduledContent):
        """Notify that content will be auto-published"""
        message = f"سيتم نشر المحتوى تلقائياً: {content.title} في {content.auto_publish_time.strftime('%H:%M')}"
        self._send_notification("auto_publish", message, content)
    
    def notify_content_published(self, content: ScheduledContent, success: bool):
        """Notify about publishing result"""
        if success:
            message = f"تم نشر المحتوى بنجاح: {content.title}"
            self._send_notification("publish_success", message, content)
        else:
            message = f"فشل في نشر المحتوى: {content.title}"
            self._send_notification("publish_failed", message, content)
    
    def _send_notification(self, notification_type: str, message: str, content: ScheduledContent):
        """Send notification to all registered callbacks"""
        notification_data = {
            'type': notification_type,
            'message': message,
            'content_id': content.id,
            'channel_id': content.channel_id,
            'timestamp': datetime.now().isoformat()
        }
        
        for callback in self.notification_callbacks:
            try:
                callback(notification_data)
            except Exception as e:
                logger.error(f"Error in notification callback: {e}")

class ContentPreviewManager:
    """Manages content preview workflow"""
    
    def __init__(self, preview_start_time: str = "21:00", preview_end_time: str = "22:00"):
        self.preview_start = preview_start_time
        self.preview_end = preview_end_time
        self.pending_content: Dict[str, ScheduledContent] = {}
        self.notification_system = PreviewNotificationSystem()
        
        # Storage paths
        self.storage_dir = "/home/ubuntu/ai_content_automation_enhanced/src/data"
        self.preview_file = os.path.join(self.storage_dir, "pending_previews.json")
        
        # Ensure storage directory exists
        os.makedirs(self.storage_dir, exist_ok=True)
        
        # Load existing pending content
        self._load_pending_content()
    
    def add_content_for_preview(self, content: ScheduledContent) -> bool:
        """Add content to preview queue"""
        try:
            # Set preview deadline and auto-publish time
            now = datetime.now()
            today = now.date()
            
            # Calculate preview deadline (end of preview window today or tomorrow)
            preview_end_today = datetime.combine(today, datetime.strptime(self.preview_end, "%H:%M").time())
            
            if now < preview_end_today:
                # Preview window is today
                content.preview_deadline = preview_end_today
            else:
                # Preview window is tomorrow
                tomorrow = today + timedelta(days=1)
                content.preview_deadline = datetime.combine(tomorrow, datetime.strptime(self.preview_end, "%H:%M").time())
            
            # Set auto-publish time (same as preview deadline)
            content.auto_publish_time = content.preview_deadline
            
            # Update status
            content.status = ContentStatus.PREVIEW
            
            # Add to pending content
            self.pending_content[content.id] = content
            
            # Save to storage
            self._save_pending_content()
            
            # Notify about new preview
            self.notification_system.notify_preview_available(content)
            
            logger.info(f"Content {content.id} added to preview queue. Deadline: {content.preview_deadline}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding content to preview: {e}")
            return False
    
    def get_pending_previews(self) -> List[ScheduledContent]:
        """Get all content pending preview"""
        return [content for content in self.pending_content.values() 
                if content.status == ContentStatus.PREVIEW]
    
    def get_content_by_id(self, content_id: str) -> Optional[ScheduledContent]:
        """Get specific content by ID"""
        return self.pending_content.get(content_id)
    
    def approve_content(self, content_id: str, user: str = "system") -> bool:
        """Approve content for publishing"""
        try:
            if content_id not in self.pending_content:
                logger.warning(f"Content {content_id} not found for approval")
                return False
            
            content = self.pending_content[content_id]
            content.status = ContentStatus.APPROVED
            content.approval_user = user
            
            # Save changes
            self._save_pending_content()
            
            logger.info(f"Content {content_id} approved by {user}")
            return True
            
        except Exception as e:
            logger.error(f"Error approving content {content_id}: {e}")
            return False
    
    def reject_content(self, content_id: str, reason: str = "", user: str = "system") -> bool:
        """Reject content"""
        try:
            if content_id not in self.pending_content:
                logger.warning(f"Content {content_id} not found for rejection")
                return False
            
            content = self.pending_content[content_id]
            content.status = ContentStatus.REJECTED
            content.rejection_reason = reason
            content.approval_user = user
            
            # Save changes
            self._save_pending_content()
            
            logger.info(f"Content {content_id} rejected by {user}: {reason}")
            return True
            
        except Exception as e:
            logger.error(f"Error rejecting content {content_id}: {e}")
            return False
    
    def is_preview_time(self) -> bool:
        """Check if current time is within preview window"""
        now = datetime.now().time()
        start_time = datetime.strptime(self.preview_start, "%H:%M").time()
        end_time = datetime.strptime(self.preview_end, "%H:%M").time()
        
        return start_time <= now <= end_time
    
    def process_expired_previews(self):
        """Process content that has passed preview deadline"""
        now = datetime.now()
        
        for content_id, content in list(self.pending_content.items()):
            if (content.status == ContentStatus.PREVIEW and 
                content.preview_deadline and 
                now > content.preview_deadline):
                
                # Auto-approve expired content
                content.status = ContentStatus.APPROVED
                content.approval_user = "auto_system"
                
                logger.info(f"Auto-approved expired content: {content_id}")
                
                # Schedule for immediate publishing
                self.notification_system.notify_auto_publish_scheduled(content)
        
        # Save changes
        self._save_pending_content()
    
    def get_approved_content(self) -> List[ScheduledContent]:
        """Get all approved content ready for publishing"""
        return [content for content in self.pending_content.values() 
                if content.status == ContentStatus.APPROVED]
    
    def mark_content_published(self, content_id: str, success: bool = True):
        """Mark content as published or failed"""
        try:
            if content_id not in self.pending_content:
                return False
            
            content = self.pending_content[content_id]
            
            if success:
                content.status = ContentStatus.PUBLISHED
                # Remove from pending content after successful publish
                del self.pending_content[content_id]
                logger.info(f"Content {content_id} marked as published")
            else:
                content.status = ContentStatus.FAILED
                content.publish_attempts += 1
                logger.warning(f"Content {content_id} failed to publish (attempt {content.publish_attempts})")
            
            # Save changes
            self._save_pending_content()
            
            # Notify about publishing result
            self.notification_system.notify_content_published(content, success)
            
            return True
            
        except Exception as e:
            logger.error(f"Error marking content as published: {e}")
            return False
    
    def cleanup_old_content(self, days_old: int = 7):
        """Clean up old content from storage"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_old)
            
            to_remove = []
            for content_id, content in self.pending_content.items():
                if content.created_at < cutoff_date:
                    to_remove.append(content_id)
            
            for content_id in to_remove:
                del self.pending_content[content_id]
                logger.info(f"Cleaned up old content: {content_id}")
            
            if to_remove:
                self._save_pending_content()
            
        except Exception as e:
            logger.error(f"Error cleaning up old content: {e}")
    
    def _save_pending_content(self):
        """Save pending content to storage"""
        try:
            # Convert to serializable format
            data = {}
            for content_id, content in self.pending_content.items():
                content_dict = asdict(content)
                # Convert datetime objects to ISO strings
                for key, value in content_dict.items():
                    if isinstance(value, datetime):
                        content_dict[key] = value.isoformat()
                    elif isinstance(value, ContentStatus):
                        content_dict[key] = value.value
                data[content_id] = content_dict
            
            with open(self.preview_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving pending content: {e}")
    
    def _load_pending_content(self):
        """Load pending content from storage"""
        try:
            if not os.path.exists(self.preview_file):
                return
            
            with open(self.preview_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for content_id, content_dict in data.items():
                # Convert ISO strings back to datetime objects
                for key, value in content_dict.items():
                    if key in ['created_at', 'scheduled_time', 'preview_deadline', 'auto_publish_time'] and value:
                        content_dict[key] = datetime.fromisoformat(value)
                    elif key == 'status':
                        content_dict[key] = ContentStatus(value)
                
                self.pending_content[content_id] = ScheduledContent(**content_dict)
                
        except Exception as e:
            logger.error(f"Error loading pending content: {e}")

class AutoPublisher:
    """Handles automatic publishing of approved content"""
    
    def __init__(self, preview_manager: ContentPreviewManager):
        self.preview_manager = preview_manager
        self.publishing_callbacks = []
        
    def add_publishing_callback(self, callback: Callable):
        """Add a callback function for publishing content"""
        self.publishing_callbacks.append(callback)
    
    def publish_approved_content(self):
        """Publish all approved content"""
        approved_content = self.preview_manager.get_approved_content()
        
        for content in approved_content:
            try:
                # Check if it's time to publish
                now = datetime.now()
                if content.auto_publish_time and now >= content.auto_publish_time:
                    success = self._publish_content(content)
                    self.preview_manager.mark_content_published(content.id, success)
                    
            except Exception as e:
                logger.error(f"Error publishing content {content.id}: {e}")
                self.preview_manager.mark_content_published(content.id, False)
    
    def _publish_content(self, content: ScheduledContent) -> bool:
        """Publish individual content item"""
        try:
            # Call all registered publishing callbacks
            for callback in self.publishing_callbacks:
                try:
                    result = callback(content)
                    if not result:
                        logger.warning(f"Publishing callback failed for content {content.id}")
                        return False
                except Exception as e:
                    logger.error(f"Error in publishing callback: {e}")
                    return False
            
            logger.info(f"Successfully published content: {content.id}")
            return True
            
        except Exception as e:
            logger.error(f"Error publishing content {content.id}: {e}")
            return False

class SchedulerService:
    """Main scheduler service that coordinates preview and publishing"""
    
    def __init__(self, preview_start: str = "21:00", preview_end: str = "22:00"):
        self.preview_manager = ContentPreviewManager(preview_start, preview_end)
        self.auto_publisher = AutoPublisher(self.preview_manager)
        self.running = False
        self.scheduler_thread = None
        
        # Set up scheduled tasks
        self._setup_scheduled_tasks()
    
    def _setup_scheduled_tasks(self):
        """Set up scheduled tasks"""
        # Check for expired previews every minute
        schedule.every(1).minutes.do(self.preview_manager.process_expired_previews)
        
        # Publish approved content every 5 minutes
        schedule.every(5).minutes.do(self.auto_publisher.publish_approved_content)
        
        # Clean up old content daily at midnight
        schedule.every().day.at("00:00").do(self.preview_manager.cleanup_old_content)
        
        # Send preview deadline reminders
        schedule.every(10).minutes.do(self._check_preview_deadlines)
    
    def _check_preview_deadlines(self):
        """Check for approaching preview deadlines"""
        now = datetime.now()
        
        for content in self.preview_manager.get_pending_previews():
            if content.preview_deadline:
                time_left = content.preview_deadline - now
                minutes_left = int(time_left.total_seconds() / 60)
                
                # Notify when 30, 15, or 5 minutes left
                if minutes_left in [30, 15, 5]:
                    self.preview_manager.notification_system.notify_preview_deadline_approaching(
                        content, minutes_left
                    )
    
    def start(self):
        """Start the scheduler service"""
        if self.running:
            logger.warning("Scheduler service is already running")
            return
        
        self.running = True
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        logger.info("Scheduler service started")
    
    def stop(self):
        """Stop the scheduler service"""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        logger.info("Scheduler service stopped")
    
    def _run_scheduler(self):
        """Run the scheduler in a separate thread"""
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(30)  # Check every 30 seconds
            except Exception as e:
                logger.error(f"Error in scheduler: {e}")
                time.sleep(60)  # Wait longer on error
    
    def add_content_for_preview(self, content: ScheduledContent) -> bool:
        """Add content to preview queue"""
        return self.preview_manager.add_content_for_preview(content)
    
    def get_pending_previews(self) -> List[ScheduledContent]:
        """Get all content pending preview"""
        return self.preview_manager.get_pending_previews()
    
    def approve_content(self, content_id: str, user: str = "system") -> bool:
        """Approve content for publishing"""
        return self.preview_manager.approve_content(content_id, user)
    
    def reject_content(self, content_id: str, reason: str = "", user: str = "system") -> bool:
        """Reject content"""
        return self.preview_manager.reject_content(content_id, reason, user)
    
    def add_notification_callback(self, callback: Callable):
        """Add notification callback"""
        self.preview_manager.notification_system.add_notification_callback(callback)
    
    def add_publishing_callback(self, callback: Callable):
        """Add publishing callback"""
        self.auto_publisher.add_publishing_callback(callback)
    
    def get_system_status(self) -> Dict:
        """Get system status information"""
        pending_previews = self.get_pending_previews()
        approved_content = self.preview_manager.get_approved_content()
        
        return {
            'running': self.running,
            'preview_window': {
                'start': self.preview_manager.preview_start,
                'end': self.preview_manager.preview_end,
                'is_active': self.preview_manager.is_preview_time()
            },
            'content_stats': {
                'pending_previews': len(pending_previews),
                'approved_content': len(approved_content),
                'total_managed': len(self.preview_manager.pending_content)
            },
            'next_deadlines': [
                {
                    'content_id': content.id,
                    'title': content.title,
                    'deadline': content.preview_deadline.isoformat() if content.preview_deadline else None
                }
                for content in pending_previews[:5]  # Show next 5 deadlines
            ]
        }

# Example usage and testing
if __name__ == "__main__":
    # Initialize scheduler service
    scheduler = SchedulerService()
    
    # Add notification callback
    def notification_handler(notification_data):
        print(f"Notification: {notification_data['message']}")
    
    scheduler.add_notification_callback(notification_handler)
    
    # Add publishing callback
    def publishing_handler(content: ScheduledContent) -> bool:
        print(f"Publishing content: {content.title} to {content.channel_id}")
        # Simulate publishing logic
        return True
    
    scheduler.add_publishing_callback(publishing_handler)
    
    # Start scheduler
    scheduler.start()
    
    # Create test content
    test_content = ScheduledContent(
        id="test_001",
        channel_id="horror_stories",
        title="قصة رعب تجريبية",
        content="هذه قصة رعب تجريبية للاختبار...",
        hashtags=["#رعب", "#قصص"],
        media_files={"image": "/path/to/image.jpg"},
        created_at=datetime.now(),
        status=ContentStatus.DRAFT
    )
    
    # Add to preview queue
    scheduler.add_content_for_preview(test_content)
    
    # Check system status
    status = scheduler.get_system_status()
    print(f"System status: {json.dumps(status, indent=2, ensure_ascii=False)}")
    
    # Keep running for testing
    try:
        while True:
            time.sleep(10)
            print(f"Pending previews: {len(scheduler.get_pending_previews())}")
    except KeyboardInterrupt:
        scheduler.stop()
        print("Scheduler stopped")

