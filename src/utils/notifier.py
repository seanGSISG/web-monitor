import asyncio
from telegram import Bot
from ..config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from ..utils.logger import logger

class Notifier:
    def __init__(self):
        self.bot = Bot(TELEGRAM_TOKEN) if TELEGRAM_TOKEN else None

    async def send_notification(self, message):
        if not self.bot or not TELEGRAM_CHAT_ID:
            return
        
        try:
            await self.bot.send_message(
                chat_id=TELEGRAM_CHAT_ID,
                text=message
            )
        except Exception as e:
            logger.error(f"Failed to send notification: {str(e)}")

    def notify(self, message):
        if self.bot:
            asyncio.run(self.send_notification(message))
