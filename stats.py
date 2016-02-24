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
