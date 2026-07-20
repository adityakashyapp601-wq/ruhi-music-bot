"""
Inline keyboards for Ruhi Music Bot
"""

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Keyboards:
    
    @staticmethod
    def main_menu() -> InlineKeyboardMarkup:
        """Main menu keyboard"""
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🎵 Play", callback_data="play_menu"),
                InlineKeyboardButton("🔍 Search", callback_data="search_menu"),
            ],
            [
                InlineKeyboardButton("📜 Queue", callback_data="show_queue"),
                InlineKeyboardButton("📂 Playlists", callback_data="playlists_menu"),
            ],
            [
                InlineKeyboardButton("⚙️ Settings", callback_data="settings_menu"),
                InlineKeyboardButton("❓ Help", callback_data="help_menu"),
            ]
        ])
    
    @staticmethod
    def music_controls() -> InlineKeyboardMarkup:
        """Music player controls"""
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⏸ Pause", callback_data="pause_music"),
                InlineKeyboardButton("▶ Resume", callback_data="resume_music"),
                InlineKeyboardButton("⏭ Skip", callback_data="skip_music"),
            ],
            [
                InlineKeyboardButton("🔁 Loop", callback_data="toggle_loop"),
                InlineKeyboardButton("⏹ Stop", callback_data="stop_music"),
            ],
            [
                InlineKeyboardButton("📜 Queue", callback_data="show_queue"),
                InlineKeyboardButton("🏠 Home", callback_data="main_menu_back"),
            ]
        ])
    
    @staticmethod
    def search_results(results_count: int) -> InlineKeyboardMarkup:
        """Search results keyboard"""
        buttons = []
        for i in range(min(5, results_count)):
            buttons.append([
                InlineKeyboardButton(f"▶ Play Result {i+1}", callback_data=f"play_result_{i}")
            ])
        buttons.append([InlineKeyboardButton("🏠 Back", callback_data="main_menu_back")])
        return InlineKeyboardMarkup(buttons)
    
    @staticmethod
    def queue_actions() -> InlineKeyboardMarkup:
        """Queue management keyboard"""
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⬆ Previous", callback_data="queue_prev"),
                InlineKeyboardButton("⬇ Next", callback_data="queue_next"),
            ],
            [
                InlineKeyboardButton("🗑 Clear Queue", callback_data="clear_queue"),
                InlineKeyboardButton("🏠 Home", callback_data="main_menu_back"),
            ]
        ])
    
    @staticmethod
    def playlist_menu() -> InlineKeyboardMarkup:
        """Playlist management keyboard"""
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("➕ Create", callback_data="create_playlist"),
                InlineKeyboardButton("📋 View", callback_data="view_playlists"),
            ],
            [
                InlineKeyboardButton("➕ Add to Playlist", callback_data="add_to_playlist"),
                InlineKeyboardButton("🏠 Home", callback_data="main_menu_back"),
            ]
        ])
    
    @staticmethod
    def settings_menu() -> InlineKeyboardMarkup:
        """Settings keyboard"""
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🌍 Language", callback_data="language_settings"),
                InlineKeyboardButton("🔊 Volume", callback_data="volume_settings"),
            ],
            [
                InlineKeyboardButton("👤 Admin", callback_data="admin_settings"),
                InlineKeyboardButton("ℹ️ About", callback_data="about_bot"),
            ],
            [
                InlineKeyboardButton("🏠 Home", callback_data="main_menu_back"),
            ]
        ])
    
    @staticmethod
    def admin_controls() -> InlineKeyboardMarkup:
        """Admin only controls"""
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🚫 Kick User", callback_data="kick_user"),
                InlineKeyboardButton("⛔ Ban User", callback_data="ban_user"),
            ],
            [
                InlineKeyboardButton("🔇 Mute VC", callback_data="mute_vc"),
                InlineKeyboardButton("🔊 Unmute VC", callback_data="unmute_vc"),
            ],
            [
                InlineKeyboardButton("🏠 Home", callback_data="main_menu_back"),
            ]
        ])
    
    @staticmethod
    def help_keyboard() -> InlineKeyboardMarkup:
        """Help menu keyboard"""
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🎵 Commands", callback_data="commands_help"),
                InlineKeyboardButton("🔧 Troubleshooting", callback_data="troubleshoot_help"),
            ],
            [
                InlineKeyboardButton("📞 Support", callback_data="support_help"),
                InlineKeyboardButton("🏠 Home", callback_data="main_menu_back"),
            ]
        ])
