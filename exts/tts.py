"""
This module is for TTS command.

(C) 2022 - Jimmy-Blue
"""

import io
import asyncio
import interactions
import aiohttp
import requests
from const import U_KEY, U_SECRET

def _get_audio(uuid: str):
    response = requests.get(url=f"https://api.uberduck.ai/speak-status?uuid={uuid}")
    json: dict = response.json()
    return json if json.get("path") else False

_voice_name_convert = {
    "sonic-jason-griffith": "Sonic the Hedgehog",
    "tails-colleen": "Tails",
    "amy-rose-cr": "Amy Rose",
    "knuckles": "Knuckles",
    "shadow-david-humphrey": "Shadow",
    "cosmo-the-seedrian": "Cosmo",
    "chris-thorndyke": "Chris Thorndyke",
    "donut-lord": "Tom Wachowski",
    "ash-ketchum": "Ash Ketchum",
    "professor-oak": "Professor Oak",
    "meowth": "Meowth"
}


class TTS(interactions.Extension):
    def __init__(self, bot: interactions.Client):
        self.bot: interactions.Client = bot

    @interactions.extension_command(
        name="tts",
        description="Send a TTS message with different voices (Powered by Uberduck)",
        options=[
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="text",
                description="Text to convert to speech",
                required=True,
            ),
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="voice",
                description="Voice to use",
                required=False,
                choices=[
                    interactions.Choice(name="Sonic", value="sonic-jason-griffith"),
                    interactions.Choice(name="Tails", value="tails-colleen"),
                    interactions.Choice(name="Amy", value="amy-rose-cr"),
                    interactions.Choice(name="Knuckles", value="knuckles"),
                    interactions.Choice(name="Shadow", value="shadow-david-humphrey"),
                    interactions.Choice(name="Cosmo the Seedrian", value="cosmo-the-seedrian"),
                    interactions.Choice(name="Chris Thorndyke", value="chris-thorndyke"),
                    interactions.Choice(name="Tom Wachowski", value="donut-lord"),
                    interactions.Choice(name="Ash Ketchum", value="ash-ketchum"),
                    interactions.Choice(name="Professor Oak", value="professor-oak"),
                    interactions.Choice(name="Meowth", value="meowth")
                ],
            ),
        ],
    )
    async def _tts(
        self, ctx: interactions.CommandContext, text: str, voice: str = None
    ):
        check_voice = [
            "sonic-jason-griffith",
            "tails-colleen",
            "amy-rose-cr",
            "knuckles",
            "shadow-david-humphrey",
            "cosmo-the-seedrian",
            "chris-thorndyke",
            "donut-lord",
            "ash-ketchum",
            "professor-oak",
            "meowth"
        ]
        if not voice:
            voice = "tails-colleen"
        elif voice and voice not in check_voice:
            return await ctx.send("Invalid voice. Please try again.", ephemeral=True)
        await ctx.defer()

        url = "https://api.uberduck.ai/speak"
        json = {"speech": text, "voice": voice.lower()}
        auth = aiohttp.BasicAuth(U_KEY, U_SECRET)

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=json, auth=auth) as response:
                    if response.status == 200:
                        uuid = (await response.json())["uuid"]
                        _json = None
                        while True:
                            failed_time = 0
                            audio = _get_audio(uuid)
                            if failed_time < 10:
                                if audio is not False:
                                    _json = audio
                                    break
                                failed_time += 1
                                await asyncio.sleep(1)
                                continue
                            else:
                                raise Exception("Failed to get audio")

                        async with session.get(_json["path"]) as resp:
                            audio = interactions.File(
                                filename="audio.wav",
                                fp=io.BytesIO(await resp.read()),
                            )
                            await ctx.send(content=f"Message: {text}\nVoice: {_voice_name_convert[voice]}", files=audio)

            await session.close()

        except Exception:
            await ctx.send("Aww! Snap.", ephemeral=True)


def setup(bot):
    TTS(bot)
