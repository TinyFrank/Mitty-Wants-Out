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

def place_loot(	settings, screen, stats, loots, brands, retailers, mfrs):
	"""create a new piece of loot"""
	
	debug_init = gen_init
	debug_init[0]='loot'
	#debug_init[2]= 'Bar'
	#debug_init[3]=16
	#debug_init[7]= 1.0
	#debug_init[9]=['Gold ',80,(255,210,48),19.32]
	#debug_init[10]=['Gold ',80,(255,210,48),19.32]
	#debug_init[23] = retailers[0]
	#debug_init[24] = mfrs[0]
	#instantiate one loot
	loot_inst = Loot(	settings, screen, stats.loot_val,gen_init,
						brands=brands,mfrs=mfrs) 
	#loot_inst = Loot(settings, screen, stats.loot_val,brands=brands) 
	loot_inst.construct()
	locate_loot(settings, screen, stats, loot_inst, loots)
	
def locate_loot(	settings, screen, stats, loot_inst, loots):
	"""find a location for a new loot inst that doesnt collide with others
	already on screen"""
	
	placed = False
	timeout=0
	while not placed:
		x = randint(50,screen.get_width()-50)
			#pick random x inside screen
		y = randint(150,screen.get_height()-50) 
			#pick random y inside screen
		loot_inst.rect.x = x - (loot_inst.rect.width/2)
		loot_inst.rect.y = y - (loot_inst.rect.height/2)
			#centre rect on this random coord
		loot_inst.collide_rect.bottom = loot_inst.rect.bottom
		loot_inst.collide_rect.x = loot_inst.rect.x
			#align collision rect with image rect
		
		hits = check_for_hits(loot_inst,loots)
					
		if not hits:
			loots.append(loot_inst)
				#add this inst to the loots list
			loots.sort(key = lambda x: x.rect.y)
				#re-sort the list by y coord to place inst at the right depth
			placed = True
			
		timeout+=1
		if timeout > 50:
			placed = True
		
		loots.sort(key=lambda loot: loot.rect.bottom)	

def check_for_hits(	loot_inst,loots):
	"""check a loot_inst for collisions against other insts in a loots list"""
	
	hits = 0
	for i in loots:
		if i.collide_rect.colliderect(loot_inst.collide_rect):
			hits=1
	return(hits)
			
def take_loot(	stats,loots,lp_buttons):
	"""delete the original loot from the loots list and add a copied 
	loot to mitty's inventory"""
	
	stats.inv.append(lp_buttons[6])
	del loots[lp_buttons[6].ref]	
	
	close_loot_pip(stats,lp_buttons)
	
def check_keydown_events(	event, settings, screen, stats, loots, 
							lp_buttons, ip_buttons,mp_buttons,hoods,
							brands, retailers, mfrs):
	"""Respond to keypresses"""
	
	if event.key == pygame.K_q:
		#quit game
		if not (stats.loot_pip or stats.inv_pip):
			sys.exit()
			
	if event.key == pygame.K_m:
		#toggle map pip
		if stats.map_pip == True:
			stats.map_pip = False
		elif stats.map_pip == False and len(hoods)> 0:
			close_inv_pip(stats,settings,screen,ip_buttons)
			close_loot_pip(stats,lp_buttons)
			stats.map_pip = True
		elif stats.map_pip == False:
			close_inv_pip(stats,settings,screen,ip_buttons)
			close_loot_pip(stats,lp_buttons)
			stats.map_pip = True
			
	elif event.key == pygame.K_k:
		#debug - grow hood
		if hoods:
			hoods[0].grow_hood(100)
			hoods[0].tiles = []
			hoods[0].roll_rects()
			if stats.watched_hh:
				update_whh(settings, screen, stats, mp_buttons)
			
	elif event.key == pygame.K_i:
		#toggle inv pip
		if not stats.inv_pip:
			inv_pip(settings,screen,stats,ip_buttons)
		else:
			close_inv_pip(stats,settings,screen,ip_buttons)
				
	elif stats.inv_pip:
		#check inventory hotkeys
		check_inv_keys(	event, settings, screen, stats, loots, 
							lp_buttons, ip_buttons,mp_buttons,hoods,
							brands, retailers, mfrs)
				
	elif stats.loot_pip:
		#check loot pip hotkeys
		check_loot_keys(	event, settings, screen, stats, loots, 
							lp_buttons, ip_buttons,mp_buttons,hoods,
							brands, retailers, mfrs)

	elif stats.map_pip:
		#check map pip hotkeys
		check_map_keys(	event, settings, screen, stats, loots, 
							lp_buttons, ip_buttons,mp_buttons,hoods,
							brands, retailers, mfrs)
		
	elif event.key == pygame.K_f:
		#debug, create a (f)uck load of loot
		for i in range(0,20):
			place_loot(	settings, screen, stats, loots, brands, retailers,
						mfrs)
			
	elif event.key == pygame.K_g:
		#debug, (g)et all loot into inventory
		while True:
			try:
				stats.inv.append(loots.pop(-1))
			except:
				break	
				
