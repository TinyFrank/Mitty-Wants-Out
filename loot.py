from random import randint,choice
import pygame
from pygame.sprite import Sprite
import libs

class Loot(object):
	def __init__(	self,settings,screen,stats,init_array)
	
	#initialization array for creating sprite copies
	self.init_array = init_array
	
	#initialize attributes
	self.raw = init_array[0] #string - part or loot
	self.l_type = init_array[1]#array - describes type of loot
	self.shape = init_array[2]#array - describes type of part
	self.l_type_num = init_array[3]#int - instance loot_types index 
	self.typ_forbid = init_array[4]#int list - forbidden type indices
	self.parts = init_array[5]#array - all parts and their descriptions
	self.largest = init_array[6]#int - index of largest part
	self.weight = init_arry[7]#float - loot weight
	self.value = init_array[8]#float - dollar value
	self.material = init_array[9]#array - primary material
	self.trim = init_array[10]#array - secondary material
	self.short_name = init_array[11]#string - short description
	self.name = init_array[12]#string - long description
	self.desc = init_array[13]#list - table description
	self.parts_desc = init_array[14]#list - table description of parts
	
	#temp attributes for calculation
	self.val_x = 0 #float - multiplier of part values
	self.val_normal = 0#int - sum of part contributions
	self.level = stats.level
	
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
	
	def construct(self):
		if not self.raw:
			self.raw = choice(['part','loot'])	
		if self.raw == 'part':
			self.construct_part()
		elif self.raw == 'loot':
			self.construct_loot()

	def construct_loot(self):
		self.roll_l_type()
		self.roll_weight()
		self.roll_parts()
		self.roll_value()
		self.roll_material()
		self.roll_trim()
		self.roll_short_name()
		self.roll_name()
		self.roll_desc()
		
		
	def construct_part(self):
		
	def roll_l_type(self):
		if not self.l_type:
			while True:
				#roll a randow number within the range of loot types
				self.l_type_num = randint(1,len(self.loot_types))
				#assign that index's array to l_type
				self.l_type = self.loot_types[l_type_num]
				#only continue loop if this l_type_num is forbidden
				if self.l_type_num not in self.typ_forbid:
					break
					
	def roll_weight(self):
		if not self.weight:
			#assign setpoint weight from l_type
			setpoint = self.ltype[3]
			offset = randint(0,101)
			offest -= 50
			offset /= 100
			offset *= self.level
			self.weight = setpoint * offset
			
	def roll_parts(self):
		#check redundancy
		if not self.parts:
			#assign l_type parts array to self.parts
			self.parts = self.l_type[2]	
			#assign materials to each part and sum v_normal
			for i,part in enumerate(self.parts):
				#store address of mat_cat info list for this part
				part_mat_cat = self.mat_cats[part[4]]
				#append rolled material array to this part
				part.append(choice(part_mat_cat))
				#add part contribution to v_normal
				self.v_normal += part[3]
				#find largest part
				score = 0
				if part[3] > score:
					leader = i #largest part index so far
					score = part[3] # largest contribution so far
				
			#assign largest part
			self.largest = leader
					
			#divide each part's contribution by v_normal to normalize it
			for part in self.parts:
				part[3] /= self.v_normal #part contrib is now >0 and <1
				#append part weight 
				part.append(part[3]*self.weight)
	
	def roll_value(self):
		if not self.value:
			self.value = 0
			for part in self.parts:
				#incrememnt value by part weight * part mat. value
				self.value += part[7]*part[6][1]
				
	def roll_material(self):
		if not self.material:
			#assign largest part material as main material
			self.material = self.parts[self.largest][6]
			self.m_color = self.material[2]
	
	def roll_trim(self):
		if not self.trim:
			#assign second part material as trim material	
			self.trim = self.parts[1][6]
			self.t_color = self.trim[2]	
			
	def roll_short_name(self):
		if not self.short_name:
			self.short_name =  str(self.material[0])
			self.short_name += str(self.l_type[0])
	
	def roll_name(self):
		if not self.name:
			self.name = ''
			self.name = str(self.color)
			self.name +=
			self.name +=
			
			
