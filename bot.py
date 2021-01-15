import discord as disc
import sqlite3 as sql
from logic import *
import time, asyncio

my_id = 408320177386684416

def read_token():
	with open("token.txt", "r") as f:
		lines = f.readlines()
		return lines[0].strip()

token = read_token()
prefix = "sb+"

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

global database
database = sql.connect("bot.db")

def get_registered_guilds():
	c = database.cursor()
	c.execute("""
		CREATE TABLE IF NOT EXISTS guild_servers(
		guildID INTEGER PRIMARY KEY,
		guildName TEXT,
		discordID INTEGER);
		""")

	c.execute("""
		SELECT * FROM guild_servers
		""")

	results = c.fetchall()
	
	global registered_guilds
	registered_guilds = {}

	for g in results:
		registered_guilds[g[2]] = g[1]

	return registered_guilds

def register_guild(guild_name, server_id):
	c = database.cursor()
	c.execute("""
		INSERT INTO guild_servers
		VALUES (NULL, ?, ?)
		""", (guild_name.lower(), server_id))

	database.commit()
	logChange("guild_servers", f"Guild {guild_name} has been registered with a server ID of {server_id}")
	logMessage("register_guild")

get_registered_guilds()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

client = disc.Client()


# async def run_daily_stats():
# 	await client.wait_until_ready()

# 	while not client.is_closed():
# 		one_day = 86400 # 86400 = 60*60*24, number of seconds in 24 hours.
# 		try:
# 			global database
# 			c = database.cursor()
# 			c.execute("SELECT name FROM sqlite_master WHERE type='table'")
# 			guilds = c.fetchall()[0]

# 			for g in guilds:
# 				guild = Guild(guilds[0])
# 				guild.cursor.execute("""
# 					SELECT * FROM {name}
# 					""".format(name=guild.tbName))
# 				for member in guild.cursor.fetchall():
# 					guild.update_record(member[1])

# 			logMessage("run_daily_stats", "Guild statistics have been updated.")

# 			await asyncio.sleep(one_day)

# 		except Exception as e:
# 			logError(e)
# 			await asyncio.sleep(one_day)


@client.event
async def on_member_update(before, after):
	new = after.nick
	if new:
		if n.lower() in ["SweatiestBoi", "Luna"] & after.id != 0:
			if before.nick:
				await after.edit(nick=before.nick)
				logMessage('nick_blocker', f"Member {before.nick} attempted to change their nick to {after.nick}.")
			else:
				await after.edit(nick=after.name)
				logMessage('nick_blocker', f"Member {after.name} attempted to change their nuck to {after.nick}.")