def check_inv_keys(	event, settings, screen, stats, loots, 
							lp_buttons, ip_buttons,mp_buttons,hoods,
							brands, retailers, mfrs):
	"""check keys while the inv pip is active"""

	if event.key == pygame.K_ESCAPE: 
		close_inv_pip(stats,settings,screen, ip_buttons)
		
	elif event.key == pygame.K_i:
		close_inv_pip(stats,settings,screen,ip_buttons)
		
	elif event.key == pygame.K_q:
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

def check_loot_keys(	event, settings, screen, stats, loots, 
							lp_buttons, ip_buttons,mp_buttons,hoods,
							brands, retailers, mfrs):
	"""check keys while the loot pip is active"""
	
	if event.key == pygame.K_ESCAPE:
		close_loot_pip(stats,lp_buttons)
		
	if event.key == pygame.K_q:
		close_loot_pip(stats,lp_buttons)
		
	elif event.key == pygame.K_e:
		take_loot(stats,loots,lp_buttons)	

def check_map_keys(	event, settings, screen, stats, loots, 
							lp_buttons, ip_buttons,mp_buttons,hoods,
							brands, retailers, mfrs):
	"""check keys while the map pip is active"""
	
	if event.key == pygame.K_l:
		#create/destroy debug hood
		stats.map_pip = False
		if len(hoods) > 0:
			del hoods[0]
		roll_hood(settings,screen,stats,mp_buttons,hoods)
		stats.map_pip = True	

def roll_hood(	settings,screen,stats,mp_buttons,hoods):
	"""roll a new hood"""
	
	d_hood = Hood(settings,screen,stats)
	mp_buttons[1].msg = d_hood.name
	mp_buttons[1].prep_msg()
	d_hood.grow_hood(10)
	d_hood.seed_hq()
	d_hood.roll_rects()
	hoods.append(d_hood)
											
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
					brands, mfrs, mouse_pos, player,hoods):
	"""React to mouse clicks on buttons"""
	
	scx = settings.screen_width/2
	scy = settings.screen_height/2
	
	if not stats.game_active:
		check_main_menu_buttons(stats, buttons, mouse_pos)
		#check for clicks on the main menu

	elif stats.loot_pip:
		check_loot_pip_buttons(stats, loots, lp_buttons, mouse_pos)
		#check for clicks in the loot pip
		
	elif stats.inv_pip and not stats.loot_pip:
		check_inv_pip_buttons(	stats, settings, loots, ip_buttons, 
								screen, mouse_pos)
		#check for clicks in the inv pip
			
	elif stats.map_pip:
		check_map_pip_buttons(	hoods, mouse_pos, stats, mp_buttons, 
								settings, screen, loots, brands, 
								retailers, mfrs)
		#check for clicks in the map pip
		
	elif ig_buttons[4].rect.collidepoint(mouse_pos[0], mouse_pos[1]):
		stats.game_active=False
												
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
	
