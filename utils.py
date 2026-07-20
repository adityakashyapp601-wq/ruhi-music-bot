"""
Utility functions for music bot
"""

import yt_dlp
import os
from typing import Optional, Dict, List

class YouTubeSearch:
    def __init__(self):
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'default_search': 'ytsearch',
        }
    
    async def search(self, query: str, limit: int = 5) -> List[Dict]:
        """Search YouTube for songs"""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch{limit}:{query}", download=False)
                results = []
                for video in info.get('entries', []):
                    results.append({
                        'title': video.get('title', 'Unknown'),
                        'url': video.get('webpage_url', ''),
                        'duration': video.get('duration', 0),
                        'thumbnail': video.get('thumbnail', ''),
                        'uploader': video.get('uploader', 'Unknown'),
                        'views': video.get('view_count', 0),
                    })
                return results
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    async def get_info(self, url: str) -> Optional[Dict]:
        """Get info from YouTube URL"""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'Unknown'),
                    'url': url,
                    'duration': info.get('duration', 0),
                    'thumbnail': info.get('thumbnail', ''),
                    'uploader': info.get('uploader', 'Unknown'),
                    'views': info.get('view_count', 0),
                    'audio_url': info.get('url', ''),
                }
        except Exception as e:
            print(f"Get info error: {e}")
            return None

class MessageFormatting:
    @staticmethod
    def format_duration(seconds: int) -> str:
        """Format duration to MM:SS"""
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins}:{secs:02d}"
    
    @staticmethod
    def create_queue_text(queue: List, current_page: int = 0) -> str:
        """Create formatted queue text"""
        if not queue:
            return "📭 Queue is empty"
        
        text = "🎵 **Current Queue:**\n\n"
        for i, song in enumerate(queue[:10], 1):
            duration = MessageFormatting.format_duration(song.get('duration', 0))
            text += f"{i}. **{song.get('title', 'Unknown')}**\n"
            text += f"   ⏱ {duration} | 👤 {song.get('uploader', 'Unknown')}\n\n"
        
        if len(queue) > 10:
            text += f"\n... and {len(queue) - 10} more songs"
        
        return text

# Global utility instances
youtube = YouTubeSearch()
formatter = MessageFormatting()
