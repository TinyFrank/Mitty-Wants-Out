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
from maps import Hood

def place_loot(settings, screen, stats, loots):
	debug_init = gen_init
	debug_init[0]='loot'
	#debug_init[2]= 'Bar'
	debug_init[3]=37
	#debug_init[7]= 1.0
	#debug_init[9]=['Gold ',80,(255,210,48),19.32]
	#debug_init[10]=['Gold ',80,(255,210,48),19.32]
	#instantiate one loot
	#loot_inst = Loot(settings, screen, stats.loot_val,debug_init) 
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
				xhits = 0
				yhits = 0
				if i.rect.colliderect(loot_inst.rect):
					#xhits=1
				#w_avg = (i.rect.width + loot_inst.rect.width)/2
				#if ((abs(i.rect.x-loot_inst.rect.x)*0.5) > w_avg):
					#print(str(abs(i.rect.x-loot_inst.rect.x)) + ' is less than ' +str(w_avg))
					#yhits=1
				#if xhits and yhits:
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
	
def check_keydown_events(	event, settings, screen, stats, loots, 
							lp_buttons, ip_buttons,hoods):
	"""Respond to keypresses"""
	if event.key == pygame.K_q:
		if not stats.loot_pip:
			sys.exit()
		else:
			close_loot_pip(stats,lp_buttons)
	elif event.key == pygame.K_m:
		#toggle map pip
		if stats.map_pip == True:
			stats.map_pip = False
		elif stats.map_pip == False and len(hoods)> 0:
			stats.map_pip = True
	#elif event.key == pygame.K_k:
		##place_loot(settings, screen, stats, loots)
		#hoods[0].grow_hood(100)
		#hoods[0].tiles = []
		#hoods[0].roll_rects()
	elif event.key == pygame.K_i:
		if not stats.inv_pip:
			inv_pip(settings,screen,stats,ip_buttons)
		else:
			close_inv_pip(stats,settings,screen,ip_buttons)
	elif event.key == pygame.K_l:
		#create/destroy debug hood
		if stats.map_pip == True:
			stats.map_pip = False
			del hoods[0]
		if stats.map_pip == False:
			d_hood = Hood(settings,screen,stats)
			d_hood.grow_hood(1)
			d_hood.roll_rects()
			hoods.append(d_hood)
			stats.map_pip = True
	elif stats.inv_pip:
		if event.key == pygame.K_ESCAPE: 
			close_inv_pip(stats,settings,screen, ip_buttons)
		elif event.key == pygame.K_i:
			close_inv_pip(stats,settings,screen,ip_buttons)
		elif event.key == pygame.K_UP or event.key == pygame.K_w:
			if not stats.scrolldown:
				stats.scroll_inv_up()
				close_inv_pip(stats,settings,screen,ip_buttons)
				inv_pip(settings,screen,stats,ip_buttons)	
				stats.scrollup = True
		elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
			if not stats.scrollup:
				stats.scroll_inv_down()
				close_inv_pip(stats,settings,screen,ip_buttons)
				inv_pip(settings,screen,stats,ip_buttons)	
				stats.scrolldown = True
	elif stats.loot_pip:
		if event.key == pygame.K_ESCAPE:
			close_loot_pip(stats,lp_buttons)
		elif event.key == pygame.K_e:
			take_loot(stats,loots,lp_buttons)			
	elif event.key == pygame.K_c:
		#debug, place_loot(settings, screen, stats, loots)
		stats.sort_inv_name()
	elif event.key == pygame.K_f:
		#debug, create a shit load of loot
		for i in range(0,200):
			place_loot(settings, screen, stats, loots)
	elif event.key == pygame.K_g:
		#debug, put all loot into inventory
		while True:
			try:
				stats.inv.append(loots.pop(-1))
			except:
				break	
				
def check_keyup_events(	event,settings, screen, stats,loots, 
						lp_buttons, ip_buttons, hoods):
	"""Respond to keyreleases"""	
	if stats.inv_pip:
		if event.key == pygame.K_UP or event.key == pygame.K_w:
			stats.scrollup = False
			stats.su_timer = stats.s_time
		elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
			stats.scrolldown = False
			stats.sd_timer = stats.s_time

def check_buttons(	settings, screen, stats, buttons, ig_buttons, 
					lp_buttons, ip_buttons, loots, mouse_pos, player):
	"""Start new game when player clicks Play"""
	scx = settings.screen_width/2
	scy = settings.screen_height/2
	if not stats.game_active:
		if buttons[0].rect.collidepoint(mouse_pos[0], mouse_pos[1]):
			stats.game_active=True
		elif  buttons[1].rect.collidepoint(mouse_pos[0], mouse_pos[1]):
			sys.exit()
	
	elif stats.game_active:
		if stats.loot_pip:
			if lp_buttons[2].rect.collidepoint(mouse_pos[0], mouse_pos[1]):
				take_loot(stats,loots,lp_buttons)
			else:
				close_loot_pip(stats,lp_buttons)
		elif stats.inv_pip and not stats.loot_pip:
			if not ip_buttons[0].rect.collidepoint(mouse_pos[0], mouse_pos[1]):
				close_inv_pip(stats,settings,screen,ip_buttons)
		elif not stats.loot_pip and not stats.inv_pip:
			for i,loot in enumerate(loots):
				if loot.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
					player.dest = mouse_pos
					player.dest_ref = i
					break	
		elif ig_buttons[0].rect.collidepoint(mouse_pos[0], mouse_pos[1]):
			inv_pip(settings,screen,stats,ip_buttons)
		elif ig_buttons[4].rect.collidepoint(mouse_pos[0], mouse_pos[1]):
			stats.game_active=False
		else:
			player.dest = mouse_pos
			
				
