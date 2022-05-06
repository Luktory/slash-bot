import interactions
from interactions import extension_listener as listener
import datetime, random, urllib.request


class Automod(interactions.Extension):
	def __init__(self, bot) -> None:
		super().__init__()
		self.bot = bot


	@listener(name="on_message_create")
	async def _message_create(self, message: interactions.Message):
		if message.guild_id == 738938246574374913 and message.guild_id is not None:
			message_content = message.content.lower()

			# If someone sends an invite link
			if "discord.gg/" in message_content or "discordapp.com/invite" in message_content or "discord.com/invite" in message_content:
				channel = await message.get_channel()
				await message.delete()
				await channel.send(f"{message.member.mention}, your message was deleted because it contained an unauthorized invite link.")
				return
			
			# If someone mentions @everyone or @here
			if "@everyone" in message_content or "@here" in message_content:
				channel = await message.get_channel()
				await message.delete()
				await channel.send(f"{message.member.mention}, please do not ping everyone.")
				return
			
			# If someone sends a Nitro scam link
			if "cdn.discordapp.com" in message_content:
				return
			else:
				with urllib.request.urlopen('https://raw.githubusercontent.com/Jimmy-Blue/discord-scam-links/articuno/list.txt') as f:
					html = f.read().decode('utf-8')
				for line in html.splitlines():
					if line in message_content:
						channel = await message.get_channel()
						await message.delete()
						await channel.send(f"{message.member.mention}, please do not send a scam link.")
						return






def setup(bot):
	Automod(bot)