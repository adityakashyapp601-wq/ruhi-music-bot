"""
✦ ʀᴜʜɪ 𝐗 ᴍᴜꜱɪᴄ ✦ - Main Bot File
Telegram Music & Video Bot with GC Manager
"""

import logging
import io
from pyrogram import Client, filters, types
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from pyrogram.errors import PeerIdInvalid
import asyncio
from config import API_ID, API_HASH, BOT_TOKEN, ADMIN_IDS, BOT_NAME
from keyboards import Keyboards
from database import db
from utils import youtube, formatter
from PIL import Image, ImageDraw, ImageFont

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Pyrogram Client
app = Client(
    "RuhiMusicBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Global variables for VC state
vc_sessions = {}
paused_videos = {}
current_playing = {}
broadcast_messages = {}

# ================== WELCOME MESSAGE GENERATOR ==================

async def create_welcome_poster(user, group_chat):
    """Create welcome poster with user info"""
    try:
        # Create image
        img = Image.new('RGB', (800, 600), color=(20, 20, 30))
        draw = ImageDraw.Draw(img)
        
        # Try to load fonts, fallback to default
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 50)
            text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 35)
            small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 25)
        except:
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Draw gradient effect (simple)
        for y in range(600):
            r = int(20 + (100 - 20) * (y / 600))
            color = (r, 20, 50)
            draw.line([(0, y), (800, y)], fill=color)
        
        # Title
        title = "🎵 WELCOME 🎵"
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        draw.text(((800 - title_width) / 2, 30), title, fill=(0, 255, 150), font=title_font)
        
        # User info
        user_name = user.first_name if user.first_name else "User"
        user_text = f"Name: {user_name}"
        draw.text((50, 150), user_text, fill=(255, 255, 255), font=text_font)
        
        # Username
        username = user.username or "No username"
        username_text = f"@{username}"
        draw.text((50, 220), username_text, fill=(0, 200, 255), font=text_font)
        
        # User ID
        user_id_text = f"ID: {user.id}"
        draw.text((50, 290), user_id_text, fill=(200, 200, 200), font=small_font)
        
        # Group name
        group_text = f"Group: {group_chat.title}"
        draw.text((50, 360), group_text, fill=(255, 200, 100), font=text_font)
        
        # Members count
        try:
            members_count = await app.get_chat_members_count(group_chat.id)
            members_text = f"Members: {members_count}"
        except:
            members_text = "Members: N/A"
        
        draw.text((50, 430), members_text, fill=(150, 255, 150), font=text_font)
        
        # Footer
        footer = "✦ ʀᴜʜɪ 𝐗 ᴍᴜꜱɪᴄ ✦"
        footer_bbox = draw.textbbox((0, 0), footer, font=small_font)
        footer_width = footer_bbox[2] - footer_bbox[0]
        draw.text(((800 - footer_width) / 2, 520), footer, fill=(255, 100, 200), font=small_font)
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return img_byte_arr
    except Exception as e:
        logger.error(f"Error creating poster: {e}")
        return None

# ================== NEW MEMBER HANDLER ==================

