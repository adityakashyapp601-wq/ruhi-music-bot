"""Inline keyboards and buttons"""

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Keyboards:
    @staticmethod
    def main_menu():
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🎵 Music", callback_data="music_menu"),
                InlineKeyboardButton("🎬 Videos", callback_data="video_menu")
            ],
            [
                InlineKeyboardButton("📂 Playlists", callback_data="playlist_menu"),
                InlineKeyboardButton("👑 Admin", callback_data="admin_menu")
            ],
            [
                InlineKeyboardButton("ℹ️ Help", callback_data="help_menu")
            ]
        ])
    
    @staticmethod
    def music_controls():
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⏸ Pause", callback_data="pause"),
                InlineKeyboardButton("▶ Resume", callback_data="resume"),
                InlineKeyboardButton("⏭ Skip", callback_data="skip")
            ],
            [
                InlineKeyboardButton("📜 Queue", callback_data="show_queue"),
                InlineKeyboardButton("🔁 Loop", callback_data="toggle_loop")
            ]
        ])
    
    @staticmethod
    def queue_actions():
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🔄 Refresh", callback_data="show_queue"),
                InlineKeyboardButton("🏠 Back", callback_data="main_menu_back")
            ]
        ])
    
    @staticmethod
    def help_keyboard():
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📖 Full Guide", url="https://github.com/adityakashyapp601-wq/ruhi-music-bot")
            ]
        ])
    
    @staticmethod
    def search_results(count):
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🎵 Play #1", callback_data="play_1"),
                InlineKeyboardButton("🎵 Play #2", callback_data="play_2")
            ]
        ])
