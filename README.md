```markdown
# ✦ ʀᴜʜɪ 𝐗 ᴍᴜꜱɪᴄ ✦

🎵 Advanced Telegram Music & Video Bot with GC Manager

## 📋 Features

### 🎵 Music Features
- 🔍 YouTube Music Search
- ⏯️ Play, Pause, Resume, Skip
- 📜 Queue Management
- 🔁 Loop Toggle
- 📂 Playlists Support
- 🎧 High Quality Audio

### 🎬 Video Features
- 📹 YouTube Video Playback in VC
- ⏸️ Video Controls (Pause/Resume/Skip)
- 📋 Video Queue Management
- 🎞️ Full Video Support

### 👑 GC Manager Features
- 🚫 Kick Users
- ⛔ Ban Users
- 🔇 Mute/Unmute Users
- 👤 Promote/Demote Admins
- ⚠️ Warn System
- 👥 Member Management
- 🎉 Welcome Messages with Posters

### 📢 Admin Features
- 📢 Broadcast Messages (Owner Only)
- ⚙️ Settings Management
- 📊 Bot Statistics

## 🚀 Quick Setup

### Prerequisites
- Python 3.8+
- Telegram Account
- Bot Token from @BotFather
- API_ID and API_HASH from my.telegram.org

### Installation

1. **Clone Repository**
```bash
git clone https://github.com/adityakashyapp601-wq/ruhi-music-bot.git
cd ruhi-music-bot
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup Environment**
```bash
cp .env.example .env
```

4. **Edit .env File**
```env
API_ID=YOUR_API_ID
API_HASH=YOUR_API_HASH
BOT_TOKEN=YOUR_BOT_TOKEN
ADMIN_IDS=YOUR_USER_ID,OTHER_ADMIN_IDS
```

### Getting API Credentials

#### Step 1: Get API_ID and API_HASH
1. Go to https://my.telegram.org
2. Login with your Telegram account
3. Click "API development tools"
4. Create new application
5. Copy `api_id` and `api_hash`

#### Step 2: Get Bot Token
1. Open Telegram and search @BotFather
2. Send `/newbot` command
3. Follow the steps
4. Copy the bot token

#### Step 3: Get Your User ID
1. Send `/id` to @userinfobot
2. Copy your user ID
3. Add it to ADMIN_IDS in .env

## 📝 Commands

### 🎵 Music Commands
```
/play [song name/URL]  - Play a song
/pause                 - Pause music
/resume                - Resume music
/skip                  - Skip to next song
/queue                 - Show queue
/loop                  - Toggle loop
/stop                  - Stop music
/search [query]        - Search songs
```

### 🎬 Video Commands
```
/vplay [video URL]     - Play video in VC
/vpause                - Pause video
/vresume               - Resume video
/vskip                 - Skip video
/vqueue                - Show video queue
/vstop                 - Stop video
```

### 👑 GC Manager Commands
```
/kick [@user]          - Kick user from group
/ban [@user]           - Ban user permanently
/mute [@user]          - Mute user
/unmute [@user]        - Unmute user
/promote [@user]       - Promote to admin
/demote [@user]        - Demote from admin
/warn [@user] [reason] - Warn user
/members               - Show group members
```

### 📂 Playlist Commands
```
/playlist              - Show all playlists
/createpl [name]       - Create new playlist
/addtopl [name]        - Add song to playlist
```

### 📢 Admin Commands
```
/broadcast             - Broadcast message (Owner only)
                        (Reply to message to broadcast)
```

### ℹ️ Other Commands
```
/start                 - Start bot
/help                  - Show all commands
/ping                  - Check bot status
/about                 - About bot
```

## 📊 File Structure

```
ruhi-music-bot/
├── bot.py              # Main bot file with all commands
├── config.py           # Configuration and settings
├── keyboards.py        # Inline button keyboards
├── database.py         # Queue & playlist database
├── utils.py            # YouTube search & utilities
├── requirements.txt    # Python dependencies
├── .env.example        # Environment template
└── README.md           # This file
```

## ▶️ Running the Bot

```bash
python bot.py
```

Or with logging:
```bash
python -u bot.py
```

## 🎯 Features in Detail

### Welcome Message with Poster
When a new user joins:
- Beautiful welcome poster with user info
- Shows user name, username, ID
- Shows group name and member count
- Auto-sent to new members

### Music Queue System
- Add unlimited songs
- View current queue
- Skip to next song
- Loop individual songs
- Clear entire queue

### Video Playback
- Stream YouTube videos in voice chat
- Full video quality support
- Queue management for videos
- Pause/Resume/Skip controls

### GC Management
- Complete moderation tools
- User warning system
- Admin promotion/demotion
- Mute/Unmute capabilities
- Member management

### Broadcast System
- Owner-only broadcast feature
- Send messages to all groups
- Supports text, photo, video, documents
- Flood protection with delays

## ⚡ Performance Tips

1. **Use better server** for hosting
2. **Enable logging** to debug issues
3. **Keep database files** in sync
4. **Use asyncio** for better performance
5. **Clear old queues** regularly

## 🐛 Troubleshooting

### Bot not responding
- Check if bot is running: `/ping`
- Verify API credentials in .env
- Check bot token validity

### Commands not working
- Make sure bot is added to group
- Check if you have required permissions
- Use `/help` to verify command format

### Music not playing
- Check internet connection
- Verify YouTube is accessible
- Try different song query

### Permission denied errors
- Make sure bot is admin in group
- Grant necessary permissions to bot
- Check user permissions for GC commands

## 📞 Support

For issues and feature requests, create an issue on GitHub.

## 📄 License

This project is free to use and modify.

## 🙏 Credits

- Made with ❤️ by Aditya
- Uses Pyrogram library
- YouTube playback via yt-dlp

---

**Version:** 1.0.0  
**Last Updated:** 2024  
**Status:** ✅ Active & Working

✦ ʀᴜʜɪ 𝐗 ᴍᴜꜱɪᴄ ✦ 🎵
```
