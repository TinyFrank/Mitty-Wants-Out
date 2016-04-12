import sys
from time import sleep
from random import randint
import json
from player import Player
from loot import *
import pygame
import copy
import libs
from button import Button
import math
from maps import Hood

def place_loot(settings, screen, stats, loots, brands, retailers, mfrs):
	debug_init = gen_init
	debug_init[0]='loot'
	#debug_init[2]= 'Bar'
	#ebug_init[3]=34
	#debug_init[7]= 1.0
	#debug_init[9]=['Gold ',80,(255,210,48),19.32]
	#debug_init[10]=['Gold ',80,(255,210,48),19.32]
	debug_init[23] = retailers[0]
	#debug_init[24] = mfrs[0]
	#instantiate one loot
	loot_inst = Loot(settings, screen, stats.loot_val,gen_init,brands=brands) 
	#loot_inst = Loot(settings, screen, stats.loot_val,brands=brands) 
	loot_inst.construct()
	locate_loot(settings, screen, stats, loot_inst, loots)
	
def locate_loot(settings, screen, stats, loot_inst, loots):
	
	placed = False
	timeout=0
	while not placed:
		x = randint(50,screen.get_width()-50)
		y = randint(150,screen.get_height()-50)
		loot_inst.rect.x = x - (loot_inst.rect.width/2)
		loot_inst.rect.y = y - (loot_inst.rect.height/2)
		loot_inst.collide_rect.bottom = loot_inst.rect.bottom
		loot_inst.collide_rect.x = loot_inst.rect.x
		hits = 0
		if loots:
			for i in loots:
				xhits = 0
				yhits = 0
				if i.collide_rect.colliderect(loot_inst.collide_rect):
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
		
		loots.sort(key=lambda loot: loot.rect.bottom)	

def take_loot(stats,loots,lp_buttons):
	#delete original loot from the loot pile
	#add coppied loot to inventory
	stats.inv.append(lp_buttons[6])
	del loots[lp_buttons[6].ref]	
	
	close_loot_pip(stats,lp_buttons)
	
