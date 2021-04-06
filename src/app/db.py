from app import cfg
from app import util

import MySQLdb
import MySQLdb.cursors


class DBClient:
	conn		= None
	user		= None
	password	= None
	host		= None
	dbname		= None
	port		= None

	def __init__(self, user, password, host, port, dbname):
		self.user = user
		self.password = password
		self.host = host
		self.dbname = dbname
		self.port = port

	def connect(self):
		self.conn = MySQLdb.connect(user=self.user,passwd=self.password,host=self.host,db=self.dbname,port=self.port,cursorclass=MySQLdb.cursors.DictCursor,
									charset='utf8', use_unicode=True)
		self.conn.autocommit(True)

	def query(self, sql, placeholders=None):
		try:
			cursor = self.conn.cursor()
			if placeholders:
				cursor.execute(sql, placeholders)
			else:
				cursor.execute(sql)
		except (AttributeError, MySQLdb.OperationalError):
			self.connect()
			cursor = self.conn.cursor()
			if placeholders:
				cursor.execute(sql, placeholders)
			else:
				cursor.execute(sql)
		return cursor

class GameDB(DBClient):
	def get_leaderboard(self, sort=None):
		if sort == "metacoins" or not sort:
			c = self.query("SELECT ckey,metacoins FROM SS13_player ORDER BY metacoins DESC LIMIT 50")
		elif sort == "playtime":
			c = self.query("SELECT sum(minutes),ckey FROM SS13_role_time WHERE job = 'Ghost' OR job = 'Living' GROUP BY ckey ORDER BY sum(minutes) DESC LIMIT 50")
		elif sort == "deaths":
			c = self.query('SELECT count(*),byondkey FROM SS13_death GROUP BY byondkey ORDER BY count(*) DESC LIMIT 50')
		elif sort == "connections":
			c = self.query('SELECT count(*),ckey FROM SS13_connection_log GROUP BY ckey ORDER BY count(*) DESC LIMIT 50')
		else:
			c = self.query("SELECT ckey,metacoins FROM SS13_player ORDER BY metacoins DESC LIMIT 50")
		return c.fetchall()

	def get_bans(self, start, end, query):
		c = self.query("SELECT * FROM SS13_ban WHERE hidden = 0 ORDER BY bantime DESC")
		db_bans = c.fetchall()
		bans = []
		i = 0
		for ban in db_bans:
			b = {
				"id": ban["id"],
				"ban_date": ban["bantime"],
				"round_id": ban["round_id"],
				"type":"Server" if ban["role"] == "Server" else "Job",
				"user": ban["ckey"],
				"banner": ban["a_ckey"],
				"reason": fix_chars(ban["reason"]),
				"expire_date":ban["expiration_time"],
				"unban_date":ban["unbanned_datetime"],
				"job":[ban["role"]],
				"server": ban["server_name"],
				"global": bool(ban["global_ban"])
			}

			if b["user"] == None:
				continue
			if query and not (query in b["user"].lower() or (str(b["round_id"]) == query) and b["round_id"] != 0):
				continue
			if len(bans)>0 and b["type"] == "Job" and bans[-1]["type"] == "Job" and b["user"] == bans[-1]["user"] and b["banner"] == bans[-1]["banner"] and b["reason"] == bans[-1]["reason"] and b["expire_date"] == bans[-1]["expire_date"] and b["ban_date"] == bans[-1]["ban_date"] and b["round_id"] == bans[-1]["round_id"] and b["server"] == bans[-1]["server"] and b["global"] == bans[-1]["global"]:
				bans[-1]["job"]+=b["job"]
			else:
				bans.append(b)
				i+=1

		return [bans[start:end], len(bans)]

	def get_library(self, start, end):
		c = self.query("SELECT id,author,title,category,datetime,ckey,content FROM SS13_library ORDER BY datetime DESC")
		db_books = c.fetchall()
		books = []
		i = 0
		invalid = 0
		for book in db_books:
			book["title"] = fix_chars(book["title"])
			book["content"] = fix_chars(book["content"])
			if book["content"] == "" or book["content"] == None: invalid+=1; continue
			if any([True if book["content"] == b["content"] and book["author"] == b["author"] and book["ckey"] == b["ckey"] and book["category"] == b["category"] else False for b in books]): invalid+=1; continue
			books.append(book)

			i+=1

		return [books[start:end], len(db_books)-invalid]

	def get_book(self, id):
		c = self.query("SELECT id,author,title,category,datetime,ckey,content FROM SS13_library WHERE id = {}".format(int(id)))
		book = c.fetchone()
		book["title"] = fix_chars(book["title"])
		book["content"] = fix_chars(book["content"])
		return book

	def get_poll(self, id):
		c = self.query("SELECT id,polltype,starttime,endtime,question FROM SS13_poll_question WHERE id = %s", (int(id), ))
		poll = c.fetchone()
		poll["options"] = []
		c = self.query("SELECT id,text FROM SS13_poll_option WHERE pollid = %s", (int(poll["id"]), ))
		for option in c.fetchall():
			c = self.query("SELECT COUNT(*) FROM SS13_poll_vote WHERE optionid = %s", (int(option["id"]), ))
			option["votes"] = c.fetchone()["COUNT(*)"]
			poll["options"].append(option)

		return poll

