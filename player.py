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
		self.dest = [0,0]
		self.dest_ref = None
		self.screen_rect = self.screen.get_rect()
		self.delta = [0,0]
		self.rect.center = self.screen_rect.center		
		"""
		Initialize sprite state
		0 - Still
		1 - Walking Down
		2 - Walking Up
		3 - Walking Left
		4 - Walking Right
		"""
		self.s_state = 0
		
	def update(self):
		"""Update the player's sprite"""
		self.center = [self.rect.x,self.rect.y]
		if self.dest != self.center:
			self.dest[0] - self.center[0] = dx
		
	def blitme(self):
		"""Draw Mitty at his current location."""
		#self.screen.blit(self.image.next(),self.rect)
		self.screen.blit(self.cells[int(self.cell_position/20)],self.rect)
		if self.cell_position < (len(self.cells)*20) -1:
			self.cell_position += 1
		else:
			self.cell_position = 0
		
