from libs import *
from household import fnames,mnames,lnames
from random import choice
ctg_retail = [	'patio','entertainment','kitchenware','clothing',
				'sanitary','toys','plumbing','hardware',
				'souvenirs','foods','publishers','stationery',
				'pharmaceutical','automotive','camping','appliance',
				'spirits','pet supplies','furniture']

ctg_industrial = ['retail','electronics','petrochemical','plastics','fabricators',
				'agriculture','carpentry','printers','glassworks','paper',
				'fabrics','toolmaking','garment','chemical','distillery']
				
words1 = [	'First','Best','Solid','OK','High','Golden','Sunny','Jelly',
			'Friendly','Happy','Fresh','Tall','Great','Awesome','Perfect',
			'Summer','Winter','Wintry','Reliable','Dependable','Magic',
			'Magical','Salty','Super','Master','Plentiful','Quick','Fast',
			'Speedy','Excellent','Superb','Silver','Shiny','Terrific']
			
words2 = [	'Friends','Friend','Neighbour','Brother','Sister','Family',
			'Tree','Path','Beach','Town','Bend','Answer','Work','Time',
			'Cat','Dog','Bear','Lion','Tiger','Man','Woman','Machine',
			'Bean','Beans','Cats','Dogs','Men','Women','Gravy','Titan',
			'Gargoyle','Animal','State','Statue','Solution','Solutions']
			
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
		self.roll_markup()
		
	def roll_industry(self):
		if not self.ri:
			self.ri =  choice(['retail','industrial'])
		if self.ri == 'retail':
			self.ctg = choice(ctg_retail)
		elif self.ri == 'industrial':
			self.ctg = choice(ctg_industrial)
	
	def roll_name(self):
		name_type = randint(0,20)
		if name_type <= 1:
			self.name += choice(lnames) + ' '
		elif 1 < name_type <= 2:
			self.name += choice(mnames) + ' '
		elif 2 < name_type <= 3:
			self.name += choice(fnames) + ' '
		elif 3 < name_type <= 5:
			self.name += choice(lnames) + ' & ' + choice(lnames) + ' '
		elif 5 < name_type <= 6:
			self.name += choice(words2) + ' '
		elif 6 < name_type <= 12:
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
		
	def roll_markup(self):
		self.markup = 1+(randint(5,50)/100)
		self.markup *= self.markup
