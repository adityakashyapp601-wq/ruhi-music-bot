"""
Database management for music queues and settings
"""

from typing import Dict, List, Optional
import json
import os

class MusicDB:
    def __init__(self):
        self.queues: Dict[int, List] = {}
        self.playlists: Dict[int, List] = {}
        self.settings: Dict[int, Dict] = {}
        self.now_playing: Dict[int, Optional[Dict]] = {}
        self.is_looping: Dict[int, bool] = {}
        self.load_data()
    
    def load_data(self):
        """Load data from JSON files"""
        if os.path.exists("queues.json"):
            with open("queues.json", "r") as f:
                self.queues = json.load(f)
        if os.path.exists("playlists.json"):
            with open("playlists.json", "r") as f:
                self.playlists = json.load(f)
    
    def save_data(self):
        """Save data to JSON files"""
        with open("queues.json", "w") as f:
            json.dump(self.queues, f)
        with open("playlists.json", "w") as f:
            json.dump(self.playlists, f)
    
    # Queue Management
    def add_to_queue(self, chat_id: int, song: Dict):
        """Add song to queue"""
        if chat_id not in self.queues:
            self.queues[chat_id] = []
        self.queues[chat_id].append(song)
        self.save_data()
    
    def get_queue(self, chat_id: int) -> List:
        """Get queue for chat"""
        return self.queues.get(chat_id, [])
    
    def clear_queue(self, chat_id: int):
        """Clear queue for chat"""
        if chat_id in self.queues:
            self.queues[chat_id] = []
        self.save_data()
    
    def remove_from_queue(self, chat_id: int, index: int) -> bool:
        """Remove song from queue"""
        if chat_id in self.queues and 0 <= index < len(self.queues[chat_id]):
            self.queues[chat_id].pop(index)
            self.save_data()
            return True
        return False
    
    # Now Playing
    def set_now_playing(self, chat_id: int, song: Dict):
        """Set current playing song"""
        self.now_playing[chat_id] = song
    
    def get_now_playing(self, chat_id: int) -> Optional[Dict]:
        """Get current playing song"""
        return self.now_playing.get(chat_id)
    
    # Loop Toggle
    def toggle_loop(self, chat_id: int) -> bool:
        """Toggle loop mode"""
        self.is_looping[chat_id] = not self.is_looping.get(chat_id, False)
        return self.is_looping[chat_id]
    
    def is_loop_enabled(self, chat_id: int) -> bool:
        """Check if loop is enabled"""
        return self.is_looping.get(chat_id, False)
    
    # Playlists
    def create_playlist(self, chat_id: int, name: str, songs: List = None):
        """Create new playlist"""
        if chat_id not in self.playlists:
            self.playlists[chat_id] = {}
        self.playlists[chat_id][name] = songs or []
        self.save_data()
    
    def add_to_playlist(self, chat_id: int, playlist_name: str, song: Dict):
        """Add song to playlist"""
        if chat_id in self.playlists and playlist_name in self.playlists[chat_id]:
            self.playlists[chat_id][playlist_name].append(song)
            self.save_data()
    
    def get_playlist(self, chat_id: int, playlist_name: str) -> List:
        """Get playlist songs"""
        if chat_id in self.playlists:
            return self.playlists[chat_id].get(playlist_name, [])
        return []

# Global database instance
db = MusicDB()
