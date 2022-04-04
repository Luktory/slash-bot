import interactions
from interactions import *
from interactions import CommandContext
from interactions import extension_command as command
from interactions.ext import wait_for
import json, random, asyncio, os, requests
from dotenv import load_dotenv
from googleapiclient.discovery import build
from utils.permission import Permissions, has_permission

load_dotenv()
scope = int(os.getenv("SCOPE"))
google_cloud = os.getenv("GOOGLE_CLOUD")
google_cse = os.getenv("GOOGLE_CSE")




class Fun(interactions.Extension):
	def __init__(self, bot):
		self.bot = bot
		wait_for.setup(bot, add_method=True)

	@command(
		name="coffee",
		description="Send an image of coffee",
		scope=scope
	)
	async def coffee(self, ctx: CommandContext):
		response = requests.get('https://coffee.alexflipnote.dev/random.json')
		data = response.json()
		file = data['file']
		response.close()
		image = interactions.EmbedImageStruct(url=file)._json
		embed = interactions.Embed(title="Coffee ☕", color=0xc4771d, image=image)
		await ctx.send(embeds=embed)
	

	@command(
		name="ship",
		description="Ship 2 users",
		scope=scope,
		options=[
			interactions.Option(
				type=interactions.OptionType.STRING,
				name="user1",
				description="User 1",
				required=False,
			),
			interactions.Option(
				type=interactions.OptionType.STRING,
				name="user2",
				description="User 2",
				required=False,
			),
		]
	)
	async def ship(self, ctx: CommandContext,
		user1: str = None,
		user2: str = None
	):
		shipnumber = int(random.randint(0, 100))
		guild = await ctx.get_guild()
		members_list = await guild.get_list_of_members(limit=1000)
		if not user1 and not user2:
			result = random.choice(members_list)
			user1 = ctx.author.user.username if ctx.author.nick is None else ctx.author.nick
			user2 = result.user.username if result.nick is None else result.nick
		if not user2 and user1:
			user_1 = user1
			user2 = user_1
			user1 = ctx.author.user.username if ctx.author.nick is None else ctx.author.nick
		if not user1 and user2:
			result = random.choice(members_list)
			user1 = result.user.username if result.nick is None else result.nick
		# Choose comment and heart emoji
		if 0 <= shipnumber <= 30:
			comment = "Really low! {}".format(random.choice(
				[
				'Friendzone.',
				'Just "friends".',
				'There is barely any love.',
				'I sense a small bit of love!',
				'Still in that friendzone ;(',
				'No, just no!',
				'But there is a small sense of romance from one person!'
				]
			))
			heart = ":broken_heart:"
		elif 31 <= shipnumber <= 70:
			comment = "Moderate! {}".format(random.choice(
				[
				'Fair enough!',
				'A small bit of love is in the air...',
				'I feel like there is some romance progressing!',
				'I am starting to feel some love!',
				'At least this is acceptable.',
				'...',
				'I sense a bit of potential!',
				'But it is very one-sided.'
				]
			))
			heart = ":mending_heart:"
		elif 71 <= shipnumber <= 90:
			comment = "Almost perfect! {}".format(random.choice(
				[
				'I definitely can see that love is in the air.',
				'I feel the love!',
				'There is a sign of a match!',
				'A few things can be imporved to make this a match made in heaven!',
				'I can definitely feel the love.',
				'This has a big potential.',
				'I can see the love is there! Somewhere...'
				]
			))
			heart = random.choice(
				[
				':revolving_hearts:',
				':heart_exclamation:',
				':heart_on_fire:',
				':heartbeat:'
				]
			)
		elif 90 < shipnumber <= 100:
			comment = "True love! {}".format(random.choice(
				[
				'It is a match!', 
				'There is a match made in heaven!',
				'It is definitely a match!',
				'Love is truely in the air!',
				'Love is most definitely in the air!'
				]
			))
			heart = random.choice(
				[
				':sparkling_heart:',
				':heart_decoration:',
				':hearts:',
				':two_hearts:',
				':heartpulse:'
				]
			)
		# Choose color
		if shipnumber <= 40:
			shipColor = 0xdd3939
		elif 41 < shipnumber < 80:
			shipColor = 0xff6600
		else:
			shipColor = 0x3be801
		name1 = user1[:len(user1) // 2]
		name2 = user2[len(user2) // 2:]
		field = [
			interactions.EmbedField(name=f"Result: {shipnumber}%", value=f"{comment}"),
		]
		embed = interactions.Embed(
			title=f"**{user1}**    {heart}    **{user2}**",
			color=shipColor,
			fields=field,
			timestamp = datetime.datetime.utcnow()
		)
		await ctx.send(embeds=embed)

	
	@command(
		name="roll",
		description="Roll a dice",
		scope=scope,
	)
	async def roll(self, ctx: CommandContext):
		dice = random.randint(1, 6)
		msg: CommandContext = await ctx.send("I am rolling the dice...")
		await asyncio.sleep(1.5)
		await msg.edit("The number is **{}**.".format(dice))
	

	@command(
		name="flip",
		description="Flip a coin",
		scope=scope,
	)
	async def flip(self, ctx: CommandContext):
		coin = random.choice(["heads", "tails"])
		msg: CommandContext = await ctx.send("I am flipping the coin...")
		await asyncio.sleep(1.5)
		await msg.edit("The coin landed on **{}**.".format(coin))
	

	@command(
		name="joke",
		description="Send a random joke",
		scope=scope,
	)
	async def joke(self, ctx: CommandContext):
		response = requests.get('https://some-random-api.ml/joke')
		data = response.json()
		response.close()
		embed = Embed(description=data['joke'], color=random.randint(0, 0xFFFFFF))
		await ctx.send(embeds=embed)


	@command(
		name="quote",
		description="Send a quote",
		scope=scope,
	)
	async def quote(self, ctx: CommandContext):
		response = requests.get('https://api.quotable.io/random')
		data = response.json()
		author = data['author']
		content = data['content']
		dateAdded = data['dateAdded']
		response.close()
		footer = interactions.EmbedFooter(text=f"Added on {dateAdded}")
		embed = interactions.Embed(title=f"From {author}", description=content, color=random.randint(0, 0xFFFFFF), footer=footer)
		await ctx.send(embeds=embed)
	

	@command(
		name="xkcd",
		description="Send a xkcd comic page",
		scope=scope,
		options=[
			interactions.Option(
				type=interactions.OptionType.INTEGER,
				name="page",
				description="The page you want to read (if any)",
				required=False,
			),
		]
	)
	async def xkcd(self, ctx: CommandContext,
		page: int = None
	):
		if page is None:
			response = requests.get('https://xkcd.com/info.0.json')
			data = response.json()
			newest = data['num']
			page = random.randint(1, newest)
			response.close()
		response = requests.get(f'https://xkcd.com/{page}/info.0.json')
		data = response.json()
		month = data['month']
		year = data['year']
		day = data['day']
		title = data['title']
		alt = data['alt']
		img = data['img']
		response.close()
		footer = interactions.EmbedFooter(text=f"Page {page}/{newest} • Created on {year}-{month}-{day}")
		image = interactions.EmbedImageStruct(url=img)._json
		author = interactions.EmbedAuthor(name=f"{title}", url=f"https://xkcd.com/{page}/", icon_url=f"https://camo.githubusercontent.com/8bd4217be107c9c190ef649b3d1550841f8b45c32fc0b71aa851b9107d70cdea/68747470733a2f2f6173736574732e7365727661746f6d2e636f6d2f786b63642d626f742f62616e6e6572332e706e67")._json
		embed = interactions.Embed(description=alt, color=random.randint(0, 0xFFFFFF), footer=footer, image=image, author=author)
		await ctx.send(embeds=embed)


	@command(
		name="hornycard",
		description="Send a hornycard",
		scope=scope,
		options=[
			interactions.Option(
				type=interactions.OptionType.USER,
				name="user",
				description="Targeted user",
				required=False
			)
		]
	)
	async def hornycard(self, ctx: CommandContext,
		user: interactions.User = None
	):
		if not user:
			user = ctx.author
		else:
			user = user
		guild = interactions.Guild(**await self.bot._http.get_guild(ctx.guild_id), _client=self.bot._http)
		bot = await guild.get_member(member_id=self.bot.me.id)
		role = await guild.get_role(role_id=bot.roles[0])
		bot_perm = role.permissions
		
		if not (
			has_permission(int(bot_perm), Permissions.EMBED_LINKS) or
			has_permission(int(bot_perm), Permissions.ADMINISTRATOR)
		):
			return
		else:
			response = 'https://some-random-api.ml/canvas/horny?avatar={}'.format(user.avatar_url)
			await ctx.send(f"{response}")


	@command(
		name="simpcard",
		description="Send a simpcard",
		scope=scope,
	)
		
		




	@command(
		name="img",
		description="Search for images using Google Images",
		scope=scope,
		options=[
			interactions.Option(
				type=interactions.OptionType.STRING,
				name="query",
				description="Query to search for",
				required=True
			)
		]
	)
	async def img(self, ctx: CommandContext,
		query: str
	):
		# Get the image and the number of results
		ran = int(0)
		resource = build("customsearch", "v1", developerKey=google_cloud).cse()
		result = resource.list(
			q=f"{query}", cx=google_cse, searchType="image"
		).execute()
		image_link = result["items"][ran]["link"]
		title = result["items"][ran]["title"]
		displayLink = result["items"][ran]["displayLink"]
		contextLink = result["items"][ran]["image"]["contextLink"]

		embed = Embed(title=f"Image for: {query}", color=0x000000)
		embed.set_footer(text=f"Google Search • Page {ran}/9", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png")
		embed.add_field(name=f"**{displayLink}**", value=f"[{title}]({contextLink})", inline=False)
		embed.set_image(url=image_link)
		buttons = [
			interactions.ActionRow(
				components=[
					interactions.Button(
						style=interactions.ButtonStyle.PRIMARY,
						label="◄",
						custom_id="previous",
					),
					interactions.Button(
						style=interactions.ButtonStyle.PRIMARY,
						label="►",
						custom_id="next"
					),
				]
			)
		]
		msg: CommandContext = await ctx.send(embeds=embed, components=buttons)
		while True:
			try:
				res = await self.bot.wait_for_component(components=buttons, messages = int(msg.id), timeout = 8)
				if res.custom_id == "next":
					ran += 1
					if ran < 9:
						ran = ran
					image_link = result["items"][ran]["link"]
					title = result["items"][ran]["title"]
					displayLink = result["items"][ran]["displayLink"]
					contextLink = result["items"][ran]["image"]["contextLink"]

					embed = interactions.Embed(title=f"Image for: {query}", color=0x000000)
					embed.set_footer(text=f"Google Search • Page {ran}/9", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png")
					embed.add_field(name=f"**{displayLink}**", value=f"[{title}]({contextLink})", inline=False)
					embed.set_image(url=image_link)
					await res.edit(embeds=embed)
				elif res.custom_id == "previous":
					ran -= 1
					if ran < 0:
						ran = 0
					image_link = result["items"][ran]["link"]
					title = result["items"][ran]["title"]
					displayLink = result["items"][ran]["displayLink"]
					contextLink = result["items"][ran]["image"]["contextLink"]

					embed = interactions.Embed(title=f"Image for: {query}", color=0x000000)
					embed.set_footer(text=f"Google Search • Page {ran}/9", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2048px-Google_%22G%22_Logo.svg.png")
					embed.add_field(name=f"**{displayLink}**", value=f"[{title}]({contextLink})", inline=False)
					embed.set_image(url=image_link)
					await res.edit(embeds=embed)
			except asyncio.TimeoutError:
				await msg.edit(components=[])
				break











def setup(bot):
	Fun(bot)