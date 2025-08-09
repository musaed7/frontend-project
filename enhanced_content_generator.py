"""
Enhanced Content Generator with Web Research and Content Preview
Supports 5 specialized channels with automated content creation and preview system
"""

import json
import os
import requests
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging
from dataclasses import dataclass
import hashlib
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ContentPackage:
    """Represents a complete content package for a channel"""
    id: str
    channel_id: str
    title: str
    content: str
    hashtags: List[str]
    media_files: Dict[str, str]  # type -> file_path
    created_at: datetime
    status: str  # draft, preview, approved, published
    scheduled_time: Optional[datetime] = None
    research_sources: List[str] = None

class WebResearcher:
    """Handles web research for content inspiration while avoiding copyright issues"""
    
    def __init__(self):
        self.search_engines = {
            'google': 'https://www.googleapis.com/customsearch/v1',
            'bing': 'https://api.bing.microsoft.com/v7.0/search'
        }
        
    def research_topic(self, topic: str, content_type: str, language: str = 'ar') -> Dict[str, Any]:
        """Research a topic across multiple sources"""
        try:
            research_results = {
                'topic': topic,
                'content_type': content_type,
                'sources': [],
                'trends': [],
                'keywords': [],
                'inspiration': []
            }
            
            # Simulate web research (in real implementation, use actual APIs)
            search_queries = self._generate_search_queries(topic, content_type, language)
            
            for query in search_queries:
                # Simulate search results
                results = self._simulate_search(query, language)
                research_results['sources'].extend(results.get('sources', []))
                research_results['trends'].extend(results.get('trends', []))
                research_results['keywords'].extend(results.get('keywords', []))
                research_results['inspiration'].extend(results.get('inspiration', []))
            
            # Remove duplicates and limit results
            research_results['sources'] = list(set(research_results['sources']))[:10]
            research_results['trends'] = list(set(research_results['trends']))[:5]
            research_results['keywords'] = list(set(research_results['keywords']))[:15]
            research_results['inspiration'] = list(set(research_results['inspiration']))[:8]
            
            return research_results
            
        except Exception as e:
            logger.error(f"Error in web research: {e}")
            return {'topic': topic, 'sources': [], 'trends': [], 'keywords': [], 'inspiration': []}
    
    def _generate_search_queries(self, topic: str, content_type: str, language: str) -> List[str]:
        """Generate search queries based on topic and content type"""
        base_queries = [topic]
        
        if content_type == 'horror_stories':
            base_queries.extend([
                f"{topic} قصة رعب",
                f"حكايات مخيفة {topic}",
                f"قصص غامضة {topic}"
            ])
        elif content_type == 'islamic_stories':
            base_queries.extend([
                f"{topic} قصة إسلامية",
                f"سيرة {topic}",
                f"تاريخ إسلامي {topic}"
            ])
        elif content_type == 'design_tips':
            base_queries.extend([
                f"{topic} تصميم منزل",
                f"ديكور {topic}",
                f"أفكار تصميم {topic}"
            ])
        elif content_type == 'motivational_quotes':
            base_queries.extend([
                f"{topic} اقتباس تحفيزي",
                f"حكمة {topic}",
                f"إلهام {topic}"
            ])
        elif content_type == 'cooking_recipes':
            base_queries.extend([
                f"{topic} وصفة طبخ",
                f"طريقة عمل {topic}",
                f"مطبخ {topic}"
            ])
        
        return base_queries[:5]  # Limit to 5 queries
    
    def _simulate_search(self, query: str, language: str) -> Dict[str, List[str]]:
        """Simulate search results (replace with actual API calls in production)"""
        # This is a simulation - in real implementation, use actual search APIs
        return {
            'sources': [f"مصدر بحث عن {query}", f"مرجع {query}"],
            'trends': [f"ترند {query}"],
            'keywords': [f"كلمة مفتاحية {query}", f"هاشتاغ {query}"],
            'inspiration': [f"إلهام من {query}"]
        }

