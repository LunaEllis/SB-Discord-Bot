import sqlite3 as sql
from stats import *

global database
database = sql.connect("bot.db")

class Guild(Player):
	def __init__(self, guild):
		self.guildName = guild
		self.tbName = guild.replace(" ", "_").lower()

		global database
		self.cursor = database.cursor()
		self.commit = database.commit

		self.cursor.execute("""
		CREATE TABLE IF NOT EXISTS {name}(
		memberID INTEGER PRIMARY KEY,
		memberName TEXT,
		totalWins INTEGER,
		winGain INTEGER(16),
		winRate VARCHAR(16),
		kdr VARCHAR(16),
		bedwarsWins INTEGER,
		skywarsWins INTEGER,
		theBridgeWins INTEGER);
		""".format(name=self.tbName))



	def get_kdr(self, stats):
		r1 = stats['kills']
		r2 = stats['deaths']

		return round((r1/r2), 2)

	def get_win_rate(self, stats):
		r1 = stats['wins']
		r2 = r1 + stats['deaths']

		return round((r1/r2)*100, 1)


	def add_member(self, username):
		try:
			x = stats(username)
			if x == False: raise UsernameError(username)

			username = username.lower()

			self.cursor.execute("""
				SELECT memberName FROM {name}
				""".format(name=self.tbName))

			results = self.cursor.fetchall()
			for i in results:
				if username in i: raise UsernameError(username, "Player already in guild.")

			x1 = x['extra']['wins']
			x2 = x['winsData']
			x3 = self.get_win_rate(x)
			x4 = self.get_kdr(x)

			params = (username, x1, "+0", x3, x4, x2['BW'], x2['SW'], x2['TB'])

			self.cursor.execute("""
			INSERT INTO {name}
			VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?);
			""".format(name=self.tbName), params)

			self.commit()
			logChange(self.tbName, f"Record {username} has been added.")

		except UsernameError as error:
			print(error)
			return False


	def view_members(self):
		self.cursor.execute("""
			SELECT * FROM {name}
			""".format(name=self.tbName))
		return self.cursor.fetchall()


	def get_member_names(self):
		lst = self.view_members()
		r = []
		for i in lst:
			r.append(i[1])

		return r


	def update_record(self, ign):
		try:
			x = stats(ign)
			if x == False: raise UsernameError(ign)

			ign = ign.lower()

			x1 = x['extra']['wins']
			x2 = x['winsData']
			x3 = self.get_win_rate(x)
			x4 = self.get_kdr(x)

			self.cursor.execute("""
				SELECT totalWins FROM {name}
				WHERE memberName = '{ign}'
				""".format(name=self.tbName, ign=ign))

			a = x1- int(self.cursor.fetchall()[0][0])
			win_dif = "+{}".format(a)

			self.cursor.execute("""
				UPDATE {}
				SET totalWins = {},
				winGain = {},
				winRate = {},
				kdr = {},
				bedwarsWins = {},
				skywarsWins = {},
				theBridgeWins = {}
				WHERE memberName = '{}'
				""".format(self.tbName, x1, win_dif, x3, x4, x2['BW'], x2['SW'], x2['TB'], ign))

			self.commit()
			logChange(self.tbName, f"Record {ign} has been updated.")

		except UsernameError as error:
			print(error)
			return False


	def mvp(self):
		return self.win_gain_leaderboard()[0]


	def kdr_leaderboard(self):
		self.cursor.execute("""
			SELECT memberName, kdr FROM {name}
			ORDER BY kdr DESC;
			""".format(name=self.tbName))

		return self.cursor.fetchall()

	def win_rate_leaderboard(self):
		self.cursor.execute("""
			SELECT memberName, winRate FROM {name}
			ORDER BY winRate DESC;
			""".format(name=self.tbName))

		return self.cursor.fetchall()

	def win_gain_leaderboard(self):
		self.cursor.execute("""
			SELECT memberName, winGain FROM {name}
			ORDER BY winGain DESC;
			""".format(name=self.tbName))

		return self.cursor.fetchall()

	def total_wins_leaderboard(self):
		self.cursor.execute("""
			SELECT memberName, totalWins FROM {name}
			ORDER BY totalWins DESC;
			""".format(name=self.tbName))

		return self.cursor.fetchall()

	def bedwars_wins_leaderboard(self):
		self.cursor.execute("""
			SELECT memberName, bedwarsWins FROM {name}
			ORDER BY bedwarsWins DESC;
			""".format(name=self.tbName))

		return self.cursor.fetchall()

	def delete_record(self, username):
		ign = username.replace(" ", "_").lower()

		self.cursor.execute("""
			DELETE FROM {name}
			WHERE memberName = '{ign}'
			""".format(name=self.tbName, ign=ign))

		self.commit()
		logChange(self.tbName, f"Record {ign} has been removed.")


