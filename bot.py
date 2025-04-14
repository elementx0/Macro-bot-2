import os
import discord
import openai
import logging
from discord.ext import commands

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('discord_bot')

# Directly set the environment variables
os.environ["DISCORD_TOKEN"] = "MTM1OTg2MjQxMjc2OTIzMDg2OA.G88NL_.sS8su6sQpTTx8x9RUiDf4GxBq4PsvjJ2CMG8ss"
os.environ["OPENAI_API_KEY"] = "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"
os.environ["DISCORD_CHANNEL_ID"] = "1359901161250881746"

# Set up the Discord bot with necessary intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Configure OpenAI
openai.api_key = "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"

# Set channel ID directly
CHANNEL_ID = 1359901161250881746

@bot.event
async def on_ready():
    """Log when the bot is ready."""
    logger.info(f"Logged in as {bot.user} (ID: {bot.user.id})")
    logger.info(f"Bot is configured to respond in channel ID: {CHANNEL_ID}")

@bot.event
async def on_message(message):
    """Handle incoming messages."""
    # Ignore messages from bots to prevent loops
    if message.author.bot:
        return
    
    # Only respond in the designated channel
    if message.channel.id != CHANNEL_ID:
        return
    
    logger.info(f"Received message from {message.author}: {message.content}")
    
    try:
        # Show typing indicator while generating response
        async with message.channel.typing():
            # Call OpenAI API
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a friendly, casual assistant in a Discord server. Keep responses concise and conversational."},
                    {"role": "user", "content": message.content}
                ],
                max_tokens=500
            )
            
            # Get the response text
            bot_response = response.choices[0].message.content
            
            # Send the response
            await message.reply(bot_response)
            logger.info(f"Sent response to {message.author}")
    
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        await message.reply("Sorry, I'm having trouble processing that message right now.")

# Run the bot
if __name__ == "__main__":
    bot.run("MTM1OTg2MjQxMjc2OTIzMDg2OA.G88NL_.sS8su6sQpTTx8x9RUiDf4GxBq4PsvjJ2CMG8ss")
