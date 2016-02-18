from random import randint,choice
import pygame
from pygame.sprite import Sprite
	
class Part(object):
	def __init__(	self,settings, screen, shape=None,material=None,
					weight=None,name=None,
					value=1,color=None):
							
		#list of possible loot qualities
		self.qualities = (	('shoddy ',0.2), 
							('cheapo ',0.4),
							('lousy ',0.6),
							('dated ',0.75), 
							('passable ',0.9),
							('regular ',1.0),
							('impressive ',1.25), 
							('top notch ',1.5), 
							('special edition ',2.0), 
							('luxury ',5.0))
		
		#list of possible loot conditions
		self.conditions = (	('junk ',0.2),
							('ruined ',0.3),
							('busted ',0.4),
							('dented ',0.5),
							('scratched ',0.6),
							('scuffed ',0.7),
							('lightly used ',0.8), 							
							('refurbished ',0.9),
							('new ',1.0),
							('polished ',1.2))
							
							
		#list of possible 'hard' metals, for cooking and what have you					
		self.metals = ( 	['tin ',0.6,(172,182,192),7.2], 
							['copper ',0.7,(255,120,0),8.9],
							['brass ',0.8,(218,165,32),8.5], 
							['iron ',0.9,(128,128,128),6.8],		
							['steel ',1.0,(192,192,192),8.05],
							['carbon steel ',1.5,(108,118,128),7.85],
							['stainless steel ',3.0,(176,196,222),7.5])
		
		self.woods = (		['ashwood ',0.6,(234,194,103),0.54], 
							['basswood ',0.7,(226,208,175),0.4],
							['beech ',0.8,(234,168,91),0.8], 
							['birch ',0.9,(209,190,135),0.67],	
							['butternut ',1.0,(199,134,42),0.38],		
							['cherry ',1.2,(175,114,63),0.63],
							['cedar ',0.3,(225,142,56),0.38],
							['elm ',0.8,(195,164,132),0.56],
							['hickory ',1.3,(166,110,68),0.83], 
							['lauan ',1.1,(128,101,77),0.85],
							['mahogany ',2.5,(151,44,15),0.65], 
							['maple ',1.1,(230,209,153),0.68],		
							['oak ',1.1,(187,166,108),0.75],
							['pecan ',1.5,(205,159,113),0.77],
							['poplar ',0.6,(225,214,173),0.42],
							['pine ',0.2,(231,192,103),0.42], 
							['redwood ',0.9,(147,55,0),0.45],
							['rosewood ',1.2,(101,42,7),0.9], 
							['satinwood ',1.1,(220,176,30),0.95],		
							['sycamore ',0.8,(240,211,167),0.5],
							['teak ',3.5,(180,90,29),0.98],
							['walnut ',1.8,(101,59,31),0.5])
				
		self.plastics = (	['PET ',0.3,(138,201,134),0.46], 
							['HDPE ',0.7,(255,255,255),0.97], 
							['PVC ',0.8,(255,255,255),0.83],
							['LDPE ',0.6,(255,255,255),0.91], 
							['Polypropylene ',0.5,(255,255,255),0.95],	
							['Polystyrene ',0.2,(255,255,255),0.8],		
							['Styrofoam ',0.1,(255,255,255),0.03],
							['ABS ',0.5,(255,255,255),1],
							['Acrylic ',0.6,(255,255,255),1.2],
							['Polycarbonate ',1.2,(255,255,255),1.2],
							['Acetal ',0.5,(255,255,255),1.41])
							
		self.rubbers = ( 	['lineoleum ',0.8,(241,231,188),1.2], 
							['neoprene ',2,(0,0,0),1.2], 
							['silicone ',1.2,(255,255,255),1.1],
							['natural ',0.4,(0,0,0),0.93], 
							['latex ',0.3,(241,231,188),0.9])
							
		self.ceramics = (	['glass ',0.6,(169,196,211),2.4], 
							['earthenware ',0.5,(157,54,32),2], 
							['stoneware ',0.4,(222,202,189),2.1],
							['porcelain ',1.5,(238,236,211),2.4], 
							['cement ',0.1,(164,164,164),2.9],	
							['fire clay ',1.0,(163,135,130),2],
							['red brick ',0.3,(194,98,79),1.7],	
							['terracotta ',0.8,(255,255,255),1.8])
									
		self.fibres = (		['Silk ',2.5,(255,255,255),1.3], 
							['Cotton ',1,(255,255,255),1.5], 
							['Wool ',1.2,(255,255,255),1.3],
							['Hemp ',1.1,(177,183,115),1.5], 	
							['Jute ',0.8,(196,146,94),1.4],
							['Nylon ',0.6,(255,255,255),1.1],	
							['Polyester ',0.2,(255,255,255),1.4],	
							['Acrylic ',0.4,(255,255,255),1.2],		
							['Sinew ',0.2,(224,197,164),0.8],
							['Hair ',0.1,(0,0,0),1.5],
							['Thatch ',0.1,(210,197,86),1.5])
							
		self.papers = (		['card Paper ',0.3,(182,139,97),1.5], 	
							['Bond Paper ',0.1,(255,255,255),1.5],
							['Corrugated Card Board ',0.6,(182,139,97),1.5],	
							['Poster Paper ',0.4,(255,255,255),1.5],	
							['Wax Paper ',0.5,(255,255,255),1.5])
							
		self.fluids = (		['Water ',0.01,(129,240,255),1],
							['Milk ',0.5,(255,255,255),1], 
							['Gasoline ',2.0,(234,228,168),0.71],	
							['Vegetable Oil ',0.8,(234,228,168),0.85],		
							['Motor Oil ',1.0,(165,156,132),0.9],		
							['Vinegar ',0.2,(255,255,255),1],
							['Paint ',0.5,(255,255,255),0.92],
							['Paint Thinner ',0.3,(255,255,255),0.78],
							['Mud ',0.0,(105,83,57),1.2],
							['Propane ',1.5,(255,255,255),0.49])
							
		self.naturals = (	['Bone ',0.3,(234,228,168),1.9],		
							['Leather ',2.0,(165,156,132),0.86],
							['Cork ',0.5,(105,83,57),0.23],
							['Wax ',1.0,(255,255,255),0.96])
		
		self.minerals = (	['Charcoal ',0.2,(20,20,20),2.0])
							
		#list of available paint colours					
		self.colors = (		('red ',(200,30,30)), 				
							('blue ',(30,30,200)),				
							('olive ',(128,128,0)), 			
							('khaki ',(240,230,140)),
							('dark green ',(0,100,0)),
							('lime green ',(50,205,50)),
							('teal ',(0,128,128)),
							('indigo ',(75,0,130)),
							('purple ',(128,0,128)), 
							('deep pink ',(255,20,147)),
							('pink ', (255,192,203)), 
							('beige ',(245,245,220)),
							('orange ', (255,165,0)), 
							('yellow ',(255,255,0)) )
							
		#array of available loot types
		self.loot_types ={	0:[
							'Charcoal Barbecue ',
							('bbq_D.png','bbq_L.png','bbq_M.png'),
							[["legs ","rod ",3,2,'metal'],
							["grill ","mesh ",1,3,'metal'],
							["lid ","sheet ",1,4,'metal'],
							["base ","sheet ",1,4,'metal',"charcoal"],
							["screws ","chunk ",10,1,'metal']],
							15],
							1:[
							'Propane Barbecue ',
							('bbq_D.png','bbq_L.png','bbq_M.png'),
							[["legs ","rod ",4,3,'metal'],
							["grill ","mesh ",1,5,'metal'],
							["lid ","sheet ",1,5,'metal'],
							["base ","sheet ",1,6,'metal'],
							["screws ","chunk ",20,0.25,'metal'],
							["propane tank","barrel",1,4,'metal',"propane"]],
							30]}
		
		#list of material categories
		self.mat_cats = (	'metal','wood','plastic','rubber','ceramic',
							'fibre','paper','fluid','natural')
		
		#list of standard weights for weigth baseline calculation
		self.std_w={	'metal':(8.05,self.metals),
						'wood':(0.5,self.woods),
						'plastic':(0.9,self.plastics),
						'rubber':(1.1,self.rubbers),
						'ceramic':(2.5,self.ceramics),
						'fibre':(1.3,self.fibres),
						'paper':(1.5,self.papers),
						'fluid':(1,self.fluids),
						'natural':(1,self.naturals),
						'mineral':(2,self.minerals)}
		
		#list of possible material shapes 
		self.shapes = {	'metal':(	'threaded rod','bar','tube','wire',
									'square tube','T-slot extrusion',
									'sheet','expanded sheet','angle bar',
									'mesh','strip','chunk','beam','peg'),
						'wood':(	'dowel','plank','board','trim',
									'scrap','beam','sawdust','log','branch'),
						'plastic':(	'rod','bar','sheet','strip','sheet',
									'chunk','beam','pellets','mesh'),
						'rubber':(	'tube','wire','sheet',
									'mesh','strip','chunk'),
						'ceramic':(	'tile','brick','strip',
									'scrap','powder','plate','shard'),
						'fibre':(	'thread','yarn','sheet','strip',
									'rope','strap'),
						'paper':(	'sheet','tube','confetti'),
						'natural':(	'scrap','chunk'),
						'mineral':('chunk')}
									
		#dictionary of image sets for parts
		self.part_sprites = {'rod':('L_rod.png','M_rod.png'),
							'bar':('L_bar.png','M_bar.png'),
							'beam':('L_beam.png','M_beam.png'),
							'mesh':('L_mesh.png','M_mesh.png'),
							'sheet':('L_sheet.png','M_sheet.png'),}
		
									
		#list of materials which can be dyed
		self.dyed = ['plastic','rubber','fibre','paper']
		
		self.settings = settings
		self.screen = screen
		self.weight = weight
		self.material = material
		self.shape = shape
		self.name = name
		self.value = value
		self.color = color
		#self.construct_part()
		
	def construct_part(self):
		self.roll_weight()
		if self.shape and not self.material:
			self.roll_material()
		elif self.material and not self.shape:
			self.roll_shape()
		elif not self.material and not self.shape:
			self.roll_material()
			self.roll_shape()
		self.roll_name()
		self.roll_value()
		self.roll_sprite()
		self.roll_image()
		self.create_rects()
		print(str(self.weight)+'kgs of '+self.name+'worth $'+str(self.value)+'\n')
	
	def roll_weight(self):
		if not self.weight:
			self.weight	= (self.value**2)*(randint(0,400)/100)
		
	def roll_material(self):
		if not self.material:
			self.mat_cat = 'fluid'
			while self.mat_cat == 'fluid':
				self.mat_cat = self.mat_cats[randint(0,len(self.mat_cats)-1)]
			self.material = choice(self.std_w[self.mat_cat][1])
		
		if self.mat_cat in self.dyed:
			self.ct = randint(0,len(self.colors)-1)
			self.color =  self.colors[self.ct][0]
			self.material[2] = self.colors[self.ct][1]
			
	def roll_shape(self):
		if not self.shape:
			self.shape = choice(self.shapes[self.mat_cat])
		
	def roll_name(self):
		if not self.name:
			if self.color:
				self.name = self.color.title()
			else:
				self.name = ''
		self.name += self.material[0].title()			
		self.name += self.shape.title() + ' '
	
	def roll_value(self):
		#print(str(self.weight)+' '+str(self.material[1]))
		self.value = round(self.value*self.weight*self.material[1],2)	

	def roll_sprite(self):
		self.sprite = self.part_sprites[self.shape]
						
	def roll_image(self):
		self.image_line = pygame.image.load(self.sprite[0])
		self.image_line.convert_alpha()
		#self.image_line.set_colorkey((255,255,255))
		self.image_mat = pygame.image.load(self.sprite[1])
		self.image_mat.convert_alpha()	
		#self.image_mat.set_colorkey((255,255,255))
		self.layers = (len(self.image_mat.get_palette()))
		"""
		#create highlight/shadow colours
		self.hi = [		self.material[2][0]+50,
						self.material[2][1]+50,
						self.material[2][2]+50,0]
		self.mid = [	self.material[2][0],
						self.material[2][1],
						self.material[2][2],0]
		self.low = [	self.material[2][0]-50,
						self.material[2][1]-50,
						self.material[2][2]-50,0]
		#check all colours between 0 and 255				
		for i in range(0,3):
			if self.hi[i] > 255:
				self.hi[i]=255
		for i in range(0,3):
			if self.low[i] < 0:
				self.low[i]=0	
		
		#convert colours in given ranges to hi,mid,lo		
		for i in range(0,self.layers-1):
			self.x_color = self.image_mat.get_palette_at(i)
			if self.x_color[0] > 230:
				self.image_mat.set_palette_at(i,(255,255,255,0))
			elif 255 > self.x_color[0] > 125:
				self.image_mat.set_palette_at(i,self.hi)
			elif 126 > self.x_color[0] > 70:
				self.image_mat.set_palette_at(i,self.mid)
			elif 71 > self.x_color[0] > 0:
				self.image_mat.set_palette_at(i,self.low)
		for i in range(0,len(self.image_line.get_palette())):
			if self.image_line.get_palette_at(i)[0] > 200:
				self.image_line.set_palette_at(i,(255,255,255,0))
		"""
	def create_rects(self):
		#create rects
		self.rect = self.image_line.get_rect()
		self.rect.inflate(-10,-10)
		self.rect.normalize()
		self.collide_rect = self.rect.copy()
		self.screen_rect = self.screen.get_rect()
		self.collide_rect.inflate(-10,-10)
		self.collide_rect.normalize()
		
	def blitme(self):
		"""Draw the loot at it's current location."""
		self.screen.blit(self.image_mat,self.rect) #Color (Paintjob)
		self.screen.blit(self.image_line,self.rect) #Line art	
			