@app.on_message(filters.group & filters.new_chat_members)
async def welcome_new_member(client: Client, message: Message):
    """Welcome new members to group"""
    for member in message.new_chat_members:
        try:
            # Get user profile picture
            user_pfp = None
            try:
                user_pfp = await client.get_profile_photos(member.id, limit=1)
                if user_pfp:
                    user_pfp = await client.download_media(user_pfp[0])
            except:
                pass
            
            # Create poster
            poster = await create_welcome_poster(member, message.chat)
            
            # Welcome text
            welcome_msg = f"""
╔━━━━━━━━━━━━━━━━━━━━━━╗
║     🎵 ʀᴜʜɪ ᴡᴇʟᴄᴏᴍᴇꜱ ʏᴏᴜ! 🎵
╚━━━━━━━━━━━━━━━━━━━━━━╝

👋 **नमस्ते {member.first_name}!**

✨ **आपको {message.chat.title} में स्वागत है!**

━━━━━━━━━━━━━━━━━━━━
📊 **Your Profile:**
━━━━━━━━━━━━━━━━━━━━

👤 **Name:** {member.first_name} {member.last_name if member.last_name else ''}
📱 **Username:** @{member.username if member.username else 'Not Set'}
🆔 **User ID:** `{member.id}`
📍 **Joined:** {message.chat.title}

━━━━━━━━━━━━━━━━━━━━
🎵 **Bot Features:**
━━━━━━━━━━━━━━━━━━━━

🎶 **Music:** Play songs from YouTube
🎬 **Videos:** Watch videos in voice chat
📜 **Queue:** Manage song queue easily
👑 **Admin Tools:** Manage group like a pro
🎧 **Playlists:** Create & save playlists

━━━━━━━━━━━━━━━━━━━━
📝 **Quick Commands:**
━━━━━━━━━━━━━━━━━━━━

/help - सभी commands देखें
/play [song] - गाना बजाएं
/vplay [video] - विडियो चलाएं
/queue - Queue देखें
/kick - User को kick करें
/ban - User को ban करें

━━━━━━━━━━━━━━━━━━━━

✦ ʀᴜʜɪ 𝐗 ᴍᴜꜱɪᴄ ✦
Bot Version 1.0.0 ✨
"""
            
            # Send poster with welcome message
            if poster:
                await message.reply_photo(
                    photo=poster,
                    caption=welcome_msg,
                    reply_markup=Keyboards.main_menu()
                )
            else:
                await message.reply_text(welcome_msg, reply_markup=Keyboards.main_menu())
        
        except Exception as e:
            logger.error(f"Welcome error: {e}")
            simple_welcome = f"👋 Welcome {member.mention} to {message.chat.title}! 🎵"
            await message.reply_text(simple_welcome)

# ================== START & HELP ==================

@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    """Start command with inline buttons"""
    welcome_text = f"""
╔━━━━━━━━━━━━━━━━━━╗
║ ✦ ʀᴜʜɪ 𝐗 ᴍᴜꜱɪᴄ ✦
║ 🎵 Music & Video Bot
╚━━━━━━━━━━━━━━━━━╝

👋 **Namaste {message.from_user.first_name}!**

Mein ek professional music & video bot hoon. Mujhe use karke aap:

🎵 **Music Features:**
• YouTube se gaane play kar sakte ho
• Queue manage kar sakte ho
• Pause, Resume, Skip kar sakte ho
• Loop enable kar sakte ho
• Playlists banaa sakte ho

🎬 **Video Features:**
• YouTube videos play kar sakte ho VC mein
• Video controls (pause, resume, skip)
• Video queue dekhna

👑 **GC Manager:**
• Users ko kick/ban kar sakte ho
• Mute/Unmute kar sakte ho
• User promote/demote kar sakte ho

📝 **/help** par tap karke commands dekhlo!
"""
    await message.reply_text(
        welcome_text,
        reply_markup=Keyboards.main_menu(),
        disable_web_page_preview=True
    )

@app.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    """Help command"""
    help_text = """
🎵 **MUSIC COMMANDS:**
/play [song name/URL] - Gaana play karo
/pause - Gaana pause karo
/resume - Gaana resume karo
/skip - Agle gaane par jao
/queue - Queue dekhо
/loop - Loop toggle karo
/stop - Bot band karo
/search [query] - YouTube search

🎬 **VIDEO COMMANDS:**
/vplay [video URL] - Video play karo VC mein
/vpause - Video pause karo
/vresume - Video resume karo
/vskip - Video skip karo
/vqueue - Video queue dekhо
/vstop - Video stop karo

👑 **GC MANAGER COMMANDS:**
/kick [@user] - User kick karo
/ban [@user] - User ban karo
/mute [@user] - User mute karo
/unmute [@user] - User unmute karo
/promote [@user] - Admin banao
/demote [@user] - Admin hatao
/warn [@user] [reason] - User ko warn do
/members - Group members list

📂 **PLAYLIST COMMANDS:**
/playlist - Playlists dekhо
/createpl [name] - Naya playlist banao
/addtopl [name] - Gaana playlist mein add karo

⚙️ **OTHER COMMANDS:**
/ping - Bot ka ping check karo
/stats - Bot statistics
/about - Bot ke baare mein
/settings - Settings change karo
"""
    await message.reply_text(help_text, reply_markup=Keyboards.help_keyboard())

