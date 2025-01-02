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
@tasks.loop(minutes=1)  # Run every 30 minutes
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

# In-memory storage for goals and to-do lists
user_goals = {}
user_todos = {}

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
    Welcome to the Countdown Bot! 🎉
    I’m here to make your experience fun, productive, and entertaining. Here’s what I can do for you:

    !countdown
    ⏳ Check the time left until New Year 2025!

    !setgoal <your goal>
    🎯 Set a personal goal to keep track of your ambitions.

    !viewgoal
    👀 View your current goal.

    !addtask <your task>
    📝 Add a task to your personal to-do list.

    !viewtasks
    📋 View all tasks in your to-do list.

    !donetask <task number>
    ✅ Mark a task as done.

    !trivia
    🧠 Challenge yourself with a trivia question. Answer correctly for a reward!

    !motivate
    🌟 Get inspired with a motivational quote.

    !joke
    😄 Lighten the mood with a random joke.

    !rps <rock/paper/scissors>
    🪨📄✂️ Play Rock-Paper-Scissors with me!

    Let’s make this countdown to 2025 exciting and meaningful. Use these commands anytime you need assistance, motivation, or just a bit of fun! 🎆
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

### Goal-Setting Feature ###
@bot.command()
async def setgoal(ctx, *, goal: str = None):
    """Set a personal goal for the user, with validation."""
    if goal is None or len(goal.strip()) == 0:
        await ctx.send("❌ Invalid input! Please specify a valid goal. Example: !setgoal Learn Python")
        return

    user_goals[ctx.author.id] = goal.strip()
    await ctx.send(f"🎯 Goal set successfully! Your goal is: **{goal.strip()}**")


@bot.command()
async def viewgoal(ctx):
    """View the user's current goal."""
    goal = user_goals.get(ctx.author.id, None)
    if goal:
        await ctx.send(f"🎯 Your current goal is: **{goal}**")
    else:
        await ctx.send("❌ You haven't set a goal yet! Use !setgoal [your goal] to set one.")

### To-Do List Feature ###
@bot.command()
async def addtask(ctx, *, task: str = None):
    """Add a task to the user's to-do list."""
    if task is None or len(task.strip()) == 0:
        await ctx.send("❌ Invalid input! Please specify a valid task. Example: !addtask Complete homework")
        return

    if ctx.author.id not in user_todos:
        user_todos[ctx.author.id] = []

    user_todos[ctx.author.id].append(task.strip())
    await ctx.send(f"✅ Task added successfully! Your task is: **{task.strip()}**")


@bot.command()
async def viewtasks(ctx):
    """View all tasks in the user's to-do list."""
    tasks = user_todos.get(ctx.author.id, [])
    if tasks:
        task_list = "\n".join([f"{i+1}. {task}" for i, task in enumerate(tasks)])
        await ctx.send(f"📝 Your To-Do List:\n{task_list}")
    else:
        await ctx.send("❌ Your to-do list is empty! Use !addtask [task] to add tasks.")

@bot.command()
async def donetask(ctx, task_index: int = None):
    """Mark a task as done."""
    if ctx.author.id not in user_todos or len(user_todos[ctx.author.id]) == 0:
        await ctx.send("❌ You have no tasks in your to-do list. Add one using !addtask.")
        return

    if task_index is None:
        await ctx.send("❌ Invalid input! Please specify the task number to mark as done. Example: !donetask 1")
        return

    if not (1 <= task_index <= len(user_todos[ctx.author.id])):
        await ctx.send(f"⚠️ Invalid task number! Please enter a number between 1 and {len(user_todos[ctx.author.id])}.")
        return

    completed_task = user_todos[ctx.author.id].pop(task_index - 1)
    await ctx.send(f"✅ Task marked as done: **{completed_task}**")

# Trivia Command
@bot.command()
async def trivia(ctx):
    questions = {
    "What is the smallest planet in the solar system?": "Mercury",
    "What is the chemical symbol for gold?": "Au",
    "Who wrote the play 'Romeo and Juliet'?": "William Shakespeare",
    "Which planet is known as the Red Planet?": "Mars",
    "Who developed the theory of general relativity?": "Albert Einstein",
    "Which is the longest river in the world?": "Nile",
    "In which year did the Titanic sink?": "1912",
    "Who was the first woman to win a Nobel Prize?": "Marie Curie",
    "What is the hardest natural substance on Earth?": "Diamond",
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
    "🔥 Don't stop now, you're on fire!",
    "💡 Every step you take brings you closer to your goal!",
    "🌱 Small progress is still progress!",
    "🎯 Stay focused and keep pushing forward!",
    "💖 You are capable of achieving greatness!",
    "🌈 Your hard work will pay off soon!",
    "🦸‍♂️ You're stronger than you think!"
]
    await ctx.send(random.choice(messages))

# Jokes Command
@bot.command()  # Added @bot.command() decorator
async def joke(ctx):
    jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "Why did the math book look sad? It had too many problems.",
    "Why can't your nose be 12 inches long? Because then it would be a foot!",
    "What do you call fake spaghetti? An impasta.",
    "What did the left eye say to the right eye? Between you and me, something smells.",
    "Why did the scarecrow win an award? Because he was outstanding in his field.",
]
    await ctx.send(random.choice(jokes))

@bot.command()
async def rps(ctx, user_choice: str = None):
    # Check if the user provided a valid choice
    if user_choice is None:
        await ctx.send("❌ You need to choose! Use !rps <rock/paper/scissors> to play.")
        return

    user_choice = user_choice.lower()
    choices = ["rock", "paper", "scissors"]
    
    if user_choice not in choices:
        await ctx.send("❌ Invalid choice! Please choose rock, paper, or scissors.")
        return

    # Bot's choice
    bot_choice = random.choice(choices)

    # Determine the winner
    if user_choice == bot_choice:
        result = "🤝 It's a tie!"
    elif (user_choice == "rock" and bot_choice == "scissors") or \
         (user_choice == "paper" and bot_choice == "rock") or \
         (user_choice == "scissors" and bot_choice == "paper"):
        result = "🎉 You win!"
    else:
        result = "💻 I win!"

    # Send the result
    await ctx.send(f"🪨📄✂️ **Rock-Paper-Scissors**\n"
                   f"Your choice: {user_choice.capitalize()}\n"
                   f"My choice: {bot_choice.capitalize()}\n"
                   f"**{result}**")


# Start the bot
bot.run(token)