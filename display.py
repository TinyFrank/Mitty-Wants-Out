import pygame
from pygame import draw, display, rect
from pygame.locals import SWSURFACE, FULLSCREEN, HWSURFACE, DOUBLEBUF
def build(settings):  
	pygame.init()
	fullscreen = True
	  
	if fullscreen:
		depth = 0
		flags = FULLSCREEN | HWSURFACE | DOUBLEBUF
	else:
		depth = 16
		flags = SWSURFACE | DOUBLEBUF
	  
	modes = display.list_modes(depth, flags)
	if fullscreen:
		if modes == -1:  # Welcome to exceptionlessland
			raise SystemExit("Failed to initialize display")
		else:
			mode = max(modes)
	else:
		mode = (settings.screen_width,settings.screen_height)
	  
	display.set_mode(mode, flags)
	#print(modes)
	#print(mode[0])
	#print(mode[1])
	return (display.get_surface(),mode[0],mode[1])