# ================== MUSIC COMMANDS ==================

@app.on_message(filters.command("play"))
async def play_command(client: Client, message: Message):
    """Play song command"""
    if not message.text.split(None, 1)[1:]:
        await message.reply_text("❌ Usage: /play [song name or YouTube URL]")
        return
    
    query = message.text.split(None, 1)[1]
    chat_id = message.chat.id
    
    await message.reply_text("🔍 Searching for song...")
    
    # Search on YouTube
    results = await youtube.search(query, limit=1)
    
    if not results:
        await message.reply_text("❌ No songs found!")
        return
    
    song = results[0]
    db.add_to_queue(chat_id, song)
    db.set_now_playing(chat_id, song)
    
    song_info = f"""
🎵 **Now Playing:**

**Title:** {song['title']}
**Duration:** {formatter.format_duration(song['duration'])}
**Uploader:** {song['uploader']}
**Views:** {song['views']:,}

✅ Added to queue!
"""
    await message.reply_text(
        song_info,
        reply_markup=Keyboards.music_controls()
    )

@app.on_message(filters.command("pause"))
async def pause_command(client: Client, message: Message):
    """Pause music"""
    chat_id = message.chat.id
    if chat_id in current_playing:
        paused_videos[chat_id] = True
        await message.reply_text("⏸ Music paused!")
    else:
        await message.reply_text("❌ No music playing!")

@app.on_message(filters.command("resume"))
async def resume_command(client: Client, message: Message):
    """Resume music"""
    chat_id = message.chat.id
    if chat_id in paused_videos:
        paused_videos[chat_id] = False
        await message.reply_text("▶ Music resumed!")
    else:
        await message.reply_text("❌ No paused music!")

@app.on_message(filters.command("skip"))
async def skip_command(client: Client, message: Message):
    """Skip to next song"""
    chat_id = message.chat.id
    queue = db.get_queue(chat_id)
    
    if not queue:
        await message.reply_text("❌ Queue is empty!")
        return
    
    db.remove_from_queue(chat_id, 0)
    await message.reply_text("⏭ Skipped to next song!")

@app.on_message(filters.command("queue"))
async def queue_command(client: Client, message: Message):
    """Show queue"""
    chat_id = message.chat.id
    queue = db.get_queue(chat_id)
    
    queue_text = formatter.create_queue_text(queue)
    await message.reply_text(
        queue_text,
        reply_markup=Keyboards.queue_actions()
    )

@app.on_message(filters.command("loop"))
async def loop_command(client: Client, message: Message):
    """Toggle loop"""
    chat_id = message.chat.id
    is_loop = db.toggle_loop(chat_id)
    
    status = "🔁 **Loop enabled!**" if is_loop else "🔁 **Loop disabled!**"
    await message.reply_text(status)

@app.on_message(filters.command("stop"))
async def stop_command(client: Client, message: Message):
    """Stop music"""
    chat_id = message.chat.id
    db.clear_queue(chat_id)
    current_playing.pop(chat_id, None)
    paused_videos.pop(chat_id, None)
    
    await message.reply_text("⏹ Music stopped!")

@app.on_message(filters.command("search"))
async def search_command(client: Client, message: Message):
    """Search songs"""
    if not message.text.split(None, 1)[1:]:
        await message.reply_text("❌ Usage: /search [query]")
        return
    
    query = message.text.split(None, 1)[1]
    await message.reply_text("🔍 Searching...")
    
    results = await youtube.search(query, limit=5)
    
    if not results:
        await message.reply_text("❌ No results found!")
        return
    
    search_text = "🔍 **Search Results:**\n\n"
    for i, result in enumerate(results, 1):
        search_text += f"{i}. **{result['title']}**\n"
        search_text += f"   ⏱ {formatter.format_duration(result['duration'])} | 👤 {result['uploader']}\n\n"
    
    await message.reply_text(
        search_text,
        reply_markup=Keyboards.search_results(len(results))
    )

