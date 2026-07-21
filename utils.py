"""Utility functions for YouTube search and formatting"""

import re

class YouTubeUtil:
    @staticmethod
    async def search(query, limit=5):
        """Mock YouTube search - returns sample results"""
        # In production, integrate with yt-dlp
        return [{
            'title': query,
            'duration': 240,
            'uploader': 'Unknown Artist',
            'views': '1M',
            'url': f'https://www.youtube.com/results?search_query={query}'
        }]

class Formatter:
    @staticmethod
    def format_duration(seconds):
        """Convert seconds to MM:SS format"""
        if not seconds:
            return '0:00'
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins}:{secs:02d}"
    
    @staticmethod
    def create_queue_text(queue):
        """Create formatted queue text"""
        if not queue:
            return "📜 **Queue is empty!**"
        
        text = "📜 **Current Queue:**\n\n"
        for i, song in enumerate(queue[:10], 1):
            title = song.get('title', 'Unknown')[:50]
            duration = Formatter.format_duration(song.get('duration', 0))
            text += f"{i}. **{title}** ⏱ {duration}\n"
        
        if len(queue) > 10:
            text += f"\n... and {len(queue) - 10} more songs"
        
        return text

youtube = YouTubeUtil()
formatter = Formatter()
