class Stats():
	"""Track stats for Fake It Til You Make It"""
	
	def __init__(self, settings):
		"""Initialize statistics."""
		self.settings = settings
		self.reset_stats()
		
		#High score should never be reset
		self.high_score = 0
	
		#Start MWO in an inactive state
		self.game_active = False
		self.loot_pip = False
		self.inv_pip = False
		
		#When to display and activate title card and menu
		self.menu = -self.game_active
		
		#holds items in Mitty's inventory
		self.inv = []
		self.inv_scroll = 0
		
		#holds items in stock in the shop
		self.stock = []
		
		#currently watched household
		self.watched_hh = None
		self.whhx,whhy = 0,0
		
		#active location and the rpeviously active location
		self.previous_hh = None
		self.active_hh = None
		self.phhx,self.phhy = 0,0
		self.ahhx,self.ahhy = 0,0
		
		#initialize Nanny State
		self.current_year = 2016
		self.min_wage = 15
		self.work_age = 18
		self.work_day = 8
		self.work_week = 5
		self.poverty = self.work_day * self.work_week * 52 * self.min_wage
		
	def roll_nstate(self):
		#update nanny state
		self.poverty = self.work_day * self.work_week * 52 * self.min_wage
		
	def reset_stats(self):
		"""Initialize statistics that can change during the game"""
		self.score = 0
		self.level = 1.0
		self.loot_val = 1.0
		self.inv = []
		self.stock = []
		self.loot_pip = False
		self.inv_pip = False
		self.map_pip = False
		self.inv_scroll = 0
		self.scrollup = False
		self.scrolldown = False
		self.s_time = 20
		self.su_timer = self.s_time
		self.sd_timer = self.s_time
		
	def scroll_inv_up(self):
		self.inv_scroll-=1
		if self.inv_scroll <= -len(self.inv):
			self.inv_scroll = 0
		
	def scroll_inv_down(self):
		self.inv_scroll+=1
		if self.inv_scroll >= len(self.inv):
			self.inv_scroll = 0
	
	def sort_inv_name(self):
		self.inv.sort(key=lambda loot: loot.short_name)
