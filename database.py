"""Database management for queues and playlists"""

class Database:
    def __init__(self):
        self.queues = {}
        self.playlists = {}
        self.now_playing = {}
        self.loop_status = {}
    
    def add_to_queue(self, chat_id, song):
        if chat_id not in self.queues:
            self.queues[chat_id] = []
        self.queues[chat_id].append(song)
    
    def get_queue(self, chat_id):
        return self.queues.get(chat_id, [])
    
    def remove_from_queue(self, chat_id, index):
        if chat_id in self.queues and index < len(self.queues[chat_id]):
            return self.queues[chat_id].pop(index)
    
    def clear_queue(self, chat_id):
        if chat_id in self.queues:
            self.queues[chat_id] = []
    
    def set_now_playing(self, chat_id, song):
        self.now_playing[chat_id] = song
    
    def get_now_playing(self, chat_id):
        return self.now_playing.get(chat_id)
    
    def toggle_loop(self, chat_id):
        current = self.loop_status.get(chat_id, False)
        self.loop_status[chat_id] = not current
        return self.loop_status[chat_id]
    
    def create_playlist(self, chat_id, name):
        if chat_id not in self.playlists:
            self.playlists[chat_id] = {}
        self.playlists[chat_id][name] = []
    
    def add_to_playlist(self, chat_id, playlist_name, song):
        if chat_id in self.playlists and playlist_name in self.playlists[chat_id]:
            self.playlists[chat_id][playlist_name].append(song)

db = Database()
