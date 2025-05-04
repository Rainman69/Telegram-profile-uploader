import asyncio
import os
import datetime
from telethon import TelegramClient, events
from telethon.tl.types import User, Channel
from telethon.errors import FloodWaitError
from telethon.tl.functions.channels import CreateChannelRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest

# Replace with your API ID and hash from my.telegram.org
api_id = 1234567  # e.g., 1234567
api_hash = '11111111111111111'  # e.g., 'your32characterhash'

# Initialize the Telegram client
client = TelegramClient('session', api_id, api_hash)

# Name of the dedicated channel
CHANNEL_NAME = "tgprof Processing Channel"

# Create downloads directory for storing images
if not os.path.exists('downloads'):
    os.makedirs('downloads')

# Logging function with timestamps
def log(message):
    print(f"[{datetime.datetime.now()}] {message}")

# Queue for uploading profile pictures
upload_queue = asyncio.Queue()

# Event to control pausing and resuming
pause_event = asyncio.Event()
pause_event.set()  # Initially not paused

# Function to find or create the dedicated channel
async def get_or_create_channel():
    """Finds the dedicated channel or creates it if it doesn’t exist."""
    async for dialog in client.iter_dialogs():
        if dialog.name == CHANNEL_NAME and isinstance(dialog.entity, Channel):
            log(f"Found existing channel: {CHANNEL_NAME}")
            return dialog.entity
    # If not found, create a new private channel
    try:
        result = await client(CreateChannelRequest(
            title=CHANNEL_NAME,
            about="Channel for tgprof script processing",
            megagroup=False  # False for channel, True for supergroup
        ))
        channel = result.chats[0]
        log(f"Created new channel: {CHANNEL_NAME}")
        return channel
    except Exception as e:
        log(f"Error creating channel: {e}")
        raise

# Worker to process the upload queue
async def upload_worker():
    """Processes the upload queue, uploading images as profile pictures with delays."""
    while True:
        await pause_event.wait()  # Wait if paused
        image_path = await upload_queue.get()
        while True:
            try:
                # Upload the file to Telegram
                file = await client.upload_file(image_path)
                # Set the uploaded file as the profile photo
                await client(UploadProfilePhotoRequest(file=file))
                log(f"Uploaded profile picture: {image_path}")
                break
            except FloodWaitError as e:
                log(f"Flood wait for {e.seconds} seconds")
                await asyncio.sleep(e.seconds)
            except Exception as e:
                log(f"Error uploading {image_path}: {e}")
                break
        upload_queue.task_done()
        await asyncio.sleep(61)  # Additional delay to respect rate limits

# Main function to run the client and worker
async def main():
    """Starts the client, gets or creates the channel, sets up the event handler, and runs the upload worker."""
    await client.start()
    log("Script started")
    # Get or create the dedicated channel
    dedicated_channel = await get_or_create_channel()
    # Define the event handler for the specific channel
    @client.on(events.NewMessage(chats=dedicated_channel))
    async def handler(event):
        log(f"Received message in channel: {event.chat_id}")
        # Process images sent to the channel
        if event.message.photo:
            file = os.path.join('downloads', f"{event.message.id}_{event.message.photo.id}.jpg")
            await client.download_media(event.message, file=file)
            await upload_queue.put(file)
            log(f"Added to queue: {file}")
        # Process text commands or cloning requests
        elif event.message.text:
            text = event.message.text.lower()
            # Control commands
            if text == 'stop':
                log("Stopping script")
                await client.disconnect()
            elif text == 'pause':
                pause_event.clear()
                log("Paused")
            elif text == 'continue':
                pause_event.set()
                log("Continued")
            elif text == 'start':
                log("Script is running")
            # Cloning command: @ID number
            elif text.startswith('@'):
                parts = text.split()
                if len(parts) == 2 and parts[1].isdigit():
                    entity_str = parts[0][1:]  # Remove '@'
                    number = int(parts[1])
                    try:
                        entity = await client.get_entity(entity_str)
                        # Clone user profile pictures
                        if isinstance(entity, User):
                            photos = await client.get_profile_photos(entity)
                            for photo in photos[:number]:
                                file = os.path.join('downloads', f"profile_{entity.id}_{photo.id}.jpg")
                                await client.download_media(photo, file=file)
                                await upload_queue.put(file)
                                log(f"Added to queue: {file}")
                        # Clone images from channel messages
                        elif isinstance(entity, Channel):
                            photos_collected = 0
                            async for message in client.iter_messages(entity):
                                if message.photo:
                                    file = os.path.join('downloads', f"channel_{entity.id}_{message.id}_{message.photo.id}.jpg")
                                    await client.download_media(message, file=file)
                                    await upload_queue.put(file)
                                    log(f"Added to queue: {file}")
                                    photos_collected += 1
                                    if photos_collected >= number:
                                        break
                    except Exception as e:
                        log(f"Error handling cloning: {e}")
                else:
                    log(f"Invalid cloning command: {text}")

    # Start the upload worker
    asyncio.create_task(upload_worker())
    # Run the client until disconnected
    await client.run_until_disconnected()

# Entry point
if __name__ == '__main__':
    asyncio.run(main())