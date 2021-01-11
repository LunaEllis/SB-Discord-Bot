from exceptions import *
import sqlite3 as sql
import requests

api_key = "http://apiv2.nethergames.org"

def test_connection():
	## Tries to pull NG player count and server status
	response = requests.get(api_key + "/servers/stats?total=true")

	## If successful connection, prints response to console and returns True
	if str(response.status_code).startswith("2"):
		t = datetime.now().strftime("%d %b %y, %H:%M:%S")
		logError(f"Successfully connected to NetherGames servers - {t}")
		return True

	## Otherwise, raises an exception which is printed to console, and then returns False
	else: raise ConnectionError(response.status_code)

## Pulls player's stats from NG servers
def stats(ign):
	try: # If successful, returns player's stats as a dictionary.
		response = requests.get(api_key + f"/players/{ign}/stats")
		if response.status_code != 200: raise UsernameError(ign)
		return response.json()
	except UsernameError as error: # Otherwise, raises a UsernameError
		print(error) # Should prolly change to outputting to log, this way it'll be easier to do the program bit later
		return False

# # Pulls guild's stats from NG servers
# # CURRENTLY UNAVAILABLE
# def g_stats(guild):
# 	try:
# 		response = requests.get(api_key + f"/guilds/{guild}/stats")
# 		if response.status_code != 200: raise GuildError(guild)
# 		return response.json()
# 	except GuildError as error:
# 		print(error)
# 		print(response.status_code)
# 		return False


#_________________________________________________________________________________________________________________________________________________________________



class Player:
	def __init__(self, username):
		test_connection()

		self.username = username
		self.overall_stats = stats(self.username)

	def check(self):
		return self.overall_stats == False

	def get_all(self):
		return self.overall_stats

	def get_statistic(self, stat, stat2=""):
		if self.check(): return False
		try:
			if not (stat in self.overall_stats): raise StatsError(stat) # guard clause for efficiency. if 'stat' is invalid, error thrown and other code not run

			if stat2 != "":
				if not (stat2 in self.overall_stats[stat]): raise StatsError(f"[{stat}][->{stat2}<-]")
				return self.overall_stats[stat][stat2]
			else: return self.overall_stats[stat]
			
		except StatsError as error:
			print(error)
			return False

	def is_online(self):
		if self.check(): return False
		return self.overall_stats['online']


	def get_total_wins(self):
		return self.get_statistic('extra', 'wins')

	def get_mode_wins(self, mode="BW"):
		return self.get_statistic('winsData', mode)


	def get_win_rate(self, mode='total'):
		if mode == 'total':
			r1 = self.get_total_wins()
			r2 = self.get_statistic('extra', 'deaths')
		else:
			m = mode.lower()
			r1 = self.get_mode_wins(mode)
			r2 = self.get_statistic('extra', f'{m}Deaths')
		
		r3 = r1+r2
		return round((r1/r3)*100, 1)

	def get_kdr(self, mode='total'):
		if mode == 'total':
			r1 = self.get_statistic('kills')
			r2 = self.get_statistic('deaths')
		else:
			m = mode.lower()
			r1 = self.get_statistic('extra', f"{m}Kills")
			r2 = self.get_statistic('extra', f"{m}Deaths")

		return round(r1/r2, 2)



#_________________________________________________________________________________________________________________________________________________________________

test_connection()