def check_main_menu_buttons(	stats, buttons, mouse_pos):
	"""react to mouse clicks in the main menu"""
	
	if buttons[0].rect.collidepoint(mouse_pos[0], mouse_pos[1]):
		stats.game_active=True
	elif  buttons[1].rect.collidepoint(mouse_pos[0], mouse_pos[1]):
		sys.exit()	

def check_loot_pip_buttons(	stats, loots, lp_buttons, mouse_pos):
	"""react to mouse clicks inside loot pip"""
	
	if lp_buttons[2].rect.collidepoint(mouse_pos[0], mouse_pos[1]):
		take_loot(stats,loots,lp_buttons)
	else:
		close_loot_pip(stats,lp_buttons)

def check_inv_pip_buttons(	stats, settings,  loots, ip_buttons, screen,  
							mouse_pos):
	"""react to mouse clicks inside the inventory pip"""
	
	if not ip_buttons[0].rect.collidepoint(mouse_pos[0], mouse_pos[1]):
		close_inv_pip(stats,settings,screen,ip_buttons)

def check_map_pip_buttons(	hoods, mouse_pos, stats, mp_buttons, 
							settings, screen, loots, brands, retailers, 
							mfrs):
	"""react to mouse clicks inside the map pip"""
	
	lot_hit = False
	click_loc = (mouse_pos[0], mouse_pos[1]) #last mouse click position
	for i in hoods[0].tiles: #cycle through each tile in active hood
		if i.rect.collidepoint(click_loc): #check for click on this tile
			if hoods[0].roadmap[i.refx][i.refy][0] == 'L':
				#if this tile is a (L)ot...
				stats.watched_hh = hoods[0].roadmap[i.refx][i.refy][2]
				#assign the clicked household to (watched_h)ouse(h)old
				stats.whhx = i.refx
				stats.whhy = i.refy
				#temporarily store coords in stats
				stats.watched_hh.x = i.refx
				stats.watched_hh.y = i.refy
				stats.watched_hh.town = hoods[0].name
				#rebuild watched_hh with coords and town name
				lot_hit = True
				update_whh(settings, screen, stats, mp_buttons)
				#update map pip to show mouse selection
				
	if not mp_buttons[0].rect.collidepoint(click_loc):
		stats.map_pip = False #close map pip if click is outside pip
		
	elif mp_buttons[5].rect.collidepoint(click_loc):
		go_to_button(	hoods, mouse_pos, stats, mp_buttons, settings, screen, 
						loots, brands, retailers, mfrs, click_loc)

	if not lot_hit:
		clear_map_pip(stats, mp_buttons)

def go_to_button(	hoods, mouse_pos, stats, mp_buttons, settings, screen, 
					loots, brands, retailers, mfrs, click_loc):
	"""go to the selected household. shifts loots around and creates 
	them based on hh if hh has not yet been visited"""
	
	lot_hit = True #prevent lot info from being erased in map pip
	if stats.active_hh == stats.watched_hh:
		return None
		#ignore
	
	if not stats.active_hh:
		#clear debug loot
		for loot in loots:
			del loot
	
	stats.previous_hh = stats.active_hh
	stats.active_hh = stats.watched_hh
	
	for prole in stats.active_hh.proles:
		prole.roll_favs(retailers)
	#pop loots back into whh loot list
	if stats.previous_hh:
		while True:
			try:
				stats.previous_hh.yard_loot.append(loots.pop())
			except:
				break
				
	#check for existing yard loot
	if not stats.active_hh.yard_loot:
		cap = round((randint(10,50)/10000)*stats.active_hh.hh_value,2)
		stats.active_hh.yl_cap = cap
		while True:
			#roll = randint(1,3)
			roll = 1
			prole = choice(stats.active_hh.proles)
			if roll == 1:
				#print('pick by mat...')
				pick_by_mat(	prole, settings, screen, stats, loots, 
								brands, mfrs, stats.active_hh)
				
			elif roll == 2:
				#print('pick by brand...')
				pick_by_brand(	prole, settings, screen, stats, loots, 
								brands, mfrs, stats.active_hh)
				
			elif roll == 3:
				#print('pick by color...')
				pick_by_color(	prole, settings, screen, stats, loots, 
								brands, mfrs, stats.active_hh)
						
			if stats.active_hh.yl_tally > stats.active_hh.yl_cap:
				break
			elif len(loots) > settings.yard_loot_cap:
				break
			
	elif stats.active_hh.yard_loot:
		while True:
			try:
				loots.append(stats.active_hh.yard_loot.pop())
			except:
				break

