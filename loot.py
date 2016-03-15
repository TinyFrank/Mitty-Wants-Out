from random import randint,choice
import random
import pygame
from pygame.sprite import Sprite
import libs
import copy
import time

gen_init = 	[choice(('loot','part')),None,None,None,[],[],[],None,
			None,[],[],[],'','',[],[],[],None,[],[],[],[],'',[],'','']
"""can be initialized with a presets for 0,2,3,7,9,10"""
class Loot(object):
	def __init__(	self,settings,screen,loot_val,init_array=None,ref=None,
					brands=[]):
		
		#initialization array for creating sprite copies
		#self.init_array = init_array
		
		#initialize attributes
		if init_array:
			self.raw = init_array[0] #string - part or loot
			self.l_type = init_array[1]#array - describes type of loot
			self.shape = init_array[2]#array - describes type of part
			self.l_type_num = init_array[3]#int - instance loot_types index 
			self.typ_forbid = init_array[4]#int list - forbidden type indices
			self.parts = init_array[5]#array - all parts and their descriptions
			self.largest = init_array[6]#int - index of largest part
			self.weight = init_array[7]#float - loot weight
			self.value = init_array[8]#float - dollar value
			self.material = init_array[9]#array - primary material
			self.trim = init_array[10]#array - secondary material
			self.quality = init_array[11]#tuple - name and number
			self.short_name = init_array[12]#string - short description
			self.name = init_array[13]#string - long description
			self.desc = init_array[14]#list - table description
			self.parts_desc = init_array[15]#list - table description of parts
			self.condition = init_array[16]#tuple - name and number
			self.mat_cat = init_array[17]#string - material category
			self.color = init_array[18]#array - color name and rgb
			self.m_color = init_array[19]#list - rgb
			self.t_color = init_array[20]#list - rgb
			self.sprite = init_array[21]#string - sprite file handle
			self.label = init_array[22]#array - label color palette
			self.brand = init_array[23]#string - brand name
			self.manufacturer = init_array[24]#string - name of manufacturer
		else:
			self.raw = choice(('loot','part'))
			self.l_type = None
			self.shape = None
			self.l_type_num = None
			self.typ_forbid = []
			self.parts = []
			self.largest = []
			self.weight = None
			self.value = None
			self.material = []
			self.trim = []
			self.quality = []
			self.short_name = ''
			self.name = ''
			self.desc = []
			self.parts_desc = []
			self.condition = []
			self.mat_cat = None
			self.color = []
			self.m_color = []
			self.t_color = []
			self.sprite = ''
			self.label = []
			self.brand = ''
			self.manufacturer = ''
					
		#overwrite ref if one was provided
		if ref:
			self.ref = ref
			
		#cast loot as a part if shape was given (no condition or sub-parts)	
		if self.shape:
			self.raw = 'part'	
			self.condition = None
			self.parts = [None]
		
		#temp attributes for calculation
		self.val_x = 0 #float - multiplier of part values
		self.val_normal = 0#int - sum of part contributions
		self.level = loot_val
		self.settings = settings
		self.screen = screen
		self.brands = brands
		self.spritepath = 'images/'
		sys_r = random.SystemRandom()
		
		#initialize external lists
		self.qualities = libs.qualities
		self.conditions = libs.conditions
		self.metals = libs.metals 
		self.woods = libs.woods 
		self.plastics = libs.plastics 
		self.rubbers = libs.rubbers 
		self.ceramics = libs.ceramics 
		self.fibres = libs.fibres 
		self.papers = libs.papers 
		self.fluids = libs.fluids
		self.naturals = libs.naturals 
		self.minerals = libs.minerals 
		self.colors = libs.colors 
		self.loot_types = libs.loot_types
		self.mat_cats = libs.mat_cats
		self.shapes = libs.shapes 
		self.dyed = libs.dyed
		self.std_w = libs.std_w
		self.part_sprites = libs.part_sprites

	def construct(self):
		if self.raw == 'loot':
			self.roll_l_type()
		self.roll_weight()
		if self.raw == 'loot':
			self.roll_parts()
			self.roll_condition()
			self.roll_brand()
		self.roll_material()
		self.roll_color()
		if self.raw == 'part':
			self.roll_shape() 
		self.roll_quality()
		self.roll_value()
		self.roll_trim()
		self.roll_short_name()
		self.roll_name()
		self.roll_desc()
		if self.raw == 'loot':
			self.roll_parts_desc()
		self.roll_sprite()
		self.roll_label()
		self.roll_image()
		self.roll_rects()
		#rebuild results into init_array for creating copies
		self.init_array=[	self.raw,self.l_type,self.shape,
			self.l_type_num,self.typ_forbid,self.parts,self.largest,
			self.weight,self.value,self.material, self.trim,
			self.quality,self.short_name,self.name,self.desc,
			self.parts_desc,self.condition,self.mat_cat,self.color,
			self.m_color,self.t_color,self.sprite,self.label,self.brand,
			self.manufacturer]
			
	def rebuild(self):
		self.roll_image()
		self.roll_rects()
		self.init_array=[	self.raw,self.l_type,self.shape,
			self.l_type_num,self.typ_forbid,self.parts,self.largest,
			self.weight,self.value,self.material, self.trim,
			self.quality,self.short_name,self.name,self.desc,
			self.parts_desc,self.condition,self.mat_cat,self.color,
			self.m_color,self.t_color,self.sprite,self.label,self.brand,
			self.manufacturer]
	
	def roll_l_type(self):
		if not self.l_type_num:
			while True:
				#roll a random number within the range of loot types
				self.l_type_num = randint(1,len(self.loot_types))
				#only continue loop if this l_type_num is forbidden
				if self.l_type_num not in self.typ_forbid:
					break
			
		if not self.l_type: 
			#assign that index's array to l_type
			self.l_type = self.loot_types[self.l_type_num]
				
	def roll_weight(self):
		if not self.weight:
			if self.raw == 'loot':
				#assign setpoint weight from l_type
				setpoint = self.l_type[3]
				offset = float(randint(0,201))
				offset = offset - 50.5 * self.level
				offset = offset / 1000.0
				offset = offset + 1.0
				self.weight = round(setpoint * offset,2)
			elif self.raw == 'part':
				#pick random weight based on level
				self.weight = randint(1,101)/100
				#mutiply 0>1 range by level squared and round to 2 digits
				self.weight = round(self.weight*self.level**2,2)
		elif self.weight:
			if self.raw == 'loot':
				setpoint = self.l_type[3]
				self.weight *= setpoint
			
	def roll_parts(self):
		#check redundancy
		if not self.parts:
			#assign l_type parts array to self.parts
			self.parts = self.l_type[2]	
			#assign materials to each part and sum v_normal
			score = 0
			for i,part in enumerate(self.parts):
				#store address of mat_cat info list for this part
				part_mat_cat = choice(part[4])
				#append rolled material array to this part
				part.append(None)
				part[6]=choice(self.std_w[part_mat_cat][1])
				#add part contribution to v_normal
				self.val_normal += part[3]
				#find largest part
				if part[3] > score:
					leader = i #largest part index so far
					score = part[3] # largest contribution so far
				if i == 1:
					self.trim_cat = part_mat_cat
				#if given 2 qtys, pick randint betweent them
				if str(part[2].__class__) ==("<class 'list'>"):
					part[2][2] = randint(part[2][0],part[2][1])
			#assign largest part
			self.largest = leader
					
			#divide each part's contribution by v_normal to normalize it
			for part in self.parts:
				part[3] /= self.val_normal #part contrib is now >0 and <1
				#append part weight 
				part.append(None)
				part[7]= part[3]*self.weight
			if self.material:
				#assign largest part material as main material
				if self.parts[self.largest][0] != 'contents ':
					self.parts[self.largest][6] = self.material
				elif self.parts[self.largest][0] == 'contents ':
					self.parts[0][6] = self.material
			if self.trim and len(self.parts)>1:
				if self.trim in self.std_w[self.trim_cat][1]:
					self.parts[1][6] = self.trim
			
	def roll_brand(self):
		if not self.brand:
			relevant_brands = []
			relevant_industries = []
			for brand in self.brands:
				if brand.ctg in self.l_type[5]:
					relevant_brands.append(brand)
				if brand.ctg in self.l_type[4]:
					relevant_industries.append(brand)
		self.brand = choice(relevant_brands)
		self.manufacturer = choice(relevant_industries)
		
	def roll_condition(self):
		if not self.condition:
			#select condition at random
			self.condition = choice(self.conditions)
						
	def roll_material(self):
		if not self.material:
			if self.raw == 'loot':
				#assign largest part material as main material
				if self.parts[self.largest][0] != 'contents ':
					self.material = self.parts[self.largest][6]
				elif self.parts[self.largest][0] == 'contents ':
					self.material = self.parts[0][6]
				self.m_color = self.material[2]
				self.color = choice(self.colors)
			if self.raw == 'part':
				self.mat_cat = 'fluid'
				if self.shape:
					#with predefined shape, find suitable category
					while self.shape not in self.shapes[self.mat_cat]:
						self.mat_cat = self.mat_cats[randint(0,len(self.mat_cats)-1)]
				#pick and mat cat but fluid
				elif not self.shape:
					while self.mat_cat == 'fluid':
						self.mat_cat = self.mat_cats[randint(0,len(self.mat_cats)-1)]
					#material becomes any mat array from chosen category
				self.material = choice(self.std_w[self.mat_cat][1])
				self.color = ['N/A',[0,0,0,0]]
				#main color becomes mat color
				self.color[1] = self.material[2]
				self.color[0] = self.material[0]
				#if the material is dyed, select a dye color 
				if self.mat_cat in self.dyed:
					self.ct = randint(0,len(self.colors)-1)
					self.color =  self.colors[self.ct]
					
	def roll_color(self):
		if not self.color:
			self.color = ['N/A',[0,0,0]]
			if self.raw == 'loot':
				self.m_color = self.material[2]
				self.color = choice(self.colors)
			if self.raw == 'part':
				self.color[1] = self.material[2]
				self.color[0] = self.material[0]
				if self.mat_cat in self.dyed:
					self.ct = randint(0,len(self.colors)-1)
					self.color =  self.colors[self.ct]
					
	def roll_shape(self):
		if not self.shape:
			self.shape = choice(self.shapes[self.mat_cat])	
			
	def roll_quality(self):
		if not self.quality:
			#select condition at random
			self.quality = choice(self.qualities)
								
	def roll_value(self):
		if not self.value:
			self.value = 0
			if self.raw == 'loot':
				for part in self.parts:
					#incrememnt value by part weight * part mat. value
					self.value += part[7]*part[6][1]
				self.value *= self.quality[1]
			elif self.raw == 'part':
				self.value = self.weight*self.material[1]*(self.quality[1]**self.level)
		self.value = round(self.value,2)
	
	def roll_trim(self):
		if self.trim:
			if self.raw == "loot" and len(self.parts) > 1:
				if self.parts[1][6] == self.trim: 
					self.t_color = self.trim[2]
					self.t_color_name = ''
				else:
					#for parts and single part loots, pick randomly
					self.trimx = choice(self.colors)
					self.trim = []
					for col in self.trimx:
						self.trim.append(col)
					self.trim.append(self.trim[1])
					self.t_color = self.trim[1]
					self.t_color_name = self.trim[0]
					
			elif self.raw == "loot" and len(self.parts) == 1:
				#for parts and single part loots, pick randomly
				self.trimx = choice(self.colors)
				self.trim = []
				for col in self.trimx:
					self.trim.append(col)
				self.trim.append(self.trim[1])
				self.t_color = self.trim[1]
				self.t_color_name = self.trim[0]
				print(self.name+' now has '+str(self.t_color_name))
				
		elif not self.trim:
			if self.raw == "loot" and len(self.parts) > 1:
				#assign second part material as trim material	
				self.trim = self.parts[1][6]
				self.t_color = self.trim[2]
				self.t_color_name = ' '
				#if the material is dyed, select a dye color 
				self.trim_cat = self.parts[1][4][0]
				if self.trim_cat in self.dyed:
					self.ct = randint(0,len(self.colors)-1)
					self.t_color =  self.colors[self.ct][1]					
					self.t_color_name =  self.colors[self.ct][0]
					
			elif self.raw == "loot" and len(self.parts) == 1:
				#for parts and single part loots, pick randomly
				self.trimx = choice(self.colors)
				self.trim = []
				for col in self.trimx:
					self.trim.append(col)
				self.trim.append(self.trim[1])
				self.t_color = self.trim[1]
				self.t_color_name = self.trim[0]
				
	def roll_short_name(self):
		if not self.short_name:
			#assign shape name for parts
			if self.raw == 'part':
				self.short_name = str(self.shape) 
			#assign loot type name for loots
			elif self.raw == 'loot':
				self.short_name = str(self.l_type[0])
	
	def roll_name(self):
		if not self.name:
			self.name = ''
			#add quality,color and material short name
			self.name += str(self.quality[0].title())
			if self.color[0] != self.material[0]:
				self.name += str(self.color[0]).title()
			self.name += str(self.material[0])
			self.name += self.short_name
			
	def roll_desc(self):
		if not self.desc:
			#compose descriptive string for PIP
			self.desc = []
			self.desc.append("Material: " + self.material[0].upper())
			try:
				if self.t_color_name:
					self.desc.append("Trim: "+self.t_color_name.upper()+' ')
					if self.t_color_name != self.trim[0]:
						self.desc[1] += self.trim[0].upper()
				elif not self.t_color_name:
					self.desc.append("Trim: "+ self.trim[0].upper())
			except:
				self.desc.append("Trim: N/A")
			self.desc.append("Quality: " + self.quality[0].upper())
			try:
				self.desc.append("Shape: " + self.shape.upper())
			except:
				self.desc.append("Shape: N/A")
			try:
				self.desc.append("Condition: " + self.condition[0].upper())
			except:
				self.desc.append("Condition: N/A")
			try:
				self.desc.append("Color: " + self.color[0].upper())
			except:
				self.desc.append("Color: N/A")
			try:
				self.desc.append("Retailer: " + self.brand.name)
			except:
				self.desc.append("Retailer: N/A")
			try:
				self.desc.append("Manufacturer: " + self.manufacturer.name)
			except:
				self.desc.append("Manufacturer: N/A")
				
			self.desc.append("Value: $" + str(round(self.value,2)))
			self.desc.append("Weight: " + str(self.weight).upper() + 'kg')
			
	def roll_parts_desc(self):
		#compose list of descriptive strings for parts
		if not self.parts_desc:
			self.parts_desc = []
			for part in self.parts: 
				#assign part qty. + part material + part name
				if str(part[2].__class__) == "<class 'list'>":
					part_qty = part[2][2]
				else:
					part_qty = part[2]
				pd = str(part_qty) + ' ' + str(part[6][0]) + ' '+ part[0]
				self.parts_desc.append(pd)
	
	def roll_sprite(self):
		#set sprite by shape or loot type
		if not self.sprite:
			if self.raw == 'part':
				self.sprite = choice(self.part_sprites[self.shape])
			elif self.raw == 'loot':
				self.sprite = choice(self.l_type[1])
	
	def roll_label(self):
		if not self.label:
			self.label = []
			for i in range(0,21):
				self.label.append(choice(self.colors))
						
	def roll_image(self):
		#always load LINE layer, convert 
		self.image_line = pygame.image.load(self.spritepath+"L_" + str(self.sprite)+'.png')
		self.image_line.convert_alpha()
		
		#always load bottom MATERIAL layer, convert 
		self.image_mat = pygame.image.load(self.spritepath+"M_" + str(self.sprite)+'.png')
		self.image_mat.convert_alpha()
		
		#number of colors/layers in the current working image	
		self.layers = (len(self.image_mat.get_palette()))
		
		#iterate through mat layer to shade	
		for i in range(0,self.layers-1):
			#assign working color to x_color
			self.x_color = self.image_mat.get_palette_at(i)
			#determine working color offset from middle grey
			self.grey_offset = (self.x_color[0]-127)
			#add offset to self.color to make new color
			self.n_color = [self.color[1][0]+self.grey_offset,
							self.color[1][1]+self.grey_offset,
							self.color[1][2]+self.grey_offset]
			#truncate new color to fall on RGB scale		
			self.n_color2=[0,0,0]
			for num,rgbint in enumerate(self.n_color):
				if rgbint>255:
					self.n_color2[num]=255
				elif rgbint<0:
					self.n_color2[num]=0
				elif 0<rgbint<256:
					self.n_color2[num]=rgbint
			#wrap new color back into tuple and assign back to palette		
			self.n_color=[self.n_color2[0],self.n_color2[1],self.n_color2[2]]
			self.image_mat.set_palette_at(i,self.n_color2)
		
		try:
			#if there is a MATERIAL-2 layer, load and convert it	
			self.image_trim = pygame.image.load('images/M2_' + str(self.sprite)+'.png')
			self.image_trim.convert_alpha()	
			self.layers = len(self.image_trim.get_palette())
			for i in range(0,self.layers-1):
				self.x_color = self.image_trim.get_palette_at(i)
				#grey offset, same as above
				self.grey_offset = (self.x_color[0]-127)
				#by now t_color should be an rgb tuple
				self.n_color = [self.t_color[0]+self.grey_offset,
								self.t_color[1]+self.grey_offset,
								self.t_color[2]+self.grey_offset]
				self.n_color2=[0,0,0]
				for num,rgbint in enumerate(self.n_color):
					if rgbint>255:
						self.n_color2[num]=255
					elif rgbint<0:
						self.n_color2[num]=0
					elif 0<rgbint<256:
						self.n_color2[num]=rgbint
						
				self.n_color=(self.n_color2[0],self.n_color2[1],self.n_color2[2])
				self.image_trim.set_palette_at(i,self.n_color)
		except:
			pass
		
		try:
			#if there is a COLOR layer, load and convert it
			self.image_col = pygame.image.load('images/C_' + str(self.sprite)+'.png')
			self.image_col.convert_alpha()	
			#get number of colors in working layer palette
			self.layers = len(self.image_col.get_palette())
			#iterate over item label palette and apply to layer
			for i in range(0,self.layers-1):
				self.image_col.set_palette_at(i,self.label[i][1])
		except:
			pass
		
		try:
			#if there is a DIRT layer, load and convert it
			self.image_dirt = pygame.image.load('images/D_' + str(self.sprite)+'.png')
			self.image_dirt.convert_alpha()
		except:
			pass		
				
	def roll_rects(self):
		#create rects
		self.rect = self.image_line.get_rect()
		self.rect.inflate(-10,-10)
		self.rect.normalize()
		self.collide_rect = self.rect.copy()
		self.screen_rect = self.screen.get_rect()
		self.collide_rect.inflate(-10,-10)
		self.collide_rect.normalize()
		
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
		self.screen.blit(self.image_mat,self.rect) #Color (Paintjob)
		try:
			self.screen.blit(self.image_trim,self.rect) #Trim (Paintjob)
		except:
			pass
		try:
			self.screen.blit(self.image_col,self.rect) #Colored Labels
		except:
			pass
		self.screen.blit(self.image_line,self.rect) #Line art
		try:
			#dirt layer
			self.blit_alpha(self.screen,self.image_dirt,self.rect,self.alpha)
		except:
			pass
	
