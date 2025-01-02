import discord
from discord.ext import commands, tasks
from datetime import datetime
import random
from dotenv import load_dotenv
import os

# Load environment variables (to access the bot token securely)
load_dotenv()
token = os.getenv('TOKEN')

# Set up the bot with intents
intents = discord.Intents.default()  # Use default intents
intents.message_content = True  # Add this if you need to read message content
bot = commands.Bot(command_prefix="!", intents=intents)

# Countdown target date
TARGET_DATE = datetime(2025, 1, 1, 0, 0, 0)

# Background task for periodic countdown updates
@tasks.loop(minutes=30)  # Run every 30 minutes
async def countdown_loop():
    now = datetime.now()
    remaining = TARGET_DATE - now
    channel = bot.get_channel(901151361863942147)  # Replace with the actual channel ID
    if remaining.total_seconds() <= 0:
        await channel.send("🎆 Happy New Year 2025! 🎆")
        await channel.send("The countdown is complete!")
        countdown_loop.stop()  # Stop the loop after the countdown is complete
    else:
        days, hours, minutes, seconds = (
            remaining.days,
            remaining.seconds // 3600,
            (remaining.seconds % 3600) // 60,
            remaining.seconds % 60,
        )
        await channel.send(f"⏳ Time left until 2025: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds!")

@bot.event
async def on_ready():
    print(f"🎉 {bot.user} is online and ready!")
    countdown_loop.start()  # Start the countdown updates when the bot is ready

@bot.event
async def on_ready():
    print(f"🎉 {bot.user} is online and ready!")
    countdown_loop.start()  # Start the countdown updates when the bot is ready
    
    # Welcome message
    channel = bot.get_channel(901151361863942147)  # Replace with the actual channel ID
    welcome_message = """
    **Welcome to the Countdown Bot! 🎉**
    I'm here to keep you entertained and informed. Here's a list of things I can do:
    1. **!countdown**  
       ⏳ Check the time left until New Year 2025!
    
    2. **!trivia**  
       🧠 Test your knowledge with a trivia question! Answer correctly for a reward.
    
    3. **!motivate**  
       🌟 Feeling down? I’ve got motivational quotes to inspire you!
    
    4. **!joke**  
       😄 Need a laugh? I’ll tell you a random joke!
    
    Feel free to use any of these commands anytime. I’m here to make your experience fun and engaging. Let’s make 2025 awesome together! 🎆
    """
    await channel.send(welcome_message)

@bot.event
async def on_guild_join(guild):
    # Get the first text channel where the bot can send messages
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send("Countdown starting soon!")
            countdown_loop.start()  # Start the countdown loop when joining a guild
            break

# Countdown Command
@bot.command()
async def countdown(ctx):
    now = datetime.now()
    remaining = TARGET_DATE - now
    if remaining.total_seconds() <= 0:
        await ctx.send("🎆 Happy New Year 2025! 🎆")
    else:
        days, hours, minutes, seconds = (
            remaining.days,
            remaining.seconds // 3600,
            (remaining.seconds % 3600) // 60,
            remaining.seconds % 60,
        )
        await ctx.send(f"⏳ Time left until 2025: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds!")

# Trivia Command
@bot.command()
async def trivia(ctx):
    questions = {
        "What is the smallest planet in the solar system?": "Mercury",
        "How many continents are there on Earth?": "7",
        "What is the capital of France?": "Paris",
    }
    question, answer = random.choice(list(questions.items()))
    await ctx.send(f"🧠 Trivia Time! {question}")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", timeout=15.0, check=check)
        if msg.content.lower() == answer.lower():
            await ctx.send("✅ Correct!")
        else:
            await ctx.send(f"❌ Wrong! The answer was {answer}.")
    except:
        await ctx.send("⏳ Time's up!")

# Motivational Message Command
@bot.command()
async def motivate(ctx):
    messages = [
        "🌟 Keep going, you're doing amazing!",
        "💪 Believe in yourself!",
        "🚀 You're closer to your dreams every day!",
    ]
    await ctx.send(random.choice(messages))

# Jokes Command
@bot.command()  # Added @bot.command() decorator
async def joke(ctx):
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the math book look sad? It had too many problems.",
        "Why can't your nose be 12 inches long? Because then it would be a foot!",
    ]
    await ctx.send(random.choice(jokes))

# Start the bot
bot.run(token)



#Personalized Goals:
#!set_goal <your goal>: Sets a personalized goal for the user.
#!view_goal: Displays the user's current goal.
#Mini-Games:
#!guess_number: A guessing game where the user tries to guess a random number between 1 and 100.