def adjust_qc(	prole, loot_inst, gain):
		"""adjust the quality and condition of a loot to coincide with
		the specific prole who fumbled it. gain is a number, 1 or more, 
		which determines how far the final q/c is from the prole's q/c"""
		
		q_offset = choice(range(-gain,gain+1))
		c_offset = choice(range(-gain,gain+1))
		
		loot_inst.quality_num = prole.quality + q_offset
		if loot_inst.quality_num > len(libs.qualities):
			loot_inst.quality_num = len(libs.qualities)
		elif loot_inst.quality_num < 0:
			loot_inst.quality_num = 0
		loot_inst.quality = libs.qualities[loot_inst.quality_num-1]
		
		loot_inst.condition_num = prole.condition + c_offset
		if loot_inst.condition_num > len(libs.conditions):
			loot_inst.condition_num = len(libs.conditions)
		elif loot_inst.condition_num < 0:
			loot_inst.condition_num = 0
		loot_inst.condition = libs.conditions[loot_inst.condition_num-1]
		
		loot_inst.roll_value()
		loot_inst.roll_name()
		loot_inst.roll_desc()
		loot_inst.rebuild()
		
def pick_by_mat(	prole, settings, screen, stats, loots, brands, mfrs, 
					active_hh):
	"""pick by fav material"""
	
	roll =1
	done = False
	while not done:
		#decide which material is wanted (pick)
		pick = choice(prole.fav_mats)
		pick_cat = ''
		for cat in libs.mat_cats:
			if pick in libs.std_w[cat][1]:
				pick_cat = cat
				#pick_cat now holds the category of the working material
		init = gen_init
		init[9] = pick
		init[0] = 'loot'
		loot_inst = Loot(	settings, screen, stats.loot_val,init,
							brands=brands,mfrs=mfrs)
		loot_inst.construct()
		
		if pick_cat in loot_inst.parts[loot_inst.largest][4]:
			"""if the material categrory is viable for the largest part 
			of this loot instance..."""
			loot_inst.parts[loot_inst.largest][6] = pick
			loot_inst.material = pick
			loot_inst.mat_cat = pick_cat
			loot_inst.source = pick_cat
			loot_inst.roll_brand()
			loot_inst.roll_mfr()
			loot_inst.roll_value()
			loot_inst.roll_name()
			loot_inst.roll_desc()
			loot_inst.roll_parts_desc()
			loot_inst.roll_image()
			loot_inst.rebuild()
			adjust_qc(	prole, loot_inst, 1)
			print('active_hh = ' + str(active_hh.qualities) + ' & ' + str(active_hh.conditions))
			print('active_hh = ' + str(prole.quality) + ' & ' + str(prole.condition))
			print('active_hh = ' + str(loot_inst.quality_num) + ' & ' + str(loot_inst.condition_num))
			print('\n')
			done=fumble_in_yard(roll, prole, stats, settings, screen, 
							loot_inst, loots)
		init[9] = None
		
def pick_by_brand(	prole, settings, screen, stats, loots, brands, mfrs, 
					active_hh):
	"""pick by fav brand"""
	
	roll = 2
	done = False
	while not done:
		init = gen_init
		init[0] = 'loot'
		#create a new loot inst by passing only this prole's brands
		loot_inst = Loot(	settings, screen, stats.loot_val,init,
							brands=prole.fav_brands,mfrs=mfrs)
		loot_inst.construct()
		#print(str(loot_inst.l_type[0]) + ' from ' + str(loot_inst.brand.name))
		#if loot_inst.brand in prole.fav_brands:
			#print('this is one of ' + prole.fname + "'s favourite brands")
		#else:
			#print(str(prole.fname).upper() + "DOESN'T LIKE THIS BRAND!!!!")
		done = fumble_in_yard(	roll, prole, stats, settings, screen, 
								loot_inst, loots)
		