def loot_pip(settings,screen,stats,lp_buttons,scx,scy,loot,i):	
	stats.inv_pip = False
	stats.map_pip = False
	loot_inst = Loot(	settings, 
						screen, 
						loot_val = stats.loot_val,
						init_array = loot.init_array,
						ref = i)
	loot_inst.rebuild()					
	lp_buttons.append(loot_inst)
	lp_buttons[1] = Button(	settings, screen, loot.name, scx-275, 
							scy-200, 550,50,(0,0,0),None,18)
							
	for x in range(0,len(loot.desc)):
		text_line = Button(settings, screen, loot.desc[x],
		scx+10, scy-55+x*25, 230,30,(0,0,0),None,14)
		lp_buttons.append(text_line)
		
	lp_buttons[6].rect.center = lp_buttons[4].rect.center 
	stats.loot_pip = True	

def close_loot_pip(stats,lp_buttons):
	#delete alll buttons related to this loot
	del lp_buttons[6:]
	#turn off the loot pip
	stats.loot_pip = False
	
def inv_pip(settings,screen,stats,ip_buttons):
	stats.map_pip = False
	stats.loot_pip = False
	scx = settings.screen_width/2
	scy = settings.screen_height/2
	if stats.inv:
		inv_inst = Loot(	settings, 
						screen, 
						loot_val = stats.loot_val,
						init_array = stats.inv[stats.inv_scroll].init_array,)
						
		inv_inst.rebuild()
		first6 = len(stats.inv)
		
		if first6 > 11:
			first6 = 11
			
		for i in range(0,first6):
			index = i + stats.inv_scroll
			if index >= len(stats.inv):
				index -= len(stats.inv)
			ip_buttons[1+i].msg = stats.inv[0+index].name
			ip_buttons[1+i].prep_msg()
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
					lp_buttons, ip_buttons, loots, hoods, player):
	"""Respond to keyboard and mouse events"""
	
	#create variables for screen center
	scx = settings.screen_width/2
	scy = settings.screen_height/2
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(	event, settings, screen, stats, 
									loots, lp_buttons, ip_buttons, hoods)		
		elif event.type == pygame.KEYUP:
			check_keyup_events(		event, settings, screen, stats,
									loots, lp_buttons, ip_buttons, hoods)	
		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			mouse_pos = pygame.mouse.get_pos()
			check_buttons(	settings, screen, stats, buttons, 
							ig_buttons, lp_buttons, ip_buttons, loots, 
							mouse_pos, player)
				
def update_screen(	settings, screen, stats, buttons, ig_buttons, 
					lp_buttons, ip_buttons, player, loots, hoods):
	"""Update images on the screen and flip to the new screen"""
	scx = settings.screen_width/2
	scy = settings.screen_height/2
	#update menus
	if stats.inv_pip:
			if stats.scrollup:
				if stats.su_timer == 0:
					stats.scroll_inv_up()
					close_inv_pip(stats,settings,screen,ip_buttons)
					inv_pip(settings,screen,stats,ip_buttons)	
				else:
					stats.su_timer -= 1
			elif stats.scrolldown:
				if stats.sd_timer == 0:
					stats.scroll_inv_down()
					close_inv_pip(stats,settings,screen,ip_buttons)
					inv_pip(settings,screen,stats,ip_buttons)	
				else:
					stats.sd_timer -= 1
	#Redraw the screen during each pass through the loop
	screen.fill(settings.bg_colour)
	
	#Draw the menu button if the game is inactive
	if not stats.game_active:
		for i in buttons:
			i.draw_button()
	#draw ingame menus while the game is active
	if stats.game_active:
		player.update()
		for i,loot in enumerate(loots):
			if loot.rect.colliderect(player.rect):
				if i == player.dest_ref:
					player_dest = [0,0]
					player_dest[0] = player.rect.x+int(player.rect.width/2)
					player_dest[1] = player.rect.y+int(player.rect.height/2)
					player.dest = player_dest
					loot_pip(settings,screen,stats,lp_buttons,scx,scy,loot,i)
					player.dest_ref = None
					break	
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
		if stats.inv_pip:
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
				
		if stats.map_pip == True:
			if hoods:
				hoods[0].draw_hood()
				
					
	#Make the most recently drawn screen visible
	pygame.display.flip()
	
