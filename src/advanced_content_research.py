"""
Advanced Content Research System
Comprehensive web research with content transformation to bypass platform restrictions
"""

import json
import os
import requests
import time
import hashlib
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import logging
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ResearchSource:
    """Represents a research source with metadata"""
    url: str
    title: str
    content: str
    source_type: str  # article, video, social_post, forum, etc.
    language: str
    credibility_score: float
    extracted_at: datetime
    keywords: List[str]
    summary: str

@dataclass
class ContentInsight:
    """Represents insights extracted from research"""
    topic: str
    trending_keywords: List[str]
    popular_formats: List[str]
    engagement_patterns: Dict[str, Any]
    content_gaps: List[str]
    competitor_analysis: Dict[str, Any]
    audience_preferences: Dict[str, Any]

class WebScraper:
    """Advanced web scraper with multiple strategies"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Rotating user agents
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]
    
    def scrape_url(self, url: str, timeout: int = 10) -> Optional[Dict[str, Any]]:
        """Scrape content from a URL"""
        try:
            # Rotate user agent
            self.session.headers['User-Agent'] = random.choice(self.user_agents)
            
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            
            # Extract basic information
            content_data = {
                'url': url,
                'status_code': response.status_code,
                'content': response.text,
                'headers': dict(response.headers),
                'scraped_at': datetime.now().isoformat()
            }
            
            return content_data
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return None
    
    def extract_text_content(self, html_content: str) -> str:
        """Extract clean text from HTML content"""
        try:
            # Simple HTML tag removal (in production, use BeautifulSoup)
            text = re.sub(r'<[^>]+>', '', html_content)
            text = re.sub(r'\s+', ' ', text)
            text = text.strip()
            
            return text
            
        except Exception as e:
            logger.error(f"Error extracting text: {e}")
            return ""

class SearchEngineInterface:
    """Interface for multiple search engines"""
    
    def __init__(self):
        self.search_engines = {
            'google': self._search_google,
            'bing': self._search_bing,
            'duckduckgo': self._search_duckduckgo
        }
        
        # API keys (should be loaded from environment)
        self.google_api_key = os.getenv('GOOGLE_SEARCH_API_KEY')
        self.google_cx = os.getenv('GOOGLE_SEARCH_CX')
        self.bing_api_key = os.getenv('BING_SEARCH_API_KEY')
    
    def search_multiple_engines(self, query: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """Search across multiple search engines"""
        all_results = []
        
        for engine_name, search_func in self.search_engines.items():
            try:
                results = search_func(query, num_results)
                for result in results:
                    result['search_engine'] = engine_name
                all_results.extend(results)
            except Exception as e:
                logger.error(f"Error searching {engine_name}: {e}")
        
        # Remove duplicates based on URL
        seen_urls = set()
        unique_results = []
        for result in all_results:
            if result.get('url') not in seen_urls:
                seen_urls.add(result.get('url'))
                unique_results.append(result)
        
        return unique_results[:num_results]
    
    def _search_google(self, query: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """Search using Google Custom Search API"""
        if not self.google_api_key or not self.google_cx:
            return self._simulate_search_results(query, 'google', num_results)
        
        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'key': self.google_api_key,
                'cx': self.google_cx,
                'q': query,
                'num': min(num_results, 10)
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for item in data.get('items', []):
                results.append({
                    'title': item.get('title', ''),
                    'url': item.get('link', ''),
                    'snippet': item.get('snippet', ''),
                    'source': 'google'
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Google search error: {e}")
            return self._simulate_search_results(query, 'google', num_results)
    
    def _search_bing(self, query: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """Search using Bing Search API"""
        if not self.bing_api_key:
            return self._simulate_search_results(query, 'bing', num_results)
        
        try:
            url = "https://api.bing.microsoft.com/v7.0/search"
            headers = {'Ocp-Apim-Subscription-Key': self.bing_api_key}
            params = {
                'q': query,
                'count': min(num_results, 50),
                'mkt': 'ar-SA'
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for item in data.get('webPages', {}).get('value', []):
                results.append({
                    'title': item.get('name', ''),
                    'url': item.get('url', ''),
                    'snippet': item.get('snippet', ''),
                    'source': 'bing'
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Bing search error: {e}")
            return self._simulate_search_results(query, 'bing', num_results)
    
    def _search_duckduckgo(self, query: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """Search using DuckDuckGo (simulated)"""
        return self._simulate_search_results(query, 'duckduckgo', num_results)
    
    def _simulate_search_results(self, query: str, engine: str, num_results: int) -> List[Dict[str, Any]]:
        """Simulate search results for testing"""
        results = []
        for i in range(min(num_results, 5)):
            results.append({
                'title': f"نتيجة بحث {i+1} عن {query}",
                'url': f"https://example.com/result_{i+1}",
                'snippet': f"هذه نتيجة بحث تجريبية رقم {i+1} عن موضوع {query} من محرك البحث {engine}",
                'source': engine
            })
        return results

class ContentTransformer:
    """Transforms and reframes content to avoid copyright issues"""
    
    def __init__(self):
        self.transformation_strategies = [
            self._paraphrase_content,
            self._change_perspective,
            self._add_cultural_context,
            self._create_analogy,
            self._extract_principles
        ]
    
    def transform_content(self, original_content: str, content_type: str, target_audience: str = "arabic") -> str:
        """Transform content using multiple strategies"""
        try:
            # Apply multiple transformation strategies
            transformed = original_content
            
            for strategy in self.transformation_strategies:
                transformed = strategy(transformed, content_type, target_audience)
            
            # Final cleanup
            transformed = self._cleanup_content(transformed)
            
            return transformed
            
        except Exception as e:
            logger.error(f"Error transforming content: {e}")
            return original_content
    
    def _paraphrase_content(self, content: str, content_type: str, target_audience: str) -> str:
        """Paraphrase content to make it original"""
        # Simple paraphrasing logic (in production, use advanced NLP)
        
        # Replace common phrases
        replacements = {
            'في الواقع': 'في الحقيقة',
            'من المهم': 'من الضروري',
            'يجب أن': 'ينبغي أن',
            'بالإضافة إلى ذلك': 'علاوة على ذلك',
            'في النهاية': 'في الختام'
        }
        
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        return content
    
    def _change_perspective(self, content: str, content_type: str, target_audience: str) -> str:
        """Change the perspective or narrative style"""
        if content_type == 'horror_stories':
            # Change from third person to first person or vice versa
            content = re.sub(r'كان هناك', 'رأيت', content)
            content = re.sub(r'حدث', 'شاهدت', content)
        
        elif content_type == 'motivational_quotes':
            # Make it more personal
            content = re.sub(r'الناس', 'أنت', content)
            content = re.sub(r'الشخص', 'أنت', content)
        
        return content
    
    def _add_cultural_context(self, content: str, content_type: str, target_audience: str) -> str:
        """Add cultural context relevant to target audience"""
        if target_audience == "arabic":
            # Add Arabic cultural references
            cultural_additions = [
                "في ثقافتنا العربية",
                "كما يقول المثل العربي",
                "في تراثنا الشعبي",
                "حسب تقاليدنا"
            ]
            
            # Randomly add cultural context
            if len(content) > 100:
                addition = random.choice(cultural_additions)
                sentences = content.split('.')
                if len(sentences) > 1:
                    sentences[1] = f"{addition}، {sentences[1]}"
                    content = '.'.join(sentences)
        
        return content
    
    def _create_analogy(self, content: str, content_type: str, target_audience: str) -> str:
        """Create analogies to explain concepts differently"""
        # Simple analogy creation
        if 'النجاح' in content:
            content = content.replace('النجاح', 'النجاح مثل الشجرة التي تحتاج وقت لتنمو')
        
        if 'الصبر' in content:
            content = content.replace('الصبر', 'الصبر كالمطر الذي يروي الأرض ببطء')
        
        return content
    
    def _extract_principles(self, content: str, content_type: str, target_audience: str) -> str:
        """Extract underlying principles rather than specific details"""
        # Focus on principles rather than specific examples
        if content_type == 'design_tips':
            content = re.sub(r'استخدم اللون الأزرق', 'اختر ألوان هادئة', content)
            content = re.sub(r'ضع الأريكة هنا', 'رتب الأثاث بشكل متوازن', content)
        
        return content
    
    def _cleanup_content(self, content: str) -> str:
        """Final cleanup of transformed content"""
        # Remove extra spaces
        content = re.sub(r'\s+', ' ', content)
        
        # Remove potential copyright indicators
        content = re.sub(r'©.*?(?=\s|$)', '', content)
        content = re.sub(r'المصدر:.*?(?=\n|$)', '', content)
        content = re.sub(r'نقلاً عن.*?(?=\n|$)', '', content)
        
        # Ensure proper sentence structure
        content = content.strip()
        if content and not content.endswith('.'):
            content += '.'
        
        return content

class TrendAnalyzer:
    """Analyzes trends and popular content patterns"""
    
    def __init__(self):
        self.trend_sources = [
            'google_trends',
            'social_media_trends',
            'news_trends',
            'search_trends'
        ]
    
    def analyze_trends(self, topic: str, content_type: str, time_period: str = "7d") -> Dict[str, Any]:
        """Analyze trends for a specific topic"""
        try:
            trend_data = {
                'topic': topic,
                'content_type': content_type,
                'time_period': time_period,
                'trending_keywords': self._get_trending_keywords(topic),
                'popular_formats': self._get_popular_formats(content_type),
                'engagement_patterns': self._analyze_engagement_patterns(topic, content_type),
                'competitor_content': self._analyze_competitor_content(topic),
                'audience_insights': self._get_audience_insights(topic, content_type)
            }
            
            return trend_data
            
        except Exception as e:
            logger.error(f"Error analyzing trends: {e}")
            return {'topic': topic, 'error': str(e)}
    
    def _get_trending_keywords(self, topic: str) -> List[str]:
        """Get trending keywords related to topic"""
        # Simulate trending keywords (in production, use Google Trends API)
        base_keywords = [topic]
        
        if 'رعب' in topic:
            base_keywords.extend(['مخيف', 'غامض', 'مرعب', 'أشباح', 'ليل'])
        elif 'إسلام' in topic:
            base_keywords.extend(['دين', 'إيمان', 'صحابة', 'سيرة', 'تاريخ'])
        elif 'تصميم' in topic:
            base_keywords.extend(['ديكور', 'منزل', 'أثاث', 'ألوان', 'مساحة'])
        elif 'تحفيز' in topic:
            base_keywords.extend(['نجاح', 'إلهام', 'أهداف', 'إنجاز', 'تطوير'])
        elif 'طبخ' in topic:
            base_keywords.extend(['وصفة', 'طعام', 'مطبخ', 'طبخة', 'لذيذ'])
        
        return base_keywords[:10]
    
    def _get_popular_formats(self, content_type: str) -> List[str]:
        """Get popular content formats"""
        format_mapping = {
            'horror_stories': ['قصة قصيرة', 'حكاية مخيفة', 'تجربة شخصية', 'أسطورة'],
            'islamic_stories': ['قصة صحابي', 'درس من السيرة', 'حكمة إسلامية', 'موعظة'],
            'design_tips': ['نصيحة سريعة', 'قبل وبعد', 'جولة منزلية', 'DIY'],
            'motivational_quotes': ['اقتباس ملهم', 'قصة نجاح', 'تحدي يومي', 'هدف'],
            'cooking_recipes': ['وصفة سريعة', 'طبخة تقليدية', 'حلوى', 'وجبة صحية']
        }
        
        return format_mapping.get(content_type, ['محتوى عام'])
    
    def _analyze_engagement_patterns(self, topic: str, content_type: str) -> Dict[str, Any]:
        """Analyze engagement patterns"""
        # Simulate engagement analysis
        return {
            'best_posting_times': ['19:00', '20:00', '21:00'],
            'optimal_length': self._get_optimal_length(content_type),
            'engagement_triggers': ['سؤال في النهاية', 'دعوة للتفاعل', 'هاشتاغ شائع'],
            'visual_preferences': ['صور عالية الجودة', 'ألوان دافئة', 'تصميم بسيط']
        }
    
    def _get_optimal_length(self, content_type: str) -> Dict[str, int]:
        """Get optimal content length"""
        length_mapping = {
            'horror_stories': {'min': 200, 'max': 300, 'optimal': 250},
            'islamic_stories': {'min': 250, 'max': 350, 'optimal': 300},
            'design_tips': {'min': 150, 'max': 250, 'optimal': 200},
            'motivational_quotes': {'min': 100, 'max': 200, 'optimal': 150},
            'cooking_recipes': {'min': 200, 'max': 400, 'optimal': 300}
        }
        
        return length_mapping.get(content_type, {'min': 150, 'max': 300, 'optimal': 200})
    
    def _analyze_competitor_content(self, topic: str) -> Dict[str, Any]:
        """Analyze competitor content"""
        # Simulate competitor analysis
        return {
            'top_performers': [
                {'title': f'محتوى منافس 1 عن {topic}', 'engagement': 1500},
                {'title': f'محتوى منافس 2 عن {topic}', 'engagement': 1200}
            ],
            'content_gaps': [f'نقص في المحتوى عن {topic}', 'فرصة للتميز'],
            'successful_strategies': ['استخدام القصص', 'التفاعل مع الجمهور', 'المحتوى البصري']
        }
    
    def _get_audience_insights(self, topic: str, content_type: str) -> Dict[str, Any]:
        """Get audience insights"""
        # Simulate audience analysis
        return {
            'demographics': {'age_range': '18-35', 'gender': 'mixed', 'location': 'MENA'},
            'interests': [topic, 'ترفيه', 'تعلم', 'ثقافة'],
            'behavior_patterns': {
                'active_hours': ['19:00-23:00'],
                'preferred_platforms': ['TikTok', 'YouTube', 'Instagram'],
                'engagement_style': 'تفاعلي'
            }
        }

class AdvancedContentResearcher:
    """Main advanced content research system"""
    
    def __init__(self):
        self.web_scraper = WebScraper()
        self.search_interface = SearchEngineInterface()
        self.content_transformer = ContentTransformer()
        self.trend_analyzer = TrendAnalyzer()
        
        # Storage for research results
        self.research_cache = {}
        self.cache_duration = timedelta(hours=6)  # Cache results for 6 hours
    
    def comprehensive_research(self, topic: str, content_type: str, depth: str = "deep") -> Dict[str, Any]:
        """Perform comprehensive research on a topic"""
        try:
            # Check cache first
            cache_key = f"{topic}_{content_type}_{depth}"
            if self._is_cached(cache_key):
                logger.info(f"Using cached research for {topic}")
                return self.research_cache[cache_key]['data']
            
            logger.info(f"Starting comprehensive research for: {topic} ({content_type})")
            
            research_results = {
                'topic': topic,
                'content_type': content_type,
                'research_depth': depth,
                'timestamp': datetime.now().isoformat(),
                'sources': [],
                'insights': {},
                'transformed_content': [],
                'recommendations': {}
            }
            
            # Step 1: Multi-engine search
            search_results = self.search_interface.search_multiple_engines(
                topic, num_results=20 if depth == "deep" else 10
            )
            
            # Step 2: Scrape and analyze sources
            research_results['sources'] = self._process_search_results(search_results)
            
            # Step 3: Trend analysis
            research_results['insights'] = self.trend_analyzer.analyze_trends(topic, content_type)
            
            # Step 4: Content transformation
            research_results['transformed_content'] = self._generate_transformed_content(
                research_results['sources'], content_type
            )
            
            # Step 5: Generate recommendations
            research_results['recommendations'] = self._generate_recommendations(research_results)
            
            # Cache results
            self._cache_results(cache_key, research_results)
            
            logger.info(f"Completed comprehensive research for: {topic}")
            return research_results
            
        except Exception as e:
            logger.error(f"Error in comprehensive research: {e}")
            return {'topic': topic, 'error': str(e)}
    
    def _process_search_results(self, search_results: List[Dict[str, Any]]) -> List[ResearchSource]:
        """Process search results and extract content"""
        sources = []
        
        # Use threading for parallel processing
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_result = {
                executor.submit(self._process_single_result, result): result 
                for result in search_results[:10]  # Limit to avoid overwhelming
            }
            
            for future in as_completed(future_to_result):
                try:
                    source = future.result()
                    if source:
                        sources.append(source)
                except Exception as e:
                    logger.error(f"Error processing search result: {e}")
        
        return sources
    
    def _process_single_result(self, result: Dict[str, Any]) -> Optional[ResearchSource]:
        """Process a single search result"""
        try:
            # Scrape the URL
            scraped_data = self.web_scraper.scrape_url(result['url'])
            if not scraped_data:
                return None
            
            # Extract text content
            text_content = self.web_scraper.extract_text_content(scraped_data['content'])
            
            # Create research source
            source = ResearchSource(
                url=result['url'],
                title=result['title'],
                content=text_content[:1000],  # Limit content length
                source_type='article',  # Default type
                language='arabic',  # Assume Arabic
                credibility_score=0.8,  # Default score
                extracted_at=datetime.now(),
                keywords=self._extract_keywords(text_content),
                summary=result['snippet']
            )
            
            return source
            
        except Exception as e:
            logger.error(f"Error processing single result: {e}")
            return None
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        # Simple keyword extraction (in production, use advanced NLP)
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filter common Arabic stop words
        stop_words = {'في', 'من', 'إلى', 'على', 'هذا', 'هذه', 'التي', 'الذي', 'أن', 'كان', 'كانت'}
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Return most frequent keywords
        from collections import Counter
        keyword_counts = Counter(keywords)
        return [word for word, count in keyword_counts.most_common(10)]
    
    def _generate_transformed_content(self, sources: List[ResearchSource], content_type: str) -> List[str]:
        """Generate transformed content from sources"""
        transformed_content = []
        
        for source in sources[:5]:  # Use top 5 sources
            try:
                transformed = self.content_transformer.transform_content(
                    source.content, content_type, "arabic"
                )
                transformed_content.append(transformed)
            except Exception as e:
                logger.error(f"Error transforming content: {e}")
        
        return transformed_content
    
    def _generate_recommendations(self, research_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate content recommendations based on research"""
        recommendations = {
            'content_angles': [],
            'trending_topics': [],
            'optimal_timing': {},
            'engagement_strategies': [],
            'content_format': {},
            'hashtag_suggestions': []
        }
        
        try:
            insights = research_results.get('insights', {})
            
            # Content angles based on sources
            recommendations['content_angles'] = [
                f"زاوية جديدة حول {research_results['topic']}",
                f"منظور مختلف عن {research_results['topic']}",
                f"تجربة شخصية مع {research_results['topic']}"
            ]
            
            # Trending topics
            recommendations['trending_topics'] = insights.get('trending_keywords', [])[:5]
            
            # Optimal timing
            engagement_patterns = insights.get('engagement_patterns', {})
            recommendations['optimal_timing'] = {
                'best_times': engagement_patterns.get('best_posting_times', ['20:00']),
                'optimal_length': engagement_patterns.get('optimal_length', {})
            }
            
            # Engagement strategies
            recommendations['engagement_strategies'] = [
                'استخدم سؤال في نهاية المحتوى',
                'أضف دعوة واضحة للتفاعل',
                'استخدم هاشتاغات شائعة',
                'أضف قصة شخصية'
            ]
            
            # Content format
            recommendations['content_format'] = {
                'structure': 'مقدمة جذابة + محتوى رئيسي + خاتمة تفاعلية',
                'visual_elements': 'صور عالية الجودة + ألوان متناسقة',
                'tone': 'ودود ومحفز'
            }
            
            # Hashtag suggestions
            recommendations['hashtag_suggestions'] = [
                f"#{research_results['topic']}",
                "#محتوى_عربي",
                "#تفاعل",
                "#إلهام"
            ]
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
        
        return recommendations
    
    def _is_cached(self, cache_key: str) -> bool:
        """Check if research results are cached and still valid"""
        if cache_key not in self.research_cache:
            return False
        
        cached_time = datetime.fromisoformat(self.research_cache[cache_key]['timestamp'])
        return datetime.now() - cached_time < self.cache_duration
    
    def _cache_results(self, cache_key: str, results: Dict[str, Any]):
        """Cache research results"""
        self.research_cache[cache_key] = {
            'timestamp': datetime.now().isoformat(),
            'data': results
        }
    
    def get_content_suggestions(self, channel_id: str, num_suggestions: int = 5) -> List[Dict[str, Any]]:
        """Get content suggestions for a specific channel"""
        try:
            # Channel-specific topics
            channel_topics = {
                'horror_stories': ['البيت المهجور', 'الصوت الغامض', 'الظل المتحرك', 'الرسالة المجهولة', 'الحلم المرعب'],
                'islamic_stories': ['قصة صحابي', 'درس من السيرة', 'حكمة إسلامية', 'معجزة نبوية', 'موقف تاريخي'],
                'home_design': ['تصميم غرفة صغيرة', 'ديكور بميزانية محدودة', 'ألوان عصرية', 'إضاءة منزلية', 'تنظيم المساحات'],
                'motivation': ['تحقيق الأهداف', 'التغلب على الصعوبات', 'قوة الإرادة', 'النجاح المهني', 'الثقة بالنفس'],
                'ai_chef': ['وصفة سريعة', 'طبخة تقليدية', 'حلوى منزلية', 'وجبة صحية', 'مقبلات لذيذة']
            }
            
            topics = channel_topics.get(channel_id, ['موضوع عام'])
            suggestions = []
            
            for i, topic in enumerate(topics[:num_suggestions]):
                suggestion = {
                    'id': f"{channel_id}_suggestion_{i+1}",
                    'topic': topic,
                    'priority': 'high' if i < 2 else 'medium',
                    'estimated_engagement': random.randint(500, 2000),
                    'content_type': self._get_content_type_for_channel(channel_id),
                    'research_needed': True
                }
                suggestions.append(suggestion)
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Error getting content suggestions: {e}")
            return []
    
    def _get_content_type_for_channel(self, channel_id: str) -> str:
        """Get content type for channel"""
        mapping = {
            'horror_stories': 'horror_stories',
            'islamic_stories': 'islamic_stories',
            'home_design': 'design_tips',
            'motivation': 'motivational_quotes',
            'ai_chef': 'cooking_recipes'
        }
        return mapping.get(channel_id, 'general')

