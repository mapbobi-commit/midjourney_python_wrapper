import discord
import requests
import yaml


with open("config.yaml", mode="r") as fp:
    config = yaml.safe_load(fp)

bot = discord.Client(intents=discord.Intents.all())


def PassPromptToSelfBot(prompt: str):
    channel_id = config["id"]["channel"]
    server_id = config["id"]["server"]
    midjourney_token = config["token"]["midjourney"]

    command_instructions = {
        "type": 2,
        "application_id": "936929561302675456",
        "guild_id": server_id,
        "channel_id": channel_id,
        "session_id": "2fb980f65e5c9a77c96ca01f2c242cf6",
        "data": {
            "version": "1077969938624553050",
            "id": "938956540159881230",
            "name": "imagine",
            "type": 1,
            "options": [{"type": 3, "name": "prompt", "value": prompt}],
            "application_command": {
                "id": "938956540159881230",
                "application_id": "936929561302675456",
                "version": "1077969938624553050",
                "default_permission": True,
                "default_member_permissions": None,
                "type": 1,
                "nsfw": False,
                "name": "imagine",
                "description": "Create images with h",
                "dm_permission": True,
                "options": [
                    {
                        "type": 3,
                        "name": "prompt",
                        "description": "The prompt to imagine",
                        "required": True,
                    }
                ],
            },
            "attachments": [],
        },
    }

    header = {"authorization": midjourney_token}
    response = requests.post(
        "https://discord.com/api/v9/interactions",
        json=command_instructions,
        headers=header,
    )
    return response


def url_to_image_byte(url):
    response = requests.get(url)
    global image
    image = response.content


def make_midjourney_image_request(prompt):
    discord_token = config["token"]["discord"]

    @bot.event
    async def on_ready():
        PassPromptToSelfBot(prompt)

    @bot.event
    async def on_message(message):
        if len(message.attachments) != 0:
            if (
                message.attachments[0]
                .filename.lower()
                .endswith((".png", ".jpg", ".jpeg", ".gif"))
            ):
                url_to_image_byte(message.attachments[0].url)
                await bot.close()

    bot.run(discord_token)
    return image
