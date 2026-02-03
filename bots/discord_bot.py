import os

import discord
import httpx

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    if message.content.startswith("!support"):
        issue = message.content.replace("!support", "").strip()
        if not issue:
            await message.channel.send("Please describe your issue after !support.")
            return
        async with httpx.AsyncClient() as client_http:
            response = await client_http.post(
                f"{BACKEND_URL}/chat",
                json={"user_id": str(message.author.id), "message": issue},
                timeout=30,
            )
        data = response.json()
        await message.channel.send(data.get("response", "Thanks!"))


def main() -> None:
    if not DISCORD_BOT_TOKEN:
        raise ValueError("DISCORD_BOT_TOKEN is not set")
    client.run(DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    main()
