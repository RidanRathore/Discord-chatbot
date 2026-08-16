import discord
import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Only respond if Nova is actually mentioned
    if bot.user not in message.mentions:
        return

    # Strip the @Nova mention out of the message so it's not sent to the model
    prompt = message.content.replace(f"<@{bot.user.id}>", "").strip()

    if not prompt:
        await message.channel.send("Yes? What do you need?")
        return

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        print(response.choices[0].message.content[:1000])

        await message.channel.send(
            response.choices[0].message.content[:2000]
        )
    except Exception as e:
        print("An error occurred:", str(e))
        print("check your connection and try again.")

bot.run(os.environ.get("DISCORD_TOKEN"))