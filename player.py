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
		
		self.image = SpriteStripAnim('images\mittyanimate.png', (0,0,106,234), 4, -1, True, self.frames)
		#'images\mittyanimate.png'
		self.rect = self.image.next().get_rect()
		self.screen_rect = self.screen.get_rect()
		
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
		
		
	def blitme(self):
		"""Draw Mitty at his current location."""
		self.screen.blit(self.image.next(),self.rect)
		