class AIContentGenerator:
    """Enhanced AI content generator with multiple provider support"""
    
    def __init__(self):
        self.providers = {
            'openai': self._generate_with_openai,
            'gemini': self._generate_with_gemini,
            'deepseek': self._generate_with_deepseek
        }
        self.current_provider = 'gemini'  # Default to Gemini
        
    def generate_content(self, prompt: str, content_type: str, research_data: Dict = None) -> str:
        """Generate content using AI with research enhancement"""
        try:
            # Enhance prompt with research data
            enhanced_prompt = self._enhance_prompt_with_research(prompt, research_data)
            
            # Try primary provider first
            if self.current_provider in self.providers:
                content = self.providers[self.current_provider](enhanced_prompt)
                if content:
                    return self._post_process_content(content, content_type)
            
            # Try fallback providers
            for provider in ['deepseek', 'openai']:
                if provider != self.current_provider and provider in self.providers:
                    content = self.providers[provider](enhanced_prompt)
                    if content:
                        return self._post_process_content(content, content_type)
            
            # If all providers fail, return a template-based content
            return self._generate_template_content(content_type, research_data)
            
        except Exception as e:
            logger.error(f"Error generating content: {e}")
            return self._generate_template_content(content_type, research_data)
    
    def _enhance_prompt_with_research(self, prompt: str, research_data: Dict) -> str:
        """Enhance the AI prompt with research data"""
        if not research_data:
            return prompt
        
        enhancement = f"""
        
        معلومات إضافية للإلهام (لا تنسخ مباشرة، استخدم للإلهام فقط):
        - الكلمات المفتاحية الشائعة: {', '.join(research_data.get('keywords', [])[:5])}
        - الاتجاهات الحالية: {', '.join(research_data.get('trends', [])[:3])}
        - أفكار للإلهام: {', '.join(research_data.get('inspiration', [])[:3])}
        
        تأكد من إنشاء محتوى أصلي ومبتكر مستوحى من هذه المعلومات دون نسخ مباشر.
        """
        
        return prompt + enhancement
    
    def _generate_with_openai(self, prompt: str) -> Optional[str]:
        """Generate content using OpenAI API"""
        try:
            import openai
            
            client = openai.OpenAI(
                api_key=os.getenv('OPENAI_API_KEY'),
                base_url=os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')
            )
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "أنت منشئ محتوى محترف متخصص في إنشاء محتوى عربي أصلي وجذاب لوسائل التواصل الاجتماعي."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.8
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"OpenAI generation failed: {e}")
            return None
    
    def _generate_with_gemini(self, prompt: str) -> Optional[str]:
        """Generate content using Gemini API"""
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
            model = genai.GenerativeModel('gemini-pro')
            
            response = model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Gemini generation failed: {e}")
            return None
    
    def _generate_with_deepseek(self, prompt: str) -> Optional[str]:
        """Generate content using DeepSeek API"""
        try:
            # DeepSeek API implementation (similar to OpenAI)
            headers = {
                'Authorization': f'Bearer {os.getenv("DEEPSEEK_API_KEY")}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'deepseek-chat',
                'messages': [
                    {'role': 'system', 'content': 'أنت منشئ محتوى محترف متخصص في إنشاء محتوى عربي أصلي وجذاب لوسائل التواصل الاجتماعي.'},
                    {'role': 'user', 'content': prompt}
                ],
                'max_tokens': 500,
                'temperature': 0.8
            }
            
            response = requests.post('https://api.deepseek.com/v1/chat/completions', 
                                   headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            
        except Exception as e:
            logger.error(f"DeepSeek generation failed: {e}")
            return None
    
    def _post_process_content(self, content: str, content_type: str) -> str:
        """Post-process generated content to ensure quality and compliance"""
        # Remove any potential copyright issues
        content = self._remove_copyright_content(content)
        
        # Ensure appropriate length for platform
        content = self._adjust_content_length(content, content_type)
        
        # Clean up formatting
        content = self._clean_formatting(content)
        
        return content
    
    def _remove_copyright_content(self, content: str) -> str:
        """Remove potential copyright-infringing content"""
        # Remove direct quotes from copyrighted material
        content = re.sub(r'"[^"]*"', '', content)  # Remove quoted text
        content = re.sub(r'©.*?(?=\s|$)', '', content)  # Remove copyright symbols
        content = re.sub(r'المصدر:.*?(?=\n|$)', '', content)  # Remove source attributions
        
        return content.strip()
    
    def _adjust_content_length(self, content: str, content_type: str) -> str:
        """Adjust content length based on platform requirements"""
        max_lengths = {
            'horror_stories': 300,
            'islamic_stories': 350,
            'design_tips': 280,
            'motivational_quotes': 200,
            'cooking_recipes': 400
        }
        
        max_length = max_lengths.get(content_type, 300)
        
        if len(content) > max_length:
            # Truncate at the last complete sentence
            sentences = content.split('.')
            truncated = ''
            for sentence in sentences:
                if len(truncated + sentence + '.') <= max_length:
                    truncated += sentence + '.'
                else:
                    break
            content = truncated.strip()
        
        return content
    
    def _clean_formatting(self, content: str) -> str:
        """Clean up content formatting"""
        # Remove extra whitespace
        content = re.sub(r'\s+', ' ', content)
        
        # Remove markdown formatting that might not display well
        content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)  # Remove bold
        content = re.sub(r'\*(.*?)\*', r'\1', content)      # Remove italic
        
        return content.strip()
    
    def _generate_template_content(self, content_type: str, research_data: Dict = None) -> str:
        """Generate template-based content as fallback"""
        templates = {
            'horror_stories': "في ليلة مظلمة وباردة، حدث شيء غريب لم يكن أحد يتوقعه. كانت الأصوات تأتي من العلية، أصوات خطوات بطيئة ومخيفة. عندما صعد أحمد للتحقق، وجد شيئاً لم يكن يتوقعه أبداً...",
            'islamic_stories': "في عهد الرسول صلى الله عليه وسلم، كان هناك صحابي جليل يُضرب به المثل في الكرم والعطاء. قصته تعلمنا أن العطاء الحقيقي يأتي من القلب، وأن البركة في العطاء وليس في الأخذ.",
            'design_tips': "إذا كنت تريد تجديد منزلك بميزانية محدودة، إليك نصيحة ذهبية: ابدأ بتغيير الإضاءة. الإضاءة الجيدة يمكنها تحويل أي مساحة من عادية إلى استثنائية.",
            'motivational_quotes': "النجاح ليس نهاية الطريق، والفشل ليس نهاية العالم. الشجاعة للاستمرار هي ما يهم حقاً. كل يوم جديد هو فرصة جديدة لتحقيق أحلامك.",
            'cooking_recipes': "وصفة اليوم: معكرونة بالصلصة الحمراء. المقادير بسيطة والطعم رائع. ستحتاج إلى معكرونة، طماطم، ثوم، وبصل. الطريقة سهلة ولذيذة."
        }
        
        return templates.get(content_type, "محتوى تجريبي للاختبار.")

