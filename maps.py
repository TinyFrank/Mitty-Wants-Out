from random import choice, randint
from button import Button

class Hood(object):
	def __init__(self,settings,screen,stats):
		self.settings = settings
		self.screen = screen
		self.stats = stats
		self.tile = 40
		self.tiles = []
		self.scx = settings.screen_width/2
		self.scy = settings.screen_height/2
		#create 20x20 grid of empty fields
		self.roadmap = [[['F',1,None]for y in range(20)]for x in range(20)]
		
		#tile color dictionary
		self.tile_dict = {	'R':((0,0,0),'Road'),
							'L':((100,0,0),'Lot'),
							'F':((0,180,0),'Field'),
							'M':((0,0,255),"Mitty's Place")}
					
		#pick a random exit on each edge
		self.exits = []
		for i in range(4):
			self.exits.append(randint(3,18))
				
		#write the exits to the roadmap
		self.roadmap[self.exits[0]][0][0] = 'R'	#top
		self.roadmap[self.exits[1]][19][0] = 'R' #bottom
		self.roadmap[0][self.exits[2]][0] = 'R'	#left
		self.roadmap[19][self.exits[3]][0] = 'R' #right
		
		#convert exits to x,y coords
		self.exits[0] = [self.exits[0],0]
		self.exits[1] = [self.exits[1],19]
		self.exits[2] = [0,self.exits[2]]
		self.exits[3] = [19,self.exits[3]]
				
		#deicde a x meeting place for y roads
		self.x_meet = randint(5,16)
		
		#draw y roads down to meeting point
		for y in range(0,self.x_meet+1):
			self.roadmap[self.exits[0][0]][y][0] = 'R'
		for y in range(self.x_meet,19):
			self.roadmap[self.exits[1][0]][y][0] = 'R'
		
		#connect y roads at meeting point
		if self.exits[0][0] < self.exits[1][0]:
			for y in range(self.exits[0][0],self.exits[1][0]):
				self.roadmap[y][self.x_meet][0] = 'R'
		else:
			for y in range(self.exits[1][0],self.exits[0][0]):
				self.roadmap[y][self.x_meet][0] = 'R'
		
		#connect x roads
		x_L = 1
		while True:
			if self.roadmap[0+x_L][self.exits[2][1]][0] == 'F':
				self.roadmap[0+x_L][self.exits[2][1]][0] ='R'
			else:
				break
			if self.roadmap[0+x_L][self.exits[2][1]+1][0] == 'R':
				break
			if self.roadmap[0+x_L][self.exits[2][1]-1][0] == 'R':
				break
			x_L += 1
			
		x_L = 1
		while True:
			if self.roadmap[19-x_L][self.exits[3][1]][0] == 'F':
				self.roadmap[19-x_L][self.exits[3][1]][0] ='R'
			else:
				break
			if self.roadmap[19-x_L][self.exits[3][1]+1][0] == 'R':
				break
			if self.roadmap[19-x_L][self.exits[3][1]-1][0] == 'R':
				break
			x_L += 1	
		
		#running list of road/lot tile coords
		self.roads = [x for x in self.exits]
		self.lots = []
		#append all current road tiles
		for i,x in enumerate(self.roadmap):
			for j,y in enumerate(x):
				if y[0] == 'R':
					self.roads.append([i,j])
				if y[0] == 'L':
					self.lots.append([i,j])
	
	def seed_hq(self):
		#place mitty's hq on the map
		self.hq_coord = choice(self.lots)
		self.roadmap[self.hq_coord[0]][self.hq_coord[1]][0] = 'M'		
					
	def grow_hood(self,turns):
		#pick a road tile at random
		tries = 100
		while turns > 0 and tries > 0:
			self.roll = []
			for x in self.roads:
				if x[0]<1 or x[0]>18: 
					del x
				elif x[1]<1 or x[1]>18:
					del x
			self.x_tile = choice(self.roads)
			self.doable = False
			#make sure selected road is inside the 2 tile margin
			if self.x_tile[1]>1:
				if self.x_tile[1]<18:
					if self.x_tile[0]>1:
						if self.x_tile[0]<18:
							self.doable = True
			if self.doable:
				if self.roadmap[self.x_tile[0]][self.x_tile[1]-1][0] != 'R':
					if self.x_tile[1]-1 > 1:
						self.roll.append([0,-1])
				if self.roadmap[self.x_tile[0]][self.x_tile[1]+1][0] != 'R':
					if self.x_tile[1]+1 < 18:
						self.roll.append([0,+1])
				if self.roadmap[self.x_tile[0]-1][self.x_tile[1]][0] != 'R':
					if self.x_tile[0]-1 > 1:
						self.roll.append([-1,0])
				if self.roadmap[self.x_tile[0]+1][self.x_tile[1]][0] != 'R':
					if self.x_tile[0]+1 < 18:
						self.roll.append([+1,0])
				if len(self.roll) > 1:
					self.offset = choice(self.roll)
					if self.offset[0] == 0:
						if self.roadmap[self.x_tile[0]+1][self.x_tile[1]+self.offset[1]][0] not in ['R','M']:
							if self.roadmap[self.x_tile[0]-1][self.x_tile[1]+self.offset[1]][0] not in ['R','M']:
								self.roadmap[self.x_tile[0]+1][self.x_tile[1]+self.offset[1]][0] = 'L'
								self.roadmap[self.x_tile[0]-1][self.x_tile[1]+self.offset[1]][0] = 'L'
								self.lots.append([self.x_tile[0]+1,self.x_tile[1]+self.offset[1]])
								self.lots.append([self.x_tile[0]-1,self.x_tile[1]+self.offset[1]])
								self.roadmap[self.x_tile[0]][self.x_tile[1]+self.offset[1]][0] = 'R'
								self.roads.append([self.x_tile[0],self.x_tile[1]+self.offset[1]])
								turns -= 1
					else:
						if self.roadmap[self.x_tile[0]+self.offset[0]][self.x_tile[1]+1][0] not in ['R','M']:
							if self.roadmap[self.x_tile[0]+self.offset[0]][self.x_tile[1]-1][0] not in ['R','M']:
								self.roadmap[self.x_tile[0]+self.offset[0]][self.x_tile[1]+1][0] = 'L'
								self.roadmap[self.x_tile[0]+self.offset[0]][self.x_tile[1]-1][0] = 'L'
								self.lots.append([self.x_tile[0]+self.offset[0],self.x_tile[1]+1])
								self.lots.append([self.x_tile[0]+self.offset[0],self.x_tile[1]+1])
								self.roadmap[self.x_tile[0]+self.offset[0]][self.x_tile[1]][0] = 'R'
								self.roads.append([self.x_tile[0]+self.offset[0],self.x_tile[1]])
								turns -= 1
				if self.lots:
					#level up a random lot
					self.x_lot = choice(self.lots)
					if self.roadmap[self.x_lot[0]][self.x_lot[1]][1]<154:
						self.roadmap[self.x_lot[0]][self.x_lot[1]][1]+=1
						turns -= 1			
			tries -= 1
			
	def roll_rects(self):
		#create rects for each tile
		for i,x in enumerate(self.roadmap):
			for j,y in enumerate(x):
				if y[0] == 'L':
					#Lots change colour based on wealth
					hood_tile = Button(self.settings, self.screen,str(y[1]),
								self.scx-(10*self.tile)+(i*self.tile), 
								self.scy-(10*self.tile)+(j*self.tile),
								self.tile,self.tile,(	self.tile_dict[y[0]][0][0]+y[1]-1,
														self.tile_dict[y[0]][0][1],
														self.tile_dict[y[0]][0][2]),None,10)
				else:
					hood_tile = Button(self.settings, self.screen,'',
							self.scx-(10*self.tile)+(i*self.tile), 
							self.scy-(10*self.tile)+(j*self.tile),
							self.tile,self.tile,(	self.tile_dict[y[0]][0]),None,10)								
				self.tiles.append(hood_tile)
		
	def draw_hood(self):
		for i in self.tiles:
			i.draw_button()