def check_keydown_events(	event, settings, screen, stats, loots, 
							lp_buttons, ip_buttons,mp_buttons,hoods,
							brands, retailers, mfrs):
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
			close_inv_pip(stats,settings,screen,ip_buttons)
			close_loot_pip(stats,lp_buttons)
			stats.map_pip = True
			
	elif event.key == pygame.K_k:
		#debug - grow hood
		hoods[0].grow_hood(100)
		hoods[0].tiles = []
		hoods[0].roll_rects()
		if stats.watched_hh:
			update_whh(settings, screen, stats, mp_buttons)
			
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
		elif stats.map_pip == False:
			d_hood = Hood(settings,screen,stats)
			mp_buttons[1].msg = d_hood.name
			mp_buttons[1].prep_msg()
			d_hood.grow_hood(10)
			d_hood.seed_hq()
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
		elif event.key == pygame.K_z:
			#sort inv by value
			close_inv_pip(stats,settings,screen,ip_buttons)
			stats.inv = sorted(stats.inv, key=lambda item: item.value)
			inv_pip(settings,screen,stats,ip_buttons)		
		elif event.key == pygame.K_c:
			#sort inv by name
			close_inv_pip(stats,settings,screen,ip_buttons)
			stats.inv = sorted(stats.inv, key=lambda item: item.quality[1])
			inv_pip(settings,screen,stats,ip_buttons)	
		elif event.key == pygame.K_b:
			#sort inv by name
			close_inv_pip(stats,settings,screen,ip_buttons)
			stats.inv = sorted(stats.inv, key=lambda item: item.brand.name)
			inv_pip(settings,screen,stats,ip_buttons)
				
	elif stats.loot_pip:
		if event.key == pygame.K_ESCAPE:
			close_loot_pip(stats,lp_buttons)
		elif event.key == pygame.K_e:
			take_loot(stats,loots,lp_buttons)
		
	elif event.key == pygame.K_f:
		#debug, create a shit load of loot
		for i in range(0,200):
			place_loot(	settings, screen, stats, loots, brands, retailers,
						mfrs)
			
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
					lp_buttons, ip_buttons, mp_buttons, loots, retailers,
					brands,	mouse_pos, player,hoods):
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
		elif stats.map_pip:
			lot_hit = False
			for i in hoods[0].tiles:
				if i.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
					if hoods[0].roadmap[i.refx][i.refy][0] == 'L':
						stats.watched_hh = hoods[0].roadmap[i.refx][i.refy][2]
						stats.whhx = i.refx
						stats.whhy = i.refy
						stats.watched_hh.x = i.refx
						stats.watched_hh.y = i.refy
						stats.watched_hh.town = hoods[0].name
						lot_hit = True
						update_whh(settings, screen, stats, mp_buttons)
						print(stats.watched_hh.lname)
			if not mp_buttons[0].rect.collidepoint(mouse_pos[0], mouse_pos[1]):
				stats.map_pip = False
			elif mp_buttons[5].rect.collidepoint(mouse_pos[0], mouse_pos[1]):
				lot_hit = True
				if stats.active_hh == stats.watched_hh:
					return None
				#go to the Current HouseHold
				if not stats.active_hh:
					#clear debug loot
					for loot in loots:
						del loot
				
				stats.previous_hh = stats.active_hh
				stats.active_hh = stats.watched_hh
				print('active is ' + stats.active_hh.lname)
				for prole in stats.active_hh.proles:
					prole.roll_favs(retailers)
				#pop loots back into whh loot list
				while True:
					try:
						stats.previous_hh.yard_loot.append(loots.pop())
					except:
						break
				#check for existing yard loot
				if not stats.active_hh.yard_loot:
					cap = round((randint(10,50)/10000)*stats.active_hh.hh_value,2)
					stats.active_hh.yl_cap = cap
					print('household vlaue is ' + str(stats.active_hh.hh_value))
					print(' cap has been set at $' + str(cap))
					while True:
						roll = randint(1,3)
						roll = 1
						#print('rolled a ' + str(roll))
						prole = choice(stats.active_hh.proles)
						if roll == 1:
							#pick by fav material
							count=100
							while True:
								pick = choice(prole.fav_mats)
								pick_cat = ''
								for cat in libs.mat_cats:
									if pick in libs.std_w[cat][1]:
										pick_cat = cat
										#pick_cat now holds the category of the working material
								init = gen_init
								init[9] = pick
								init[0] = 'loot'
								loot_inst = Loot(settings, screen, stats.loot_val,init,brands=brands)
								loot_inst.construct()
								legit = False
								if loot_inst.raw == 'loot':
									if pick_cat in loot_inst.parts[loot_inst.largest][4]:
										loot_inst.parts[loot_inst.largest][6] = pick
										loot_inst.material = pick
										loot_inst.mat_cat = pick_cat
										loot_inst.source = pick_cat
										loot_inst.roll_mfr()
										loot_inst.roll_value()
										loot_inst.roll_name()
										loot_inst.roll_desc()
										loot_inst.roll_parts_desc()
										legit = True
								if loot_inst.raw == 'part':
									loot_inst.material = pick
									loot_inst.mat_cat = pick_cat
									loot_inst.roll_shape()
									loot_inst.roll_industry()
									loot_inst.roll_value()
									loot_inst.roll_name()
									loot_inst.roll_desc()
									legit = True
								temp_val = stats.active_hh.yl_tally+loot_inst.value
								cap_buffer = stats.active_hh.yl_cap*1.2
								if (temp_val < cap_buffer) and legit:
									stats.active_hh.yl_tally += loot_inst.value
									locate_loot(settings, screen, stats,loot_inst, loots)
									print('sent material: ' + pick[0])
									#print('got something made from '+pick[0]+' by '+loot_inst.mfr.name)
									print('got '+loot_inst.name+'\n\n')
									break
								count -= 1
								if count < 1:
									break
						if roll == 2:
							#pick by fav brand
							while True:
								init = gen_init
								init[0] = 'loot'
								loot_inst = Loot(settings, screen, stats.loot_val,init,brands=prole.fav_brands)
								loot_inst.construct()
								if (stats.active_hh.yl_tally+loot_inst.value) < (stats.active_hh.yl_cap*1.2):
									#print('value is kosher!')
									if loot_inst.brand in prole.fav_brands:
										stats.active_hh.yl_tally += loot_inst.value
										locate_loot(settings, screen, stats,loot_inst, loots)
										print('got something from '+loot_inst.brand.name)
										break
								prole_brands = []
								for i in prole.fav_brands:
									prole_brands.append(i.name)
								print(loot_inst.brand.name + str(prole_brands))
						if roll == 3:
							#pick by fav color
							while True:
								init = gen_init
								init[18] = choice(prole.fav_colors)
								init[0] = 'loot'
								loot_inst = Loot(settings, screen, stats.loot_val,init,brands=brands)
								loot_inst.construct()
								if (stats.active_hh.yl_tally+loot_inst.value) < (stats.active_hh.yl_cap*1.2):
									stats.active_hh.yl_tally += loot_inst.value
									locate_loot(settings, screen, stats,loot_inst, loots)
									print('got something '+init[18][0])
									break
						if stats.active_hh.yl_tally > stats.active_hh.yl_cap:
							print(str(round(stats.active_hh.yl_tally,2))+' dollars in the yard')
							break
			if not lot_hit:
				stats.watched_hh = []
				mp_buttons[2].msg=''
				mp_buttons[2].prep_msg()
				mp_buttons[3].msg=''
				mp_buttons[3].prep_msg()
				mp_buttons[4].msg=''
				mp_buttons[4].prep_msg()
				mp_buttons[5].msg=''
				mp_buttons[5].prep_msg()
				del mp_buttons[6:]
													
		elif not stats.loot_pip and not stats.inv_pip:
			for i,loot in enumerate(loots):
				if loot.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
					player.dest = mouse_pos
					player.dest_ref = i
					break	
			if ig_buttons[0].rect.collidepoint(mouse_pos[0], mouse_pos[1]):
				inv_pip(settings,screen,stats,ip_buttons)
			elif player.dest_ref == None:
				player.dest = mouse_pos
		elif ig_buttons[4].rect.collidepoint(mouse_pos[0], mouse_pos[1]):
			stats.game_active=False
			