# ================== VIDEO COMMANDS ==================

@app.on_message(filters.command("vplay"))
async def vplay_command(client: Client, message: Message):
    """Play video in voice chat"""
    if not message.text.split(None, 1)[1:]:
        await message.reply_text("❌ Usage: /vplay [YouTube URL or video name]")
        return
    
    query = message.text.split(None, 1)[1]
    chat_id = message.chat.id
    
    await message.reply_text("🎬 Searching for video...")
    
    # Search video
    results = await youtube.search(query, limit=1)
    
    if not results:
        await message.reply_text("❌ Video not found!")
        return
    
    video = results[0]
    current_playing[chat_id] = video
    
    video_info = f"""
🎬 **Now Playing (Video):**

**Title:** {video['title']}
**Duration:** {formatter.format_duration(video['duration'])}
**Uploader:** {video['uploader']}
**Views:** {video['views']:,}

📹 Video playing in voice chat!
"""
    await message.reply_text(
        video_info,
        reply_markup=Keyboards.music_controls()
    )

@app.on_message(filters.command("vpause"))
async def vpause_command(client: Client, message: Message):
    """Pause video"""
    chat_id = message.chat.id
    if chat_id in current_playing:
        paused_videos[chat_id] = True
        await message.reply_text("⏸ Video paused!")
    else:
        await message.reply_text("❌ No video playing!")

@app.on_message(filters.command("vresume"))
async def vresume_command(client: Client, message: Message):
    """Resume video"""
    chat_id = message.chat.id
    if chat_id in paused_videos:
        paused_videos[chat_id] = False
        await message.reply_text("▶ Video resumed!")
    else:
        await message.reply_text("❌ No paused video!")

@app.on_message(filters.command("vskip"))
async def vskip_command(client: Client, message: Message):
    """Skip video"""
    chat_id = message.chat.id
    queue = db.get_queue(chat_id)
    
    if queue:
        db.remove_from_queue(chat_id, 0)
        await message.reply_text("⏭ Skipped to next video!")
    else:
        await message.reply_text("❌ No more videos in queue!")

@app.on_message(filters.command("vqueue"))
async def vqueue_command(client: Client, message: Message):
    """Show video queue"""
    chat_id = message.chat.id
    queue = db.get_queue(chat_id)
    
    queue_text = formatter.create_queue_text(queue)
    await message.reply_text(queue_text)

@app.on_message(filters.command("vstop"))
async def vstop_command(client: Client, message: Message):
    """Stop video"""
    chat_id = message.chat.id
    db.clear_queue(chat_id)
    current_playing.pop(chat_id, None)
    
    await message.reply_text("⏹ Video stopped!")

# ================== GC MANAGER COMMANDS ==================

@app.on_message(filters.command("kick"))
async def kick_command(client: Client, message: Message):
    """Kick user from group"""
    if not message.reply_to_message:
        await message.reply_text("❌ Reply to a message to kick that user!")
        return
    
    user_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id
    
    # Check if admin
    member = await client.get_chat_member(chat_id, message.from_user.id)
    if not member.privileges or not member.privileges.can_delete_messages:
        await message.reply_text("❌ You don't have permission to kick users!")
        return
    
    try:
        await client.ban_chat_member(chat_id, user_id)
        await asyncio.sleep(1)
        await client.unban_chat_member(chat_id, user_id)
        await message.reply_text(f"👋 User {user_id} kicked from group!")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@app.on_message(filters.command("ban"))
async def ban_command(client: Client, message: Message):
    """Ban user from group"""
    if not message.reply_to_message:
        await message.reply_text("❌ Reply to a message to ban that user!")
        return
    
    user_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id
    
    # Check if admin
    member = await client.get_chat_member(chat_id, message.from_user.id)
    if not member.privileges or not member.privileges.can_delete_messages:
        await message.reply_text("❌ You don't have permission to ban users!")
        return
    
    try:
        await client.ban_chat_member(chat_id, user_id)
        await message.reply_text(f"🚫 User {user_id} banned from group!")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@app.on_message(filters.command("mute"))
