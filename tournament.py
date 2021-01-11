from stats import *
import sqlite3 as sql

with sql.connect("bot.db") as db:
	cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXITS tournaments(
tourID INTEGER PRIMARY KEY,
tourname VARCHAR(32) NOT NULL,
startdate INTEGER NOT NULL,
enddate INTEGER NOT NULL,
members TEXT);
""")


class Tournament(Player):
	def __init__(self, name, mode, length):
		self.name = name
		self.mode = mode

		self.start_time = datetime.now()
		self.end_time = self.start_time + timedelta(days=length)

		self.member_list = []


	def update_info(self, new, name=False, mode=False, length=False):
		if length: self.end_time = self.start_time + timedelta(days=new)
		elif name: self.name = new
		elif mode: self.mode = new


	def create_tournament(self):
		sql.cursor.execute("""
			INSERT INTO tournaments(tourname, startdate, enddate, members)
			VALUES ({name}, {start}, {end}, {members});
			""".format(name=self.name, start=self.start_time, end=self.end_time, members=""))
		self.row_id = sql.cursor.lastrowid
		self.created = True


	def register_member(self, member):
		try:
			if not self.created: raise CreationError(self.name)
			elif self.closed: raise CreationError(self.name, "Registration has already been closed.")
			elif member in self.member_list: raise CreationError(member, "Player is already registered.")

			if not stats(member): raise CreationError(member, "Username does not exist.")

			self.member_list.append(member)

		except CreationError as error:
			print(error)
			return False


	def close_registration(self):
		with open("data/temp_stats.txt", "w") as f:
			self.member_stats = {}
			for member in self.member_list:
				player = Player(member)

				if self.mode == 'total': self.member_stats[member] = player.get_statistic('extra', 'wins')
				else: self.member_stats[member] = player.get_statistic('winsData', self.mode)

				to_write = f"{member},{self.member_stats[member]}\n"
				f.write(to_write)


		sql.cursor.execute("""
			UPDATE tournaments
			SET members = {list}
			WHERE tourID = {id};
			""".format(list=self.member_list, id=self.row_id)