from libs import *
from household import fnames,mnames,lnames
from random import choice
ctg_retail = [	'patio','electronics','kitchenware','clothing',
				'sanitary','toys','plumbing','hardware',
				'souvenirs','foods','publishers','stationery',
				'pharmaceutical','automotive','camping','appliance',
				'distillery']

ctg_industrial = ['retail','electronics','petrochemical','plastics','fabricators',
				'agriculture','carpentry','printers','glassworks','paper',
				'fabrics','toolmaking','garment','chemical','distillery']
words1 = [	'First','Best','Solid','OK','High','Golden','Sunny','Jelly',
			'Friendly','Happy','Fresh','Tall','Great','Awesome','Perfect',
			'Summer','Winter','Wintry','Reliable','Dependable']
words2 = [	'Friends','Friend','Neighbour','Brother','Sister','Family',
			'Tree','Path','Beach','Town','Bend','Answer','Work','Time',
			'Cat','Dog','Bear','Lion','Tiger','Man','Woman','Machine']
class Brand(object):
	def __init__(	self,settings,stats):
		self.settings = settings
		self.stats = stats
		self.ri = ''
		self.ctg = ''
		self.name = ''
		
		self.construct()
		
	def construct(self):
		self.roll_industry()
		self.roll_name()
		
	def roll_industry(self):
		if not self.ri:
			self.ri =  choice(['retail','industrial'])
		if self.ri == 'retail':
			self.ctg = choice(ctg_retail)
		elif self.ri == 'industrial':
			self.ctg = choice(ctg_industrial)
	
	def roll_name(self):
		name_type = randint(0,20)
		if name_type <= 2:
			self.name += choice(lnames) + ' '
		elif 2 < name_type <= 4:
			self.name += choice(mnames) + ' '
		elif 4 < name_type <= 6:
			self.name += choice(fnames) + ' '
		elif 6 < name_type <= 8:
			self.name += choice(lnames) + ' & ' + choice(lnames) + ' '
		elif 8 < name_type <= 10:
			self.name += choice(words2) + ' '
		elif 10 < name_type <= 12:
			self.name += choice(words1) + ' ' + choice(words2) + ' '
		elif 12 < name_type <= 14:
			self.name += choice(words1) + ' ' + choice(words1) + ' '
			self.name += choice(words2) + ' '
		elif 14 < name_type <= 16:
			self.name += choice(words1) + ' ' + choice(lnames) + ' '
		elif 16 < name_type <= 18:
			self.name += choice(words2) + ' ' + choice(lnames) + ' '
		elif 18 < name_type <= 20:
			self.name += choice(words2) + ' '
		self.name += self.ctg.title() + ' Inc.'
		