async def mute_command(client: Client, message: Message):
    """Mute user"""
    if not message.reply_to_message:
        await message.reply_text("❌ Reply to a message to mute that user!")
        return
    
    user_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id
    
    try:
        await client.restrict_chat_member(
            chat_id,
            user_id,
            types.ChatPermissions(can_send_messages=False)
        )
        await message.reply_text(f"🔇 User {user_id} muted!")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@app.on_message(filters.command("unmute"))
async def unmute_command(client: Client, message: Message):
    """Unmute user"""
    if not message.reply_to_message:
        await message.reply_text("❌ Reply to a message to unmute that user!")
        return
    
    user_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id
    
    try:
        await client.restrict_chat_member(
            chat_id,
            user_id,
            types.ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        await message.reply_text(f"🔊 User {user_id} unmuted!")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@app.on_message(filters.command("warn"))
async def warn_command(client: Client, message: Message):
    """Warn user"""
    if not message.reply_to_message:
        await message.reply_text("❌ Reply to a message to warn that user!")
        return
    
    reason = " ".join(message.command[1:]) or "No reason specified"
    user = message.reply_to_message.from_user
    
    await message.reply_text(
        f"⚠️ **User Warned!**\n\n"
        f"**User:** {user.mention}\n"
        f"**Reason:** {reason}\n"
        f"**By:** {message.from_user.mention}"
    )

@app.on_message(filters.command("promote"))
async def promote_command(client: Client, message: Message):
    """Promote user to admin"""
    if not message.reply_to_message:
        await message.reply_text("❌ Reply to a message to promote that user!")
        return
    
    user_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id
    
    try:
        await client.promote_chat_member(
            chat_id,
            user_id,
            privileges=types.ChatPrivileges(
                can_manage_chat=True,
                can_delete_messages=True,
                can_manage_video_chats=True,
                can_restrict_members=True,
                can_promote_members=True,
                can_change_info=True,
                can_invite_users=True,
                can_pin_messages=True,
            )
        )
        await message.reply_text(f"👑 User {user_id} promoted to admin!")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@app.on_message(filters.command("demote"))
async def demote_command(client: Client, message: Message):
    """Demote admin to user"""
    if not message.reply_to_message:
        await message.reply_text("❌ Reply to a message to demote that user!")
        return
    
    user_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id
    
    try:
        await client.promote_chat_member(
            chat_id,
            user_id,
            privileges=types.ChatPrivileges()
        )
        await message.reply_text(f"📉 User {user_id} demoted!")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@app.on_message(filters.command("members"))
async def members_command(client: Client, message: Message):
    """Show group members"""
    chat_id = message.chat.id
    
    try:
        members = await client.get_chat_members(chat_id)
        members_text = "👥 **Group Members:**\n\n"
        
        count = 0
        for member in members:
            if count >= 20:
                members_text += f"\n... and {len(members) - 20} more members"
                break
            members_text += f"• {member.user.mention}\n"
            count += 1
        
        await message.reply_text(members_text)
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

# ================== PLAYLIST COMMANDS ==================

@app.on_message(filters.command("playlist"))
async def playlist_command(client: Client, message: Message):
    """Show playlists"""
    chat_id = message.chat.id
    
    if chat_id not in db.playlists or not db.playlists[chat_id]:
        await message.reply_text("❌ No playlists created yet!")
        return
    
    playlist_text = "📂 **Your Playlists:**\n\n"
    for name, songs in db.playlists[chat_id].items():
        playlist_text += f"📋 **{name}** - {len(songs)} songs\n"
    
    await message.reply_text(playlist_text)

@app.on_message(filters.command("createpl"))
async def createpl_command(client: Client, message: Message):
    """Create new playlist"""
    if not message.text.split(None, 1)[1:]:
        await message.reply_text("❌ Usage: /createpl [playlist name]")
        return
    
    name = message.text.split(None, 1)[1]
    chat_id = message.chat.id
    
    db.create_playlist(chat_id, name)
    await message.reply_text(f"✅ Playlist '{name}' created!")

# ================== BROADCAST COMMAND (OWNER ONLY) ==================

@app.on_message(filters.command("broadcast") & filters.user(ADMIN_IDS))
async def broadcast_command(client: Client, message: Message):
    """Broadcast message to all chats (Owner only)"""
    if not message.reply_to_message:
        await message.reply_text("❌ Reply to a message to broadcast!")
        return
    
    broadcast_msg = message.reply_to_message
    
    try:
        sent = 0
        failed = 0
        
        # Get all chat IDs from database
        all_chats = list(set(list(db.queues.keys()) + list(db.playlists.keys())))
        
        await message.reply_text(f"📢 Broadcasting to {len(all_chats)} chats...")
        
        for chat_id in all_chats:
            try:
                if broadcast_msg.text:
                    await app.send_message(chat_id, broadcast_msg.text)
                elif broadcast_msg.photo:
                    await app.send_photo(chat_id, broadcast_msg.photo.file_id, caption=broadcast_msg.caption or "")
                elif broadcast_msg.video:
                    await app.send_video(chat_id, broadcast_msg.video.file_id, caption=broadcast_msg.caption or "")
                elif broadcast_msg.document:
                    await app.send_document(chat_id, broadcast_msg.document.file_id, caption=broadcast_msg.caption or "")
                sent += 1
                await asyncio.sleep(0.1)  # Avoid flood
            except Exception as e:
                failed += 1
        
        result_text = f"""
✅ **Broadcast Complete!**

📊 **Statistics:**
✔️ Sent: {sent}
❌ Failed: {failed}
📝 Total: {len(all_chats)}
"""
        await message.reply_text(result_text)
        logger.info(f"Broadcast: Sent to {sent} chats, Failed: {failed}")
    
    except Exception as e:
        await message.reply_text(f"❌ Broadcast error: {str(e)}")

# ================== OTHER COMMANDS ==================

@app.on_message(filters.command("ping"))
async def ping_command(client: Client, message: Message):
    """Bot ping"""
    await message.reply_text("🏓 **Pong!** Bot is active! ✅")

@app.on_message(filters.command("about"))
async def about_command(client: Client, message: Message):
    """About bot"""
    about_text = f"""
╔━━━━━━━━━━━━━━━━━━╗
║ ✦ ʀᴜʜɪ 𝐗 ᴍᴜꜱɪᴄ ✦
╚━━━━━━━━━━━━━━━━━╝

🎵 **Advanced Telegram Music & Video Bot**

**Features:**
✅ YouTube Music Search
✅ Voice Chat Music Playing
✅ Video Playing with VC Support
✅ Queue Management
✅ Playlist Support
✅ GC Manager Tools
✅ Admin Controls
✅ Broadcast System

**Made With:** ❤️ Pyrogram
**Version:** 1.0.0
**Developer:** Aditya ✨

👨‍💻 Support & Feedback: Soon!
"""
    await message.reply_text(about_text)

# ================== CALLBACK QUERIES ==================

@app.on_callback_query()
async def handle_callbacks(client: Client, callback_query: CallbackQuery):
    """Handle inline button callbacks"""
    chat_id = callback_query.message.chat.id
    data = callback_query.data
    
    if data == "main_menu_back":
        await callback_query.edit_message_text(
            "🏠 **Main Menu**",
            reply_markup=Keyboards.main_menu()
        )
    
    elif data == "show_queue":
        queue = db.get_queue(chat_id)
        queue_text = formatter.create_queue_text(queue)
        await callback_query.edit_message_text(
            queue_text,
            reply_markup=Keyboards.queue_actions()
        )
    
    elif data == "toggle_loop":
        is_loop = db.toggle_loop(chat_id)
        status = "🔁 Loop: ON" if is_loop else "🔁 Loop: OFF"
        await callback_query.answer(status, show_alert=True)
    
    elif data == "help_menu":
        help_text = "ℹ️ **Need help? Use /help command!**"
        await callback_query.edit_message_text(help_text)

# ================== BOT START ==================

async def main():
    """Start the bot"""
    await app.start()
    logger.info(f"✦ ʀᴜʜɪ 𝐗 ᴍᴜꜱɪᴄ ✦ is running! 🎵")
    logger.info("Bot started successfully!")
    await app.idle()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped!")
