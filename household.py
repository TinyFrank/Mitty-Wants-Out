import pygame
import random
from random import randint,choice
from libs import *

lnames = [ 	'Manning','Tsang','MacLeod','Flood','Elston','Rayner',
			'Triantafilou','Cracknell','Shetler','Robertson','Smith',
			'Johnson','Pilkington','Wynne','Sanders','Trump',"O'Neil",
			'Flaherty','Harper','Trudeau']

mnames = [	'Josh','Nick','Pete','Caleb','Phil','Garth','Matt','Micah',
			'Don','Al','Paul','Dan','John','Steve','Chris','Ken','Frank',
			'Berg']

fnames = [	'Cherry','Tessa','Carron','Sharon','Mel','Hannah','Lila',
			'Meghan','Becca','Sarah','Kate','Ali','Pat']

months = [	('January',31),
			('February',29),
			('March',31),
			('April',30),
			('May',31),
			('June',30),
			('July',31),
			('August',31),
			('September',30),
			('October',31),
			('November',30),
			('December',31) ]
			
lqds = ['fluid','drink','lqd food']

cntnts = ['fluid','drink','lqd food','pwdr food','soft food','soft solid','pills']

class Household(object):
	def __init__(	self,settings, screen, stats, lot_value=None, 
					materials=None, colors=None, num_proles=None,
					num_kids=None, proles=None, lname=None):
		self.settings = settings
		self.screen = screen
		self.stats = stats
		self.lot_value = lot_value
		self.materials = materials
		self.colors = colors
		self.num_proles = num_proles
		self.num_kids = num_kids
		self.proles = proles
		self.lname = lname
		self.x = None
		self.y = None
		self.town = ''
		self.yard_loot = [] #contains loot in yard
		self.yl_tally = 0	#tally of current total yard loot value
		self.yl_cap = 0
					
	def roll_hh_value(self):
		"""Roll a household value based on lot value, the poverty line 
		and a random offset of +/- 20%"""
		self.hhv_offset = ((randint(0,41)-20)/100)+1
		self.lv_offset = (self.lot_value*0.1)+1
		self.hh_value = round((self.lv_offset * self.hhv_offset) * self.stats.poverty,0)
		
	def roll_lname(self):
		"""Pick a last name"""
		if not self.lname:
			self.lname = choice(lnames)
		
	def roll_num_proles(self):
		"""Roll the number of proles living here"""
		if not self.num_proles:
			self.num_proles = choice([1,1,1,1,2,2,2,2,3,3,3,4,5,6,7,8])
		if not self.num_kids:
			if self.num_proles > 1:
				self.num_kids = self.num_proles + 1
				while self.num_kids >= self.num_proles:
					self.num_kids = choice([0,0,1,1,1,1,2,2,3,4,5,6,7])
				self.num_adults = self.num_proles - self.num_kids
			elif self.num_proles == 1:
				self.num_adults = 1
	
	def roll_wages(self):
		"""make a normalized map of wages for adult proles"""
		self.x_wages = []
		self.wages = []
		self.wages_n = 0
		for i in range(self.num_adults):
			self.x_wages.append(randint(1,101)**2)	
			self.wages_n += self.x_wages[i]
		for i in self.x_wages:
			self.wages.append(i/self.wages_n)
		
	def roll_proles(self):
		"""Roll each individual prole"""
		if not self.proles:
			self.proles = []
			#roll the adults at working age and above
			for i in range(self.num_adults):
				x_age = randint(self.stats.work_age+1,85)
				prole = Prole(	self.settings,self.screen,self.stats,
								self.hh_value,lname=self.lname,
								salary=round(self.hh_value*self.wages[i],2),
								age=x_age)
				self.proles.append(prole)
			#roll the kids below working age
			if self.num_kids:
				for i in range(self.num_kids):
					x_age = randint(0,self.stats.work_age+1)
					prole = Prole(	self.settings,self.screen,self.stats,
									self.hh_value,lname=self.lname,
									age=x_age)
					self.proles.append(prole)
			
	def adjust_wages(self):
		for i in range(self.num_adults):
			self.proles[i].salary = int(self.hh_value*self.wages[i])
			
	def construct(self):
		self.roll_hh_value()
		self.roll_lname()
		self.roll_num_proles()
		self.roll_wages()
		self.roll_proles()				
		
class Prole(object):
	def __init__(	self,settings, screen, stats, hh_value=None, 
					materials=None, colors=None, lname=None, fname=None,
					salary=None, age=None, sex=None, bday=None):
		self.settings = settings
		self.screen = screen
		self.stats = stats
		self.hh_value = hh_value
		self.materials = materials
		self.colors = colors
		self.lname = lname
		self.fname = fname
		self.salary = salary
		self.age = age
		self.sex = sex
		self.bday = bday
		
		self.construct()
		
	def construct(self):
		self.roll_sex()
		self.roll_name()
		self.roll_bday()	
		
	def roll_sex(self):
		if not self.sex:
			self.sex = choice(['M','F'])
	
	def roll_name(self):
		if not self.fname:
			if self.sex == 'M':
				self.fname = choice(mnames) + ' '
			elif self.sex == 'F':
				self.fname = choice(fnames) + ' '
	
	def roll_bday(self):
		if not self.bday:
			random.seed()
			self.bday = randint(0,365)
			for i in range(12):
				if self.bday <= months[i][1]:
					self.bday = months[i][0] + ' ' + str(self.bday)
					break
				else:
					self.bday -= months[i][1]
		
	def roll_favs(self,retailers):
		clrs = randint(1,3)
		self.fav_colors = []
		for i in range(clrs):
			self.fav_colors.append(choice(colors))
			
		brnds = randint(1,3)
		self.fav_brands = []
		for i in range(brnds):
			self.fav_brands.append(choice(retailers))
			
		mats = randint(1,3)
		self.fav_mats = []
		for i in range(mats):
			temp_mat_cat = 'fluid'
			while temp_mat_cat in cntnts:
				temp_mat_cat = choice(mat_cats)
			self.fav_mats.append(choice(std_w[temp_mat_cat][1]))
		
		print(self.fname.upper() + ' ' + self.lname.upper())
		for color in self.fav_colors:
			print(color[0])
		for mat in self.fav_mats:
			print(mat[0])
		for brand in self.fav_brands:
			print(brand.name)
