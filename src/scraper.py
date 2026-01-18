import os
import json
import logging
from datetime import datetime
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from dotenv import load_dotenv

load_dotenv()

# Setup logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(filename='logs/scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Telegram API credentials from .env
api_id = int(os.getenv('TELEGRAM_API_ID'))
api_hash = os.getenv('TELEGRAM_API_HASH')
phone = os.getenv('TELEGRAM_PHONE')

# Channels to scrape (add more from et.tgstat.com/medicine)
channels = [
    'CheMed123',  # Chemed
    'lobelia4cosmetics',
    'tikvahpharma',
    # Add more, e.g., 'another_channel'
]

async def scrape_channel(client, channel_name):
    try:
        entity = await client.get_entity(channel_name)
        messages = []
        async for message in client.iter_messages(entity, limit=100):  # Adjust limit as needed
            msg_data = {
                'message_id': message.id,
                'channel_name': channel_name,
                'message_date': message.date.isoformat(),
                'message_text': message.text,
                'has_media': message.media is not None,
                'image_path': None,
                'views': message.views,
                'forwards': message.forwards
            }
            
            # Download image if present
            if message.photo:
                date_str = message.date.strftime('%Y-%m-%d')
                img_dir = f'data/raw/images/{channel_name}'
                os.makedirs(img_dir, exist_ok=True)
                img_path = f'{img_dir}/{message.id}.jpg'
                await message.download_media(img_path)
                msg_data['image_path'] = img_path
            
            messages.append(msg_data)
        
        # Save to JSON in data lake
        date_str = datetime.now().strftime('%Y-%m-%d')  # Use scrape date or message date
        json_dir = f'data/raw/telegram_messages/{date_str}'
        os.makedirs(json_dir, exist_ok=True)
        json_path = f'{json_dir}/{channel_name}.json'
        with open(json_path, 'w') as f:
            json.dump(messages, f, indent=4)
        
        logging.info(f'Scraped {len(messages)} messages from {channel_name}. Saved to {json_path}')
    except Exception as e:
        logging.error(f'Error scraping {channel_name}: {str(e)}')

async def main():
    client = TelegramClient('session', api_id, api_hash)
    await client.start(phone=phone)
    
    # Handle 2FA if needed
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        code = input('Enter the code: ')
        try:
            await client.sign_in(phone, code)
        except SessionPasswordNeededError:
            password = input('Enter password: ')
            await client.sign_in(password=password)
    
    for channel in channels:
        await scrape_channel(client, channel)
    
    await client.disconnect()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())