import sys
from time import sleep
from random import randint
import json
from player import Player
from loot import *
import pygame
import copy
from button import Button
import math

def place_loot(settings, screen, stats, loots):
	#instantiate one loot
	loot_inst = Loot(settings, screen, stats.loot_val) 
	loot_inst.construct()
	placed = False
	timeout=0
	while not placed:
		x = randint(50,screen.get_width()-50)
		y = randint(150,screen.get_height()-50)
		loot_inst.rect.x = x - (loot_inst.rect.width/2)
		loot_inst.rect.y = y - (loot_inst.rect.height/2)
		hits = 0
		if loots:
			for i in loots:
				if 	i.rect.colliderect(loot_inst.rect):
					hits=1
		if not hits and loots:
			loot_inst.rect.x = x - (loot_inst.rect.width/2)
			loot_inst.rect.y = y - (loot_inst.rect.height/2)
			loots.append(loot_inst)
			loots.sort(key = lambda x: x.rect.y)
			placed = True
		if not hits and not loots:
			loot_inst.rect.x = x - (loot_inst.rect.width/2)
			loot_inst.rect.y = y - (loot_inst.rect.height/2)
			loots.append(loot_inst)
			loots.sort(key = lambda x: x.rect.y)
			placed = True
		timeout+=1
		if timeout > 50:
			placed = True	

def take_loot(stats,loots,lp_buttons):
	#delete original loot from the loot pile
	#add coppied loot to inventory
	stats.inv.append(lp_buttons[6])
	del loots[lp_buttons[6].ref]	
	
	close_loot_pip(stats,lp_buttons)
	
def close_loot_pip(stats,lp_buttons):
	#delete alll buttons related to this loot
	del lp_buttons[6:]
	#turn off the loot pip
	stats.loot_pip = False
	
def check_keydown_events(	event, settings, screen, stats, loots, 
							lp_buttons, ip_buttons):
	"""Respond to keypresses"""
	if event.key == pygame.K_q:
		sys.exit()
	elif event.key == pygame.K_c:
		#place_loot(settings, screen, stats, loots)
		stats.sort_inv_name()
	elif event.key == pygame.K_f:
		for i in range(0,101):
			place_loot(settings, screen, stats, loots)
	elif event.key == pygame.K_g:
		print(len(loots))
		while True:
			try:
				stats.inv.append(loots.pop(-1))
			except:
				break
			#stats.inv.append(loots[i])
			#loots.remove(loots[i])
	#D is my debug key - click for terminal infos
	elif event.key == pygame.K_d:
		for i in loots:
			print(i.desc)
		for i in stats.inv:
			print(i.desc)
	elif event.key == pygame.K_e and stats.loot_pip:
		take_loot(stats,loots,lp_buttons)
	elif not stats.inv_pip and not stats.loot_pip:
		if event.key == pygame.K_i:
			inv_pip(settings,screen,stats,ip_buttons)
	elif stats.inv_pip:
		if event.key == pygame.K_ESCAPE: 
			close_inv_pip(stats,settings,screen, ip_buttons)
		elif event.key == pygame.K_i:
			close_inv_pip(stats,settings,screen,ip_buttons)
		elif event.key == pygame.K_UP or event.key == pygame.K_w:
			stats.scroll_inv_up()
			close_loot_pip(stats,lp_buttons)
			close_inv_pip(stats,settings,screen,ip_buttons)
			inv_pip(settings,screen,stats,ip_buttons)
		elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
			stats.scroll_inv_down()
			close_loot_pip(stats,lp_buttons)
			close_inv_pip(stats,settings,screen,ip_buttons)
			inv_pip(settings,screen,stats,ip_buttons)
	elif stats.loot_pip:
		if event.key == pygame.K_ESCAPE:
			close_loot_pip(stats,lp_buttons)	
#def check_keyup_events(event,settings, screen, stats):
	#"""Respond to keyreleases"""		

def check_buttons(	settings, screen, stats, buttons, ig_buttons, 
					lp_buttons, ip_buttons, loots, mouse_pos):
	"""Start new game when player clicks Play"""
	if not stats.game_active:
		if buttons[0].rect.collidepoint(mouse_pos[0], mouse_pos[1]):
			stats.game_active=True
		elif  buttons[1].rect.collidepoint(mouse_pos[0], mouse_pos[1]):
			sys.exit()
		
	if stats.game_active:
		if ig_buttons[0].rect.collidepoint(mouse_pos[0], mouse_pos[1]):
			inv_pip(settings,screen,stats,ip_buttons)
		elif ig_buttons[4].rect.collidepoint(mouse_pos[0], mouse_pos[1]):
			stats.game_active=False
		elif stats.loot_pip:
			if lp_buttons[2].rect.collidepoint(mouse_pos[0], mouse_pos[1]):
				take_loot(stats,loots,lp_buttons)
		elif stats.inv_pip:
			if not ip_buttons[0].rect.collidepoint(mouse_pos[0], mouse_pos[1]):
				close_inv_pip(stats,settings,screen,ip_buttons)
				