class Loot(Part):
	def __init__(	self,settings,screen,value=None,color=None,
					condition=None,quality=None,material=None,
					ref=None,l_type=None,parts=None,trim=None,
					den=1,num=10):	
		super(Loot, self).__init__( settings, screen)
		
		self.l_type = l_type
		self.settings = settings
		self.screen = screen
		self.weight = None
		self.value = value
		self.color = color
		self.condition = condition
		self.quality = quality
		self.mat = material
		self.ref = ref
		self.trim = trim
		self.parts = parts
		self.num = num
		self.den = den
		self.qua_forbid = []
		self.mat_forbid = []
		self.col_forbid = []
		self.con_forbid = []
		self.typ_forbid = []		
		self.val_x = 0
		self.weight = 0
		self.val_normal = 0
		#pick a loot type if none was given
		if self.l_type == None:	
			self.specify_l_type()
		
		"""
		specifying short_name, sprite and parts - these functions
		simply pull data out of the loot_types dictionary to prevent
		you from doing it repeatedly. specify_parts() is nested at the 
		beginning of include_parts()
		"""
		
		self.specify_short_name()
		self.specify_sprite()
		
		self.specify_quality()
		self.specify_condition()
		self.specify_mat()
		self.specify_color()
		self.specify_trim()
		
		"""
		print('try: 1')
		print('PARTS:\t' + str(self.parts))
		print('VALUE:\t'+ str(self.value)+'\n')
		"""
		self.include_parts()
		"""
		print('try: 2')
		print('PARTS:\t' + str(len(self.parts)) + ' ' + str(len(self.parts[0])))
		print('X AND NORMAL:\t' + str(self.val_x)+ ' ' +str(self.val_normal))
		print('VALUE:\t'+ str(self.value)+'\n')	
		"""
		self.specify_value()
		self.compose_name()	
		self.compose_desc()
		self.set_images()
		self.create_rects()
		"""
		print('try: 3')
		print('PARTS:\t' + str(len(self.parts)) + ' ' + str(len(self.parts[0])))
		print('X AND NORMAL:\t' + str(self.val_x)+ ' ' +str(self.val_normal))
		print('VALUE:\t'+ str(self.value)+'\n')	
		"""		
	
	def specify_l_type(self):
		"""pick random loot type when none was given"""
		while True:
			self.l_type = randint(0,len(self.loot_types)-1)	
			if self.l_type not in self.typ_forbid:
				break
		
	def set_images(self):
		#compose image from source and alter based on qual/mat/color
		"""
		Loads in the three images(Dirt, Line and Material) that are
		used to generate the procedural graphic.
		The material layer is full of coloured fragments and is used
		twice; once in the bottom layer for MAT and again in the second
		from top layer for COL. Each time it's colours are changed to 
		match that of the chosen paint and material. In the case of the
		paint, some of the fragments are made transparent to reveal
		the material layer below.
		"""
		self.image_dirt = pygame.image.load(self.sprite[0])
		self.image_dirt.convert_alpha()
		self.image_line = pygame.image.load(self.sprite[1])
		self.image_line.convert_alpha()
		self.image_col = pygame.image.load(self.sprite[2])
		self.image_col.convert_alpha()
		
		#num of colour layers in 'M' palette
		self.layers = (len(self.image_col.get_palette())) 
		
		#set number of dents based on condition
		self.dents=0
		for i,con in enumerate(self.conditions):
			if con == self.condition:
				self.dents = len(self.conditions)-i
				self.con_num = i
				
		#apply the dents by make paint fragments transparent	
		if self.dents == len(self.conditions):
			for i in range(self.layers):
				self.image_col.set_palette_at(i,self.mat[2])
		elif self.dents == 0:
			for i in range(self.layers):
				self.image_col.set_palette_at(i,self.color[2]) 
			
		else:	
			for i in range(1,self.layers-1):
				if self.dents:
					self.image_col.set_palette_at(i,self.mat[2])
					self.dents -= 1
				else:
					self.image_col.set_palette_at(i,self.color[1])
				
		#pick an alpha between 0 and 255 based on condition number		
		self.alpha = (self.con_num * 51)-25
		if self.alpha > 255:
			self.alpha = 255
		if self.alpha < 0:
			self.alpha = 0
		self.alpha = 255 - self.alpha
		
	def blit_alpha(self,target, source, location, opacity):
		"""
		workaround to blit a pixel-alpha containing surface at an
		opacity other than 100
		"""
		self.x = location[0]
		self.y = location[1]
		self.temp = pygame.Surface((source.get_width(), source.get_height())).convert()
		self.temp.blit(target, (-self.x, -self.y))
		self.temp.blit(source, (0, 0))
		self.temp.set_alpha(opacity)        
		target.blit(self.temp, location)	
        
	def blitme(self):
		"""Draw the loot at it's current location."""
		self.screen.blit(self.image_col,self.rect) #Color (Paintjob)
		self.screen.blit(self.image_line,self.rect) #Line art
		self.blit_alpha(self.screen,self.image_dirt,self.rect,self.alpha)
	
	def specify_quality(self):
		"""if no quality was specified, select one randomly"""
		if self.quality == None:
			while True:
				self.q_num = randint(0,len(self.qualities)-1)
				if self.q_num not in self.qua_forbid:
					self.quality = self.qualities[self.q_num]
					break
					
		#otherwise, save quality to q_num and reload quality from list			
		else:
			self.q_num = self.quality
			self.quality = self.qualities[self.q_num]
			
	def specify_mat(self):
		"""specify a primary material if none was given"""
		if not self.mat:
			while True:
				mt = randint(0,len(self.metals)-1)
				if mt not in self.mat_forbid:
					self.mat = self.metals[mt]
					break
	
	def specify_condition(self):
		"""define a state-of-repair or 'conditon' if none was given"""
		if not self.condition:
			while True:
				ct = randint(0,len(self.conditions)-1)
				if ct not in self.con_forbid:
					self.condition = self.conditions[ct]
					break
						
	def specify_color(self):
		"""specify color if none was given"""
		if not self.color:
			while True:
				self.ct = randint(0,len(self.colors)-1)
				if self.ct not in self.col_forbid:
					self.color = self.colors[self.ct]
					break
	
	def specify_trim(self):
		"""specify trim if none was given"""
		if not self.trim:
			self.trim = self.mat
			while self.trim == self.mat:
				self.trim = self.metals[randint(0,len(self.metals)-1)]
		
	def include_parts(self):
		""""
		this very busy function first calls specify_parts() to pull down
		a list of parts from this loot's dictionary entry, so long
		as this is not already done.
		
		'parts' contains a list of lists, each one representing a part
		from which the loot is built. Each part prototype come with a 
		[0]name, [1]material form factor, [2]quantity, [3]relative 
		contribution to total value/weight, [5]material type and an 
		optional [6]th var which represents materials stored in this 
		part.
		
		As an example, there are 3 'legs' that contribute 2 to the overall
		mass, while the 10 'screws' only contribute 1. The legs are 
		metal 'rod' material whil the screws are metal 'chunks'. 
		
		The 'num'erator and 'den'ominator define the probability that 
		a part will get trim. ex. (10,3) gives a 30% for any given part.
		"""
		#get weight and parts from loot_types dictionary
		if not self.parts:
			self.specify_parts()
		self.weight = self.loot_types[self.l_type][3]
		
		#figure out what the standard weight ought to be
		self.trial_w = 0
		for part in self.parts:
			self.trial_w += part[2]*part[3]*self.std_w[part[4]][0]
		self.w_x = self.weight / self.trial_w
		#calculate a weigth factor based on the quotient above
		for part in self.parts:
			part[3] *= self.w_x		
		#for each part...
		if len(self.parts[0])<6:
			for i in self.parts:
				#20% chance to change the material to different material
				if randint(0,self.num) > self.den:
					while True:
						sel = randint(0,len(self.std_w[i[4]][1])-1)
						if sel not in self.mat_forbid:
							i.append(self.metals[sel])
							break
				else:
					i.append(self.mat)
		self.parts_desc = []
		for n,i in enumerate(self.parts):
			#val_x is the part contribtuion(i[3]) * material value
			self.val_x += i[3]*i[-1][1]
			self.val_normal += i[3]
			"""print('\t'+str(i[2])+' '+str(i[-1][0])+' '+str(i[0])+' weight = ' + str(round(i[2]*i[3]*i[4][3],2)))"""
			self.weight+=i[2]*i[3]*i[-1][3]
			self.parts_desc.append(str(i[2]))
			self.parts_desc[n]+=' '+str(i[-1][0])
			self.parts_desc[n]+=' '+str(i[0])
		self.weight = round(self.weight-self.loot_types[self.l_type][3],2)
		
		"""print('sum of part weights = ' + str(self.weight) + '\n\n')"""
		
		#create a final factor by taking the weighted average of the parts
		self.val_x /= self.val_normal
	
	def breakdown(self,inv):
		pass
	
	def specify_value(self):
		#set value
		self.value *= 20 #cost of a 'new, steel' bbq IRL, for balancing
		self.value *= round(self.quality[1]*self.mat[1],2)
		self.value *= round(self.val_x,2)
		self.value = round(self.condition[1]*self.value,2)
	def compose_name(self):
		#compose name
		self.name = self.quality[0].title() + self.mat[0].title() + self.short_name
			
	def compose_desc(self):
		#compose descriptive string for Loot PIP
		self.desc = []
		self.desc.append("Material: " + self.mat[0].upper())
		self.desc.append("Trim: " + self.trim[0].upper())
		self.desc.append("Quality: " + self.quality[0].upper())
		self.desc.append("Condition: " + self.condition[0].upper())
		self.desc.append("Color: " + self.color[0].upper())
		self.desc.append("Value: $" + str(round(self.value,2)))
		self.desc.append("Weight: " + str(self.weight).upper() + 'kg')
		
	def create_rects(self):
		#create rects
		self.rect = self.image_line.get_rect()
		self.rect.inflate(-10,-10)
		self.rect.normalize()
		self.collide_rect = self.rect.copy()
		self.screen_rect = self.screen.get_rect()
		self.collide_rect.inflate(-10,-10)
		self.collide_rect.normalize()
	
	def specify_parts(self):
		self.parts = self.loot_types[self.l_type][2]
	
	def specify_sprite(self):
		self.sprite = self.loot_types[self.l_type][1]
		
	def specify_short_name(self):
		self.short_name = self.loot_types[self.l_type][0]
	
		

		
		
		
