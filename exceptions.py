from datetime import datetime, timedelta
import json

## script to handle all errors for the programs.
class UsernameError(Exception):
	def __init__(self, ign, message="Username does not exist."):
		self.ign = ign
		self.message = message
		super().__init__(self.message)

	def __str__(self):
		x = f"{self.ign} --> {self.message}"
		logError(f"UsernameError: {x}")
		return x

class GuildError(Exception):
	def __init__(self, guild, message="Guild does not exist"):
		self.guild = guild
		self.message = message
		super().__init__(self.message)

	def __str__(self):
		x = f"{self.guild} --> {self.message}"
		logError(f"GuildError: {x}")
		return x

class MemberError(Exception):
	def __init__(self, ign, message="Member not in guild."):
		self.ign = ign
		self.message = message
		super().__init__(self.message)

	def __str__(self):
		x = f"{self.ign} --> {self.message}"
		logError(f"MemberError: {x}")
		return x

class ConnectionError(Exception):
	def __init__(self, code, message="Unable to connect with NetherGames servers."):
		self.code = code
		self.message = message
		self.time = datetime.now().strftime("%d %b %y, %H:%M:%S")
		super().__init__(self.message)

	def __str__(self):
		x = f"{self.time} - Status Code: {self.code} --> {self.message}"
		logError(f"ConnectionError: {x}")
		return x

class StatsError(Exception):
	def __init__(self, stat, message="Invalid dictionary item."):
		self.stat = stat
		self.message = message
		super().__init__(self.message)

	def __str__(self):
		x = f"{self.stat} --> {self.message}"
		logError(f"StatsError: {x}")
		return x


class CreationError(Exception):
	def __init__(self, name, message="Tournament settings have not been finalised."):
		self.name = name
		self.message = message
		super().__init__(self.message)

	def __str__(self):
		x = f"{self.name} --> {self.message}"
		logError(f"CreationError: {x}")
		return x



## code to handle writing stuff to a log file.
def logError(message):
	with open("log.txt", "a") as f:
		f.write(f" > {message}\n")
		f.close()
		return True

def logChange(table, update):
	t = datetime.now().strftime("%d %b %y, %H:%M:%S")
	with open("log.txt", "a") as f:
		f.write(f" > {t} - Database modified. {table} --> {update}\n")
		f.close()
		return True

def logMessage(command, message=""):
	t = datetime.now().strftime("%d %b %y, %H:%M:%S")
	with open("log.txt", "a") as f:
		f.write(f" > {t} - Command '{command}' run. {message}\n")
		f.close()
		return True

def logCommand(user, command, message=""):
	t=datetime.now().strftime("%d %b %y, %H:%M:%S")
	with open("log.txt", "a") as f:
		f.write(f" > {t} - User {user} used command {command}.\n > '{message}'\n")
		f.close()
		return True


## code to handle writing stats to a cache.
def cache_stats(item):
	now = datetime.now()
	t = datetime.timestamp(now)
	
	with open("cache.txt", "r+") as f:
		file = f.readlines()
		if len(file) < 15:
			f.write(f"{t};;{json.dumps(item)}\n")
			f.close()
			return True

		f.close()

	with open("cache.txt", "w") as f:
		file.append(f"{t};;{json.dumps(item)}\n")
		for line in file[1:]: f.write(line)
		f.close()
		return True


## code to handle reading stats from the cache. needs updating to match format of stats, but for now it'll do
def read_cache(item):
	now = datetime.now()
	t = datetime.timestamp(now)

	cache = []

	with open("cache.txt", "r") as f:
		file = f.readlines()
		for i in file:
			cache.append(i.split(";;"))

		f.close()

	for i in cache:
		if f'"name": "{item.lower()}"' in i[1]:
			if float(i[0]) >= t - 1800: return json.loads(i[1].strip()) # 1800 = 30 * 60. No. of seconds in 30 minutes

	return False


