import pygame
from pygame.sprite import Sprite
import spritesheet
from sprite_strip_anim import SpriteStripAnim

class Player(Sprite):
	
	def __init__(self,settings, screen):
		"""Initialize Mitty and set his starting position."""
		super(Player, self).__init__()
		self.screen = screen
		self.settings = settings
		self.frames = int(self.settings.FPS/12)
		pygame.init()
		pygame.sprite.Sprite.__init__(self)
		self.sheet = pygame.image.load('images\mittyanimate.png')#.convert_alpha()
		self.sheet_size = self.sheet.get_size()
		self.x_cells = 4
		self.y_cells = 1
		self.cell_width = int(self.sheet_size[0]/self.x_cells)
		self.cell_height = int(self.sheet_size[1]/self.y_cells)
		self.cells = []
		for y in range(0,self.sheet_size[1],self.cell_height):
			for x in range(0,self.sheet_size[0],self.cell_width):
				surface = pygame.Surface((	self.cell_width,
											self.cell_height))#.convert_alpha(self.sheet)
				surface.blit(self.sheet,(0,0),
							(x,y,self.cell_width,self.cell_height))
				colorkey = surface.get_at((0,0))
				surface.set_colorkey((colorkey))
				self.cells.append(surface)
		self.cell_position = 0
		self.rect = self.cells[0].get_rect()
		
		#create footprint rect for collisions
		self.collide_rect = self.rect.copy()
		
		self.dodge = [0,0]
		self.blocked = [0,0]
		self.edges = [0,0,0,0]
		"""dodge holds the current dodging direction for x and y with
		either a 1 (down, right) or -1 (up, left).
		it is 0 when not dodging
		
		blocked holds the current direction mitty is being blocked from
		
		edges holds the current offset of the player collide_rect to
		the opposite edges of the colliding loot or object, in the order
		(left, right, top, bottom)"""
		
		self.dest_ref = None
		self.screen_rect = self.screen.get_rect()
		self.delta = [0.0,0.0,0.0]
		self.rect.center = self.screen_rect.center		
		self.speed = 5 #pixel ditance moved per update
		self.center = [	self.rect.x+int(self.rect.width/2),
						self.rect.y+int(self.rect.height/2)]
		self.dest = [	self.rect.x+int(self.rect.width/2),
						self.rect.y+int(self.rect.height/2)]
		"""
		Initialize sprite state
		0 - Still
		1 - Walking Down
		2 - Walking Up
		3 - Walking Left
		4 - Walking Right
		"""
		self.s_state = 0
		self.crashes = 0
		
	def update(self, loots):
		"""Update the player's sprite"""
		self.center = [	self.collide_rect.x+int(self.collide_rect.width/2),
						self.collide_rect.y+int(self.collide_rect.height/2)]
		if self.dest != self.center:
			self.dx = self.dest[0] - self.center[0]
			self.dy = self.dest[1] - self.center[1]
			self.delta = [self.dx,self.dy,round((self.dx**2+self.dy**2)**(1/2))]
			
			"""self.delta contains the x distance, y distance, and total diatnce to target
			calculated via pythagoras"""
			
			collision = False
			if self.delta[2] >= self.speed:
				self.delta[0] = int((self.delta[0]/self.delta[2])*self.speed)
				self.delta[1] = int((self.delta[1]/self.delta[2])*self.speed)
				self.roll_rects()
				print(self.collide_rect.x)
				for i in loots:
					if i.collide_rect.colliderect(self.collide_rect):
						self.get_edges(i)
						self.get_blocked()
						collision = True
						break
						
				if not collision:
					self.blocked = [0,0]
				else:
					#if self.blocked[0] and self.blocked[1]:
						#self.delta[0] = 0
						#self.delta[1] = 0
					if self.blocked[0]:
						self.delta[0] = 0
						if self.delta[1] > 0:
							self.delta[1] = self.speed
						else:
							self.delta[1] = -self.speed
					elif self.blocked[1]:
						self.delta[1] = 0
						if self.delta[0] > 0:
							self.delta[0] = self.speed
						else:
							self.delta[0] = -self.speed
						
				
				
				self.rect.x += self.delta[0]
				self.rect.y += self.delta[1]
				self.center = [	self.collide_rect.x+int(self.collide_rect.width/2),
								self.collide_rect.y+int(self.collide_rect.height/2)]
			
			else:
				self.collide_rect.x = self.dest[0] - int(self.collide_rect.width/2)
				self.collide_rect.y = self.dest[1] - int(self.collide_rect.height/2)
				self.rect.x = self.collide_rect.x
				self.rect.bottom = self.collide_rect.bottom
				
	def get_edges(self, i):
		"""determine the parallel distances between opposing edges
		of the player and another sprite in order to figure out which
		direction a collision comes from"""
		i_right = i.collide_rect.x + i.collide_rect.width
		i_left = i.collide_rect.x
		i_top = i.collide_rect.y
		i_bottom = i.collide_rect.y + i.collide_rect.height
		
		right = self.collide_rect.x + self.collide_rect.width
		left = self.collide_rect.x
		top = self.collide_rect.y
		bottom = self.collide_rect.y + self.collide_rect.height
		
		self.edges[0] = left - i_right
		self.edges[1] = right - i_left
		self.edges[2] = top - i_bottom
		self.edges[3] = bottom - i_top
	
	def get_blocked(self):
		closest = max(self.edges)
		closest = self.edges.index(closest)
		if closest == 0:
			self.blocked[0] = 1
		elif closest == 1:
			self.blocked[0] = -1
		elif closest == 2:
			self.blocked[1] = -1
		elif closest == 3:
			self.blocked[1] = 1
					
	def roll_rects(self):
		self.collide_rect = self.rect.copy()
		self.collide_rect.height = int(self.rect.height * 0.25)
		self.collide_rect.bottom = self.rect.bottom
	
	def blitme(self):
		"""Draw Mitty at his current location."""
		self.screen.blit(self.cells[int(self.cell_position/20)],self.rect)
		if self.cell_position < (len(self.cells)*20) -1:
			self.cell_position += 1
		else:
			self.cell_position = 0
		