class SiteDB(DBClient):
	def link_patreon(self, ckey, patreon_id):
		self.query("INSERT IGNORE INTO patreon_link (ckey, patreon_id) VALUES (%s, %s) ON DUPLICATE KEY UPDATE ckey = %s", (ckey, patreon_id, ckey))




game_db = GameDB(
	cfg.PRIVATE["database"]["game"]["user"],
	cfg.PRIVATE["database"]["game"]["pass"],
	cfg.PRIVATE["database"]["game"]["host"],
	cfg.PRIVATE["database"]["game"]["port"],
	cfg.PRIVATE["database"]["game"]["db"]
)

site_db = SiteDB(
	cfg.PRIVATE["database"]["site"]["user"],
	cfg.PRIVATE["database"]["site"]["pass"],
	cfg.PRIVATE["database"]["site"]["host"],
	cfg.PRIVATE["database"]["site"]["port"],
	cfg.PRIVATE["database"]["site"]["db"]
)

class Player():
	def __init__(self,d):
		if not d:
			self.valid = False
			return

		self.ckey				= d["ckey"]
		self.byond_key			= d["byond_key"]
		self.firstseen			= d["firstseen"]
		self.firstseen_round_id	= d["firstseen_round_id"]
		self.lastseen			= d["lastseen"]
		self.lastseen_round_id	= d["lastseen_round_id"]
		self.ip					= d["ip"]
		self.computerid			= d["computerid"]
		self.lastadminrank		= d["lastadminrank"]
		self.accountjoindate	= d["accountjoindate"]
		self.flags				= d["flags"]
		self.antag_tokens		= d["antag_tokens"]
		self.metacoins			= d["metacoins"]
		
		self.valid = True

	def __bool__(self):
		return self.valid
	def __str__(self):
		return str(self.__dict__)
	def __repr__(self):
		return self.__str__()

	@classmethod
	def from_ckey(cls,ckey):
		ckey = util.to_ckey(ckey)
		c = game_db.query("SELECT * FROM SS13_player WHERE ckey = %s", (str(ckey),))
		d=c.fetchone()
		return cls(d)

	def set(self,q):
		c = game_db.query("UPDATE SS13_player SET {} WHERE ckey=%s".format(q), (str(self.ckey),))

	def get_notes(self):
		c = game_db.query("SELECT id,type,targetckey,adminckey,text,timestamp,severity,round_id FROM SS13_messages WHERE targetckey = %s ORDER BY timestamp DESC", (str(self.ckey), ))
		notes = list(c.fetchall())
		return notes

	def get_playtime(self):
		try:
			c = game_db.query("SELECT job,minutes FROM SS13_role_time WHERE ckey = %s", (str(self.ckey), ))
			rows = list(c.fetchall())
			roles = {}
			for row in rows:
				roles[row["job"]] = row["minutes"]
			roles["Total"] = roles["Living"]+roles["Ghost"]
			return roles
		except:
			return {"Total": 0, "Living": 0, "Ghost": 0}

	def get_deaths(self):
		try:
			c = game_db.query("SELECT count(*) FROM SS13_death WHERE byondkey = %s", (str(self.ckey), ))
			return c.fetchall()[0]["count(*)"]
		except:
			return 0

	def get_connection_count(self):
		c = game_db.query("SELECT COUNT(*) FROM SS13_connection_log WHERE ckey = %s", (str(self.ckey), ))
		return c.fetchone()["COUNT(*)"]

	def get_bans(self):
		c = game_db.query("SELECT * FROM SS13_ban WHERE ckey = %s AND hidden = 0 ORDER BY bantime DESC", (self.ckey, ))
		db_bans = c.fetchall()
		bans = []
		for ban in db_bans:
			b = {
				"id": ban["id"],
	            "round_id": ban["round_id"],
	            "type": "server" if ban["role"] == "Server" else "job",
	            "ckey": ban["ckey"], "admin": ban["a_ckey"],
	            "reason": fix_chars(ban["reason"]),
	            "ban_date": int(ban["bantime"].timestamp()),
				"expire_date": int(ban["expiration_time"].timestamp()) if ban["expiration_time"] else None,
	            "unban_date": int(ban["unbanned_datetime"].timestamp()) if ban["unbanned_datetime"] else None,
				"server": ban["server_name"],
				"global": bool(ban["global_ban"]),
				"admin": ban["a_ckey"]
	        }
			if ban["role"] and not ban["role"] == "Server":
				b["job"] = ban["role"].lower()
			bans.append(b)
		return bans

	def get_linked_accounts(self):
		investigated = [(self.ckey, "ckey")]
		to_investigate = [(self.ckey, "ckey")]
		linked_ckeys = []

		sc = game_db.query("SELECT matched_ckey FROM SS13_stickyban_matched_ckey WHERE stickyban = {}".format(repr(self.ckey)))
		sticky_linked = list(sc.fetchall())
		for sticky_link in sticky_linked:
			if (sticky_link["matched_ckey"], "ckey") not in investigated and (sticky_link["matched_ckey"], "ckey") not in to_investigate:
				investigated.append((sticky_link["matched_ckey"], "ckey"))
				to_investigate.append((sticky_link["matched_ckey"], "ckey"))
				linked_ckeys.append(sticky_link["matched_ckey"])

		while len(to_investigate) > 0:
			investigating = to_investigate.pop(len(to_investigate)-1)
			c = game_db.query("SELECT ckey,ip,computerid FROM SS13_connection_log WHERE {} = {}".format(investigating[1],repr(investigating[0])))
			linked = list(c.fetchall())
			for link in linked:
				if (link["ckey"], "ckey") not in investigated and (link["ckey"], "ckey") not in to_investigate:
					investigated.append((link["ckey"], "ckey"))
					to_investigate.append((link["ckey"], "ckey"))
					if link["ckey"] not in linked_ckeys:
						linked_ckeys.append(link["ckey"])
						sc = game_db.query("SELECT matched_ckey FROM SS13_stickyban_matched_ckey WHERE stickyban = {}".format(repr(link["ckey"])))
						sticky_linked = list(sc.fetchall())
						for sticky_link in sticky_linked:
							if (sticky_link["matched_ckey"], "ckey") not in investigated and (sticky_link["matched_ckey"], "ckey") not in to_investigate:
								investigated.append((sticky_link["matched_ckey"], "ckey"))
								to_investigate.append((sticky_link["matched_ckey"], "ckey"))
								linked_ckeys.append(sticky_link["matched_ckey"])

				if (link["ip"], "ip") not in investigated and (link["ip"], "ip") not in to_investigate:
					investigated.append((link["ip"], "ip"))
					to_investigate.append((link["ip"], "ip"))
				if (link["computerid"], "computerid") not in investigated and (link["computerid"], "computerid") not in to_investigate:
					investigated.append((link["computerid"], "computerid"))
					to_investigate.append((link["computerid"], "computerid"))

		return linked_ckeys



def fix_chars(s):
	return bytes(s, "utf8").replace(b'\x92',b"'").replace(b"\x93",b'"').replace(b"\x94",b'"').decode("utf8", "ignore").replace("&#39;", "'")