def update_whh(settings, screen, stats, mp_buttons):
	#update the Current HouseHold buttons in the map pip
	del mp_buttons[6:]	
	mp_buttons[2].msg = str(stats.watched_hh.lname) + ' Household'
	mp_buttons[2].prep_msg()
	mp_buttons[3].msg = str(stats.watched_hh.hh_value) + ' Value'
	mp_buttons[3].prep_msg()
	mp_buttons[4].msg = str(stats.watched_hh.num_proles) + ' Residents'
	mp_buttons[4].prep_msg()
	mp_buttons[5].msg = 'GO TO'
	mp_buttons[5].prep_msg()
	x = mp_buttons[5].x
	y = mp_buttons[5].y+60 
	for i in range(0,stats.watched_hh.num_proles):
		tp_fname = stats.watched_hh.proles[i].fname
		tp_age = str(stats.watched_hh.proles[i].age)
		tp_bday = str(stats.watched_hh.proles[i].bday)
		tp_salary = str(stats.watched_hh.proles[i].salary) 
		text_line = Button(settings, screen, tp_fname,
			x, y+i*25, 75,30,(0,0,0),None,15)
		mp_buttons.append(text_line)
		text_line = Button(settings, screen, tp_age,
			x+75, y+i*25, 40,30,(0,0,0),None,15)
		mp_buttons.append(text_line)
		text_line = Button(settings, screen, tp_bday,
			x+115, y+i*25, 125,30,(0,0,0),None,15)
		mp_buttons.append(text_line)
		text_line = Button(settings, screen, tp_salary,
			x+240, y+i*25, 75,30,(0,0,0),None,15)
		mp_buttons.append(text_line)
			
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
		scx+10, scy-55+x*25, 350,30,(0,0,0),None,14)
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
			scx+190, scy-160+x*25, 425,30,(0,0,0),None,15)
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
					lp_buttons, ip_buttons, mp_buttons, loots, hoods,
					brands, retailers, mfrs, player):
	"""Respond to keyboard and mouse events"""
	
	#create variables for screen center
	scx = settings.screen_width/2
	scy = settings.screen_height/2
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(	event, settings, screen, stats, 
									loots, lp_buttons, ip_buttons, 
									mp_buttons, hoods, brands, retailers,
									mfrs)		
		elif event.type == pygame.KEYUP:
			check_keyup_events(		event, settings, screen, stats,
									loots, lp_buttons, ip_buttons, hoods)	
		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			mouse_pos = pygame.mouse.get_pos()
			check_buttons(	settings, screen, stats, buttons, 
							ig_buttons, lp_buttons, ip_buttons, 
							mp_buttons, loots, retailers, brands,
							mouse_pos, player, hoods)
				
def update_screen(	settings, screen, stats, buttons, ig_buttons, 
					lp_buttons, ip_buttons, mp_buttons, 
					player, loots, hoods):
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
			for i in mp_buttons:
				i.draw_button()
			if hoods:
				hoods[0].draw_hood()
				
					
	#Make the most recently drawn screen visible
	pygame.display.flip()
	
