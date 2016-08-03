from libs import *
from random import choice
from loot import sources as sources

lnames = [ 	'Manning','Tsang','MacLeod','Flood','Elston','Rayner',
			'Triantafilou','Cracknell','Shetler','Robertson','Smith',
			'Johnson','Pilkington','Wynne','Sanders','Trump',"O'Neil",
			'Flaherty','Harper','Trudeau']

mnames = [	'Josh','Nick','Pete','Caleb','Phil','Garth','Matt','Micah',
			'Don','Al','Paul','Dan','John','Steve','Chris','Ken','Frank',
			'Berg']

fnames = [	'Cherry','Tessa','Carron','Sharon','Mel','Hannah','Lila',
			'Meghan','Becca','Sarah','Kate','Ali','Pat']
			
ctg_retail = [	'patio','entertainment','kitchenware','clothing',
				'sanitary','toys','plumbing','hardware',
				'souvenirs','foods','publishers','stationery',
				'medical','automotive','camping','appliance',
				'spirits','pet supplies','furniture','electronics']

ctg_industrial = ['petrochemical','plastics','fabricators',
				'agriculture','carpentry','printers','glassworks','paper',
				'fabrics','toolmaking','garment','chemical','distillery',
				'soapworks','semiconductor','pharmaceutical','minerals',
				'masonry']
				
words1 = [	'First','Best','Solid','OK','High','Golden','Sunny','Jelly',
			'Friendly','Happy','Fresh','Tall','Great','Awesome','Perfect',
			'Summer','Winter','Wintry','Reliable','Dependable','Magic',
			'Magical','Salty','Super','Master','Plentiful','Quick','Fast',
			'Speedy','Excellent','Superb','Silver','Shiny','Terrific',
			'Creamy','Wonderful','Instant','Smart','Clever','Wise','Snappy',
			'Sweet','Savory','Old','Young','Silent','Huge','Gross','Whole',
			'Humble','Nightly','Future','Silicon','Sheer','Adequate',
			'Good Times','Local','Family','Center','Back','Ye Olde','Royal',
			'Dunking','Smashing','Zig-Zag','Running','New','Hidden','Quiet',
			'Covert','Half','Mostly','Full','Quarter','Gigantic','Giant',
			'Discount','Tri','Little','Short','Tiny','Baby','Cute','Rolling',
			'Bouncing','Fun','Thrifty','Winning','Determined','Unstoppable',
			'Entertaining','Premium','Amused','General','Illustrious',
			'Long','Flagrant','Fragrant','Strong','Mighty','Proud','Hypnotic',
			'Greasey','Non-Stop','Wry','Furtive','Yummy','Cheap','Bargain',
			'Festive','Prickly','Divergent','Nimble','Famous','Puzzled','Cool',
			'Normal','Soft','Jolly','Exclusive','Lush','Far','Substantial',
			'Harsh','Tenuous','Shallow','Tight-Fisted','Hard-Boiled','Iron-Fisted',
			'Irregular','Dynamic','Sassy','Tasteful','Ossified','Hapless',
			'Neat','Pastoral','Graceful','Upbeat','Successful','Special',
			'Chief','Tangible','Didactic','Near','Wet','Sneaky','Fantastic',
			'Cloistered','Vivacious','Glorious','Steady','Instinctive',
			'Armoatic','Economical','Powerful','Spiffy','Jiffy','Average',
			'Decent','Fair']
			

			
words2 = [	'Friends','Friend','Neighbour','Brother','Sister','Family',
			'Tree','Path','Beach','Town','Bend','Answer','Work','Time',
			'Cat','Dog','Bear','Lion','Tiger','Man','Woman','Machine',
			'Bean','Beans','Cats','Dogs','Men','Women','Gravy','Titan',
			'Gargoyle','Animal','State','Statue','Solution','Solutions',
			'Invention','Player','Worker','Boss','Place','House','Meat',
			'Baps','Shop','Exchange','Things','Stuff','Bonanza','Madness',
			'Corner','Job','Hand','Foot','Nose','Eye','Eyes','Finger',
			'Fingers','Fruit','Produce','Production','Lord','Lady','Knight',
			'Tower','Castle','Alley','Depot','Center','Market','Shoppe',
			'Firkin','Club','Jelly','Specialists','Kaboom','Dollar','Penny',
			'Nickel','Dime','Quarter','Discount','Dimes','Snipe','Ray','Chicken',
			'Troll','Judas','Partner','Kirk','Cricket','Fun','Spot','Child',
			'Nugget','Nuggets','Partners','Thing','Dollar','Specialist',
			'Azimuth']

btype = [ ' Inc.',' Co.',' Ltd.',' LLC',' Outlet']

conj = [' & ',' + ',' and ',' of ',' for ']
			
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
		self.roll_specs()
		self.roll_quality()
		
	def roll_industry(self):
		if not self.ri:
			self.ri =  choice(['retail','industrial'])
		if self.ri == 'retail':
			self.ctg = choice(ctg_retail)
		elif self.ri == 'industrial':
			self.ctg = choice(ctg_industrial)
	
	def roll_name(self):
		name_type = randint(0,27)
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
			self.name += choice(lnames) + ' ' + choice(words2) + ' '
		elif 18 < name_type <= 20:
			self.name += choice(words2) + ' '
		elif 20 < name_type <= 25:
			self.name += choice(words2) + choice(conj) + choice(words2) + ' '
		elif 25 < name_type <= 27:
			self.name += choice(words1) + ' '
		self.name += self.ctg.title() + choice(btype)
		
	def roll_markup(self):
		self.markup = 1+(randint(5,50)/100)
		self.markup *= self.markup
	
	def roll_specs(self):
		self.num_mats = randint(1,4)
		self.mats = []
		self.num_colors = randint(1,4)
		self.colors = []
		for i in range(0,self.num_colors):
			self.colors.append(choice(colors))
		self.label = []
		for i in range(0,25):
			self.label.append(choice(colors))
			
		#if this is a retail brand, create fav mfrs
		if self.ri == 'retail':
			self.num_mfrs = randint(1,6)
			self.mfrs = []
		
		#record viable mat_cats for this company
		if self.ri == 'industrial':
			for source in sources:
				if self.ctg == source[0]: 
					self.mat_cats = source[1]
	
	def roll_quality(self):
		self.qtys = []
		qtys = randint(1,3)
		for i in range(qtys):
			self.qtys.append(choice(qualities))