def loot_pip(settings,screen,stats,lp_buttons,scx,scy,loot,i):	
	loot_inst = Loot(	settings, 
						screen, 
						loot_val = stats.loot_val,
						init_array = loot.init_array,
						ref = i)
							
	lp_buttons.append(loot_inst)
	lp_buttons[1] = Button(	settings, screen, loot.name, scx-275, 
							scy-200, 550,50,(0,0,0),None,18)
							
	for x in range(0,len(loot.desc)):
		text_line = Button(settings, screen, loot.desc[x],
		scx+10, scy-55+x*25, 230,30,(0,0,0),None,14)
		lp_buttons.append(text_line)
		
	lp_buttons[6].rect.center = lp_buttons[4].rect.center 
	stats.loot_pip = True	

def inv_pip(settings,screen,stats,ip_buttons):
	scx = settings.screen_width/2
	scy = settings.screen_height/2
	if stats.inv:
		inv_inst = Loot(	settings, 
						screen, 
						loot_val = stats.loot_val,
						init_array = stats.inv[stats.inv_scroll].init_array,)
						
	
		first6 = len(stats.inv)
		
		if first6 > 11:
			first6 = 11
			
		for i in range(0,first6):
			index = i + stats.inv_scroll
			if index >= len(stats.inv):
				index -= len(stats.inv)
			#print(str(first6) +  ' ' + str(i) + ' ' + str(stats.inv_scroll) + ' ' + str(index))
			ip_buttons[1+i].msg = stats.inv[0+index].name
			ip_buttons[1+i].prep_msg()
	#if stats.inv:	
		for x in range(0,len(inv_inst.desc)):
			text_line = Button(settings, screen, inv_inst.desc[x],
			scx+190, scy-160+x*25, 300,30,(0,0,0),None,15)
			ip_buttons.append(text_line)
		ip_buttons.append(inv_inst)
		ip_buttons[-1].rect.center = ip_buttons[13].rect.center 
	
	#calculate the height of the above series of buttons
		ip_dheight = len(inv_inst.desc)*25
		try:
			for x in range(0,len(inv_inst.parts_desc)):	
				text_line = Button(settings, screen, inv_inst.parts_desc[x],
				scx+190, scy-150+ip_dheight+x*25, 300,30,(50,50,50),None,13)
				ip_buttons.append(text_line)
			ip_buttons.append(inv_inst)
			ip_buttons[-1].rect.center = ip_buttons[13].rect.center 
		except:
			pass
	stats.inv_pip = True

def close_inv_pip(stats,settings,screen,ip_buttons):
	if stats.inv:
		del ip_buttons[15:]
	stats.inv_pip = False
	screen.fill(settings.bg_colour)
			
def check_events(	settings, screen, stats, buttons, ig_buttons, 
					lp_buttons, ip_buttons, loots):
	"""Respond to keyboard and mouse events"""
	
	#create variables for screen center
	scx = settings.screen_width/2
	scy = settings.screen_height/2
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(	event, settings, screen, stats, 
									loots, lp_buttons, ip_buttons)		
		#elif event.type == pygame.KEYUP:
			#check_keyup_events(event, settings, screen, stats)	
		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			mouse_pos = pygame.mouse.get_pos()
			check_buttons(	settings, screen, stats, buttons, 
							ig_buttons, lp_buttons, ip_buttons, loots, mouse_pos)
			if not stats.loot_pip or stats.inv_pip:
				for i,loot in enumerate(loots):
					if loot.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
						loot_pip(settings,screen,stats,lp_buttons,scx,scy,loot,i)
						break
			elif stats.loot_pip and not stats.inv_pip:
				if not lp_buttons[0].rect.collidepoint(mouse_pos):
					close_loot_pip(stats,lp_buttons)
				
def update_screen(	settings, screen, stats, buttons, ig_buttons, 
					lp_buttons, ip_buttons, player, loots):
	"""Update images on the screen and flip to the new screen"""

	#Redraw the screen during each pass through the loop
	screen.fill(settings.bg_colour)
	
	#Draw the menu button if the game is inactive
	if not stats.game_active:
		for i in buttons:
			i.draw_button()
	#draw ingame menus while the game is active
	if stats.game_active:
		for i in loots:
			i.blitme()
		player.blitme()
		for i in ig_buttons:
			i.draw_button()
		if stats.loot_pip:
			for i in lp_buttons:
				try:
					i.draw_button()
				except:	
					i.blitme()
		elif stats.inv_pip:
			if len(stats.inv)>11:
				len_inv = 11
			else:
				len_inv = len(stats.inv)
			for i in ip_buttons[:len_inv+1]:
				i.draw_button()
			for i in ip_buttons[12:]:
				try:
					i.draw_button()
				except:	
					i.blitme()
				
					
	#Make the most recently drawn screen visible
	pygame.display.flip()
	