def pick_by_color(	prole, settings, screen, stats, loots, brands, mfrs, 
					active_hh):
	"""pick by fav color"""
	
	roll = 3
	done = False
	while not done:
		init = gen_init
		#init[18] = choice(prole.fav_colors)
		init[0] = 'loot'
		loot_inst = Loot(	settings, screen, stats.loot_val,init,
							brands=brands,mfrs=mfrs)
		loot_inst.construct()
		if loot_inst.is_dyeable():
			loot_inst.color = choice(prole.fav_colors)
			loot_inst.roll_name()
			loot_inst.roll_desc()
			loot_inst.roll_image()
			loot_inst.rebuild()
			#for color in prole.fav_colors:
				#print(color[0])
			#print(loot_inst.color[0].upper()+'\n')
			done = fumble_in_yard(	roll, prole, stats, settings, screen, 
									loot_inst, loots)
		
def fumble_in_yard(	roll, prole, stats, settings, screen, loot_inst, 
					loots):
	"""fumble - maybe he catches it, maybe it falls.
	this is how we determine which loots land in the yard!"""
	
	temp_val = stats.active_hh.yl_tally+loot_inst.value
	cap_buffer = stats.active_hh.yl_cap*1.2
	if (temp_val < cap_buffer):
		stats.active_hh.yl_tally += loot_inst.value
		#narrate_choice(roll, loot_inst, prole)
		locate_loot(settings, screen, stats,loot_inst, loots)
		return(True)
	else:
		return(False)

def narrate_choice(	roll, loot_inst, prole):
	"""print a debug narration string to console"""
	
	narrative = '\n'+str(roll)+': '+prole.fname+prole.lname
	narrative += ' left a '+loot_inst.name+' from '+loot_inst.brand.name
	narrative += ' in the yard.'
	narrative += "\nIt was purchased for it's "
	f_mats = []
	f_brands = []
	f_colors = []
	for x in prole.fav_mats:
		f_mats.append(x[0])
	for x in prole.fav_brands:
		f_brands.append(x.name)
	for x in prole.fav_colors:
		f_colors.append(x[0])
	if roll == 1:
		narrative += 'material.('+str(f_mats)+')'
	elif roll == 2:
		narrative += 'brand.('+str(f_brands)+')'
	elif roll == 3:
		narrative += 'color.('+str(f_colors)+')'
	print(narrative)	
			
def clear_map_pip(	stats, mp_buttons):
	"""delete all mp_buttons beyond 6 (which held temp information
	for the currently selected lot) and rewrite all buttons before 6 to
	and empty string"""
	
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
				
def update_whh(	settings, screen, stats, mp_buttons):
	"""update the watched household buttons in the map pip"""
	
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
			
def loot_pip(	settings,screen,stats,lp_buttons,scx,scy,loot,i):	
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

def close_loot_pip(	stats,lp_buttons):
	#delete alll buttons related to this loot
	del lp_buttons[6:]
	#turn off the loot pip
	stats.loot_pip = False
	
def inv_pip(	settings,screen,stats,ip_buttons):
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

def close_inv_pip(	stats,settings,screen,ip_buttons):
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
							mfrs, mouse_pos, player, hoods)

def blit_depths(	player, loots):
	"""blit mitty and other items at the correct depth"""
	
	blits = []
	blits[1:1] = loots
	blits.append(player)
	blits.sort(key=lambda x: x.rect.y+x.rect.height)	
	for i in blits:
		i.blitme()	
				
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
		player.update(loots)
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
			
		blit_depths(player, loots)
			
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
	