# Example usage and testing
if __name__ == "__main__":
    # Initialize the advanced content researcher
    researcher = AdvancedContentResearcher()
    
    # Test comprehensive research
    test_topics = [
        ('قصص الرعب', 'horror_stories'),
        ('القصص الإسلامية', 'islamic_stories'),
        ('تصميم المنازل', 'design_tips'),
        ('التحفيز', 'motivational_quotes'),
        ('وصفات الطبخ', 'cooking_recipes')
    ]
    
    for topic, content_type in test_topics:
        print(f"\n=== Research for: {topic} ===")
        
        try:
            results = researcher.comprehensive_research(topic, content_type, "deep")
            
            print(f"Sources found: {len(results.get('sources', []))}")
            print(f"Transformed content pieces: {len(results.get('transformed_content', []))}")
            print(f"Recommendations: {len(results.get('recommendations', {}))}")
            
            # Show sample recommendations
            recommendations = results.get('recommendations', {})
            if recommendations:
                print(f"Content angles: {recommendations.get('content_angles', [])[:2]}")
                print(f"Trending topics: {recommendations.get('trending_topics', [])[:3]}")
        
        except Exception as e:
            print(f"Error researching {topic}: {e}")
    
    # Test content suggestions
    print(f"\n=== Content Suggestions ===")
    for channel_id in ['horror_stories', 'islamic_stories', 'home_design', 'motivation', 'ai_chef']:
        suggestions = researcher.get_content_suggestions(channel_id, 3)
        print(f"{channel_id}: {len(suggestions)} suggestions")
        for suggestion in suggestions:
            print(f"  - {suggestion['topic']} (Priority: {suggestion['priority']})")