@client.event
async def on_message(message):
	if message.author.name == "SweatiestBoi": return False

	server = message.guild.id
	global registered_guilds, my_id


	####################
	## GUILD COMMANDS ##
	####################

	## DAILY STATS command.
	if "daily-stats" in str(message.channel):
		if message.content == prefix+"daily-stats":
			if server in registered_guilds:
				guild_name = registered_guilds[server]
			else:
				await message.channel.send("You have not registered as a guild server! Please use the 'register-guild' command to do so, then try again.")
				return
			description = """
			Stats for every member of the {guild} guild!
			Date: {date}.
			""".format(guild=guild_name ,date=datetime.now().strftime("%d %B, %y"))

			c = database.cursor()
			c.execute("""
				SELECT * FROM {guild}
				""".format(guild=guild_name))
			results = c.fetchall()

			embed = disc.Embed(title="Guild Statistics", description=description)

			i = 1
			for record in results:
				value = f"""
				Total Wins: {record[2]} (+{record[3]})
				Win Rate: {record[4]}
				KDR: {record[5]}
				Bedwars Wins: {record[6]}
				Skywars Wins: {record[7]}
				The Bridge Wins: {record[8]}
				"""
				if i // 2 == 0: inline=True
				else: inline=False
				embed.add_field(name=record[1], value=value, inline=inline)

			mvp = Guild(guild_name).mvp()
			value = f"- {mvp[0]}, with {mvp[1]} wins!"
			embed.add_field(name='MVP of the day:', value=value, inline=False)

			await message.channel.send(content=None, embed=embed)

			logCommand(message.author.name, "daily-stats")



	## HELP command
	elif message.content == prefix+"help":
		# the first embed. Title and description of menu.
		embed1 = disc.Embed(title="Help", description=f"A list of all available commands and their permissions. The server-wide prefix is: '{prefix}'", color=0xd60000)
		file = disc.File("icon.png", filename="image.png")
		embed1.set_author(name="SweatiestBoi", url="https://www.github.com", icon_url="attachment://image.png")
		
		# the second embed. Guild commands menu.
		embed2 = disc.Embed(title="Guild Commands", description="Commands to do with guild management. **NOTE**: Guild commands *will not work* until the server has been registered.", color=0x884444)
		embed2.add_field(name="'daily-stats'", value=" Admins only. Displays the statistics of every member in the guild, as well as the MVP (player with most wins that day). **NOTE**: Only works inside of channels that have 'daily-stats' within their name.", inline=False)
		embed2.add_field(name="'add-member <:ign>'", value="Admins only. Adds a member to the guild.", inline=False)
		embed2.add_field(name="'remove-member <:ign>'", value="Admins only. remvoes a member from the guild.", inline=False)
		embed2.add_field(name="'view-members'", value="Lists the guild members.", inline=False)
		embed2.set_footer(text="Paramaters: <:ign> - Target username.")

		# the third embed. Player commands menu.
		embed3 = disc.Embed(title="Player Commands", description="Commands for indiviual users.", color=0x2f4265)
		embed3.add_field(name="'stats <:ign>'", value="Displays stats for the specified player. \n**Stats shown**: -*Kills* -*Deaths* -*KDR* -*Total wins* -*Win Rate* -*Bedwars wins* -*Skywars wins* -*The Bridge wins* -*Duels wins*", inline=False)
		embed3.add_field(name="'stat <:ign> <:stat1> <:stat2:optional>'", value="Displays the specified statistic for the specified player. \nValid arguments are:\n**:stat1** -*kills* -*deaths* -*kdr* -*wins* -*friends list* -*warnings* -*wins distribution (you can use stat2 here)* \n**:stat2** -*bedwars* -*skywars* -*the bridge* -*duels*", inline=False)
		embed3.add_field(name="'online <:ign>'", value="Displays whether the targeted player is currently online.", inline=False)

		# the fourth embed. General commands menu.
		embed4 = disc.Embed(title="General Commands", description="The various miscellaneous commands.", color=0x46ce81)
		embed4.add_field(name="'help'", value="Displays a menu showing the commands the bot can perform.", inline=False)
		embed4.add_field(name="'heart'", value="<3", inline=False)
		embed4.add_field(name="'fun-fact'", value="Displays a random fun fact about Minecraft.", inline=False)

		# the fifth embed. Admin commands menu.
		embed5 = disc.Embed(title="Admin Commands", description="Server management commands. Requires administrator permissions, or a role marked as 'admin' within the bot.", color=0x5f0c97)
		embed5.add_field(name="'register-server <:guild>'", value="Sends an application to register the server as belonging to the specified guild. If verified, guild commands will then be enabled for the server.", inline=False)
		embed5.add_field(name="'prefix <:prefix>'", value="Changes the server-wide prefix.", inline=False)
		embed5.add_field(name="'admin-role <:role>'", value="Makes the specified role an admin role, and gives them access to admin-only commands. *Does not apply to roles with server-wide administrator permissions.*", inline=False)
		embed5.add_field(name="'block <:user>'", value="Blocks the specified user from using any SB bot commands in this server.", inline=False)
		embed5.add_field(name="'unblock <:user>'", value="Unblocks the specified user from using any SB bot commands in this server.", inline=False)


		# sends embeds to discord server.
		await message.channel.send(content=None, file=file, embed=embed1)
		await message.channel.send(content=None, embed=embed2)
		await message.channel.send(content=None, embed=embed3)
		await message.channel.send(content=None, embed=embed4)
		await message.channel.send(content=None, embed=embed5)

		logCommand(message.author.name, "help")



	####################
	## ADMIN COMMANDS ##
	####################


	elif message.content.startswith(prefix+"register-guild"):
		logCommand(message.author.name, "register-guild", message.content)

		x = message.content.replace(prefix+"register-guild", "")
		if server in registered_guilds:
			await message.channel.send(f"Error: the server is already registered as guild '{registered_guilds[server]}'.")
			# return False
		elif x == "":
			await message.channel.send("Error: paramater '<:guild>' missing.\nPlease try again.")
			return False

		description = f"Thank you for applying to register your server under the name {x}.\nA bot administrator will get back to you soon to verify the server as belonging to the guild."

		embed1 = disc.Embed(title="Register Server", description=description, color=0xd10000)
		await message.author.send(content=None, embed=embed1)

		embed2 = disc.Embed(title="Server Registration Application", description=f"A user has attempted to register their server as guild '{x}'.", color=0xd10000)
		value = f"""
		Server: {message.guild.name}, id={server}
		User: {message.author.name}, id={message.author.id}
		"""
		embed2.add_field(name="Details:", value=value)
		await message.author.send(content=None, embed=embed2)











	## Attributions command.
	elif message.content == prefix+"attributions":
		embed = disc.Embed(title="Attributions", description="Thanks to every person mentioned here, for either helping me or providing an asset free of charge!", color=0xd60000)
		embed.add_field(name="Bot Icon", value="Starry backdrop - Photo by Manouchehr Hejazi on Unsplash.")

		await message.channel.send(content=None, embed=embed)

	elif message.content == "dm-me":
		user = client.get_user(str(my_id))
		await message.channel.send(f"Sending message to {my_id}")
		await user.send(user)




# client.loop.create_task(run_daily_stats())

client.run(token)