class MediaGenerator:
    """Generates images and videos for content"""
    
    def __init__(self):
        self.image_generators = ['stable_diffusion', 'dall_e', 'midjourney']
        self.video_generators = ['runway_ml', 'pika_labs']
        
    def generate_image(self, prompt: str, content_type: str, output_path: str) -> bool:
        """Generate image for content"""
        try:
            # Simulate image generation (replace with actual API calls)
            logger.info(f"Generating image for: {prompt}")
            
            # Create a placeholder image file
            with open(output_path, 'w') as f:
                f.write(f"Image placeholder for: {prompt}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return False
    
    def generate_video(self, prompt: str, content_type: str, output_path: str) -> bool:
        """Generate video for content"""
        try:
            # Simulate video generation (replace with actual API calls)
            logger.info(f"Generating video for: {prompt}")
            
            # Create a placeholder video file
            with open(output_path, 'w') as f:
                f.write(f"Video placeholder for: {prompt}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error generating video: {e}")
            return False

class ContentPreviewSystem:
    """Manages content preview and approval workflow"""
    
    def __init__(self, preview_window_start: str = "21:00", preview_window_end: str = "22:00"):
        self.preview_start = preview_window_start
        self.preview_end = preview_window_end
        self.pending_content = []
        
    def is_preview_time(self) -> bool:
        """Check if current time is within preview window"""
        now = datetime.now().time()
        start_time = datetime.strptime(self.preview_start, "%H:%M").time()
        end_time = datetime.strptime(self.preview_end, "%H:%M").time()
        
        return start_time <= now <= end_time
    
    def add_content_for_preview(self, content_package: ContentPackage):
        """Add content to preview queue"""
        content_package.status = 'preview'
        self.pending_content.append(content_package)
        logger.info(f"Content {content_package.id} added to preview queue")
    
    def get_pending_content(self) -> List[ContentPackage]:
        """Get all content pending preview"""
        return [c for c in self.pending_content if c.status == 'preview']
    
    def approve_content(self, content_id: str) -> bool:
        """Approve content for publishing"""
        for content in self.pending_content:
            if content.id == content_id:
                content.status = 'approved'
                logger.info(f"Content {content_id} approved for publishing")
                return True
        return False
    
    def reject_content(self, content_id: str, reason: str = "") -> bool:
        """Reject content"""
        for content in self.pending_content:
            if content.id == content_id:
                content.status = 'rejected'
                logger.info(f"Content {content_id} rejected: {reason}")
                return True
        return False
    
    def auto_approve_expired_content(self):
        """Auto-approve content that wasn't reviewed during preview window"""
        if not self.is_preview_time():
            for content in self.pending_content:
                if content.status == 'preview':
                    content.status = 'approved'
                    logger.info(f"Content {content.id} auto-approved after preview window")

class EnhancedContentGenerator:
    """Main enhanced content generator class"""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or '/home/ubuntu/ai_content_automation_enhanced/src/data/channels_config.json'
        self.config = self._load_config()
        
        self.web_researcher = WebResearcher()
        self.ai_generator = AIContentGenerator()
        self.media_generator = MediaGenerator()
        self.preview_system = ContentPreviewSystem(
            self.config['global_settings']['preview_window']['start_time'],
            self.config['global_settings']['preview_window']['end_time']
        )
        
        # Create necessary directories
        self.base_dir = os.path.dirname(self.config_path)
        self.content_dir = os.path.join(self.base_dir, 'generated_content')
        self.media_dir = os.path.join(self.base_dir, 'media')
        
        os.makedirs(self.content_dir, exist_ok=True)
        os.makedirs(self.media_dir, exist_ok=True)
        os.makedirs(os.path.join(self.media_dir, 'images'), exist_ok=True)
        os.makedirs(os.path.join(self.media_dir, 'videos'), exist_ok=True)
    
    def _load_config(self) -> Dict:
        """Load channels configuration"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return {'channels': [], 'global_settings': {}}
    
    def generate_content_for_channel(self, channel_id: str, topic: str = None) -> ContentPackage:
        """Generate complete content package for a specific channel"""
        try:
            # Find channel config
            channel_config = None
            for channel in self.config['channels']:
                if channel['id'] == channel_id:
                    channel_config = channel
                    break
            
            if not channel_config:
                raise ValueError(f"Channel {channel_id} not found")
            
            # Generate topic if not provided
            if not topic:
                topic = self._generate_topic_for_channel(channel_config)
            
            # Research the topic
            content_type = channel_config['content_types'][0]  # Use first content type
            research_data = self.web_researcher.research_topic(topic, content_type, channel_config['language'])
            
            # Generate content using AI
            ai_prompt = channel_config['ai_prompts'][content_type]
            content = self.ai_generator.generate_content(ai_prompt, content_type, research_data)
            
            # Generate media
            media_files = {}
            content_id = self._generate_content_id(channel_id, topic)
            
            # Generate image
            image_prompt = channel_config['media_prompts']['image']
            image_path = os.path.join(self.media_dir, 'images', f"{content_id}.jpg")
            if self.media_generator.generate_image(image_prompt, content_type, image_path):
                media_files['image'] = image_path
            
            # Generate video if applicable
            if 'video' in channel_config['media_prompts']:
                video_prompt = channel_config['media_prompts']['video']
                video_path = os.path.join(self.media_dir, 'videos', f"{content_id}.mp4")
                if self.media_generator.generate_video(video_prompt, content_type, video_path):
                    media_files['video'] = video_path
            
            # Create content package
            content_package = ContentPackage(
                id=content_id,
                channel_id=channel_id,
                title=topic,
                content=content,
                hashtags=channel_config['hashtags'],
                media_files=media_files,
                created_at=datetime.now(),
                status='draft',
                research_sources=research_data.get('sources', [])
            )
            
            # Add to preview system
            self.preview_system.add_content_for_preview(content_package)
            
            # Save content package
            self._save_content_package(content_package)
            
            logger.info(f"Generated content package {content_id} for channel {channel_id}")
            return content_package
            
        except Exception as e:
            logger.error(f"Error generating content for channel {channel_id}: {e}")
            raise
    
    def _generate_topic_for_channel(self, channel_config: Dict) -> str:
        """Generate a topic based on channel type"""
        topics = {
            'horror_stories': ['البيت المهجور', 'الصوت في الليل', 'الظل الغامض', 'الرسالة المجهولة'],
            'islamic_stories': ['الصحابي الكريم', 'قصة من السيرة', 'درس من التاريخ', 'حكمة إسلامية'],
            'home_design': ['تصميم غرفة المعيشة', 'ديكور المطبخ', 'تنسيق الألوان', 'الإضاءة المنزلية'],
            'motivation': ['النجاح والإصرار', 'تحقيق الأهداف', 'التفكير الإيجابي', 'قوة الإرادة'],
            'ai_chef': ['معكرونة بالصلصة', 'سلطة صحية', 'حلوى سريعة', 'وجبة إفطار مغذية']
        }
        
        channel_topics = topics.get(channel_config['id'], ['موضوع عام'])
        import random
        return random.choice(channel_topics)
    
    def _generate_content_id(self, channel_id: str, topic: str) -> str:
        """Generate unique content ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        topic_hash = hashlib.md5(topic.encode()).hexdigest()[:8]
        return f"{channel_id}_{timestamp}_{topic_hash}"
    
    def _save_content_package(self, content_package: ContentPackage):
        """Save content package to file"""
        try:
            package_data = {
                'id': content_package.id,
                'channel_id': content_package.channel_id,
                'title': content_package.title,
                'content': content_package.content,
                'hashtags': content_package.hashtags,
                'media_files': content_package.media_files,
                'created_at': content_package.created_at.isoformat(),
                'status': content_package.status,
                'research_sources': content_package.research_sources
            }
            
            package_file = os.path.join(self.content_dir, f"{content_package.id}.json")
            with open(package_file, 'w', encoding='utf-8') as f:
                json.dump(package_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving content package: {e}")
    
    def get_all_channels(self) -> List[Dict]:
        """Get all configured channels"""
        return self.config['channels']
    
    def get_pending_previews(self) -> List[ContentPackage]:
        """Get all content pending preview"""
        return self.preview_system.get_pending_content()
    
    def approve_content(self, content_id: str) -> bool:
        """Approve content for publishing"""
        return self.preview_system.approve_content(content_id)
    
    def reject_content(self, content_id: str, reason: str = "") -> bool:
        """Reject content"""
        return self.preview_system.reject_content(content_id, reason)
    
    def process_auto_approvals(self):
        """Process automatic approvals for expired preview content"""
        self.preview_system.auto_approve_expired_content()
    
    def get_approved_content(self) -> List[ContentPackage]:
        """Get all approved content ready for publishing"""
        return [c for c in self.preview_system.pending_content if c.status == 'approved']

# Example usage and testing
if __name__ == "__main__":
    # Initialize the enhanced content generator
    generator = EnhancedContentGenerator()
    
    # Test content generation for each channel
    channels = generator.get_all_channels()
    
    for channel in channels:
        try:
            print(f"\nGenerating content for channel: {channel['name']}")
            content_package = generator.generate_content_for_channel(channel['id'])
            print(f"Generated content: {content_package.title}")
            print(f"Content preview: {content_package.content[:100]}...")
            print(f"Status: {content_package.status}")
            
        except Exception as e:
            print(f"Error generating content for {channel['name']}: {e}")
    
    # Test preview system
    print(f"\nPending previews: {len(generator.get_pending_previews())}")
    
    # Test auto-approval
    generator.process_auto_approvals()
    print(f"Approved content: {len(generator.get_approved_content())}")

