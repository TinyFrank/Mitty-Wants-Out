"""
Mitty Wants Out
"""
import sys 
import pygame
from pygame.sprite import Group
import json
from button import Button
from settings import Settings
import display
from stats import Stats
from player import Player
from brands import Brand,ctg_retail,ctg_industrial
import libs
import functions as gf

def run():
	#Initialize game, settings and create a screen object
	pygame.init()	
	settings = Settings()
	screen_setup = display.build(settings)
	screen = screen_setup[0]
	pygame.display.set_caption("Mitty Wants Out")
	
	#Change screen dims to match fullscreen dims
	settings.screen_width = screen_setup[1]
	settings.screen_height = screen_setup[2]
	
	#create variables for screen center
	scx = settings.screen_width/2
	scy = settings.screen_height/2
	
	#Make Main Menu
	buttons = []
	play_button = Button(settings, screen, "NEW GAME",
		scx-100, 500, 300,75,(0,0,0),None)
	quit_button = Button(settings, screen, "QUIT",
		scx-100, 600, 300,75,(0,0,0),None)
	buttons.append(play_button)
	buttons.append(quit_button)
	
	#Make Ingame Menu
	ig_buttons = []
	inv_button = Button(settings, screen, "INVENTORY",
		settings.screen_width*.2-100, 0,
		200,50,(0,0,0),None)
	craft_button = Button(settings, screen, "CRAFT",
		settings.screen_width*.35-100, 0,
		200,50,(0,0,0),None)
	build_button = Button(settings, screen, "BUILD",
		settings.screen_width/2-100, 0,
		200,50,(0,0,0),None)
	character_button = Button(settings, screen, "CHARACTER",
		settings.screen_width*.65-100, 0,
		200,50,(0,0,0),None)
	menu_button = Button(settings, screen, "MENU",
		settings.screen_width*.8-100, 0,
		200,50,(0,0,0),None)
	ig_buttons.append(inv_button)
	ig_buttons.append(craft_button)
	ig_buttons.append(build_button)
	ig_buttons.append(character_button)
	ig_buttons.append(menu_button)
	
	#Make Map PIP menu
	ms = settings.map_size
	mp_buttons = []
	mp_bg = Button(settings, screen, "",
		scx-(ms/2)-(ms/4)-10, scy-(ms/2)-10, 
		ms+(ms/2)+20,ms+20,(0,0,0),None,20)
	mp_title = Button(settings, screen, "",
		scx+(ms/4)+10, scy-(ms/2), 
		ms/2-10,100,(100,100,100),None,20)
	mp_hh = Button(settings, screen, "",
		scx+(ms/4)+10, scy-(ms/2)+110, 
		ms/2-10,40,(100,100,100),None,15)
	mp_hhinc = Button(settings, screen, "",
		scx+(ms/4)+10, scy-(ms/2)+150, 
		ms/2-10,40,(100,100,100),None,15)
	mp_num = Button(settings, screen, "",
		scx+(ms/4)+10, scy-(ms/2)+190, 
		ms/2-10,40,(100,100,100),None,15)
	mp_goto = Button(settings, screen, "",
		scx+(ms/4)+10, scy-(ms/2)+230, 
		ms/2-10,60,(100,100,100),None,20)
	mp_buttons.append(mp_bg)
	mp_buttons.append(mp_title)
	mp_buttons.append(mp_hh)
	mp_buttons.append(mp_hhinc)
	mp_buttons.append(mp_num)
	mp_buttons.append(mp_goto)
	
	
	#Make Loot PIP menu
	lp_buttons = []
	lp_title = Button(settings, screen, "",
		scx-250, scy-200, 500,50,(0,0,0),None,20)
	lptake_button = Button(settings, screen, "TAKE",
		scx+25, scy-125, 200,50,(0,0,0),None,20)
	lpdesc_button = Button(settings, screen, "",
		scx+25, scy-50, 200,175,(0,0,0),None,10)
	lp_window = Button(settings, screen, "",
		scx-275, scy-200, 670,350,(100,100,100),None)
	lp_loot_window = Button(settings, screen, "",
		scx-225, scy-125, 200,250,(180,180,180),None)
	lp_loot = Button(settings, screen, "",
		scx-215, scy-115, 180,230,(250,250,250),None)
	lp_buttons.append(lp_window)
	lp_buttons.append(lp_title)
	lp_buttons.append(lptake_button)
	lp_buttons.append(lpdesc_button)
	lp_buttons.append(lp_loot_window)
	lp_buttons.append(lp_loot)
	
	#Make Inventory PIP menu
	ip_buttons = []
	#font used by inventory list buttons 
	ip_font = 12
	ip_window = Button(settings, screen, "",
		scx-500, scy-145, 1120,290,(100,100,100),None,20)
	ip_itemt5_button = Button(settings, screen, "",
		scx-494, scy-135, 448,20,(200,0,0),None,14)
	ip_itemt5_button.font.set_bold(True)
	ip_itemt4_button = Button(settings, screen, "",
		scx-490, scy-110, 440,20,(0,0,0),None,ip_font)
	ip_itemt3_button = Button(settings, screen, "",
		scx-490, scy-85, 440,20,(0,0,0),None,ip_font)
	ip_itemt2_button = Button(settings, screen, "",
		scx-490, scy-60, 440,20,(0,0,0),None,ip_font)
	ip_itemt1_button = Button(settings, screen, "",
		scx-490, scy-35, 440,20,(0,0,0),None,ip_font)
	ip_item_button = Button(settings, screen, "",
		scx-490, scy-12, 440,24,(2,0,0),None,ip_font)
	ip_itemb1_button = Button(settings, screen, "",
		scx-490, scy+15, 440,20,(0,0,0),None,ip_font)
	ip_itemb2_button = Button(settings, screen, "",
		scx-490, scy+40, 440,20,(0,0,0),None,ip_font)
	ip_itemb3_button = Button(settings, screen, "",
		scx-490, scy+65, 440,20,(0,0,0),None,ip_font)
	ip_itemb4_button = Button(settings, screen, "",
		scx-490, scy+90, 440,20,(0,0,0),None,ip_font)
	ip_itemb5_button = Button(settings, screen, "",
		scx-490, scy+115, 440,20,(0,0,0),None,ip_font)
	ipdesc_button = Button(settings, screen, "",
		scx+225, scy-100, 200,200,(100,100,100),None,10)
	ip_loot_window = Button(settings, screen, "",
		scx-25, scy-125, 200,250,(180,180,180),None)
	ip_loot = Button(settings, screen, "",
		scx-15, scy-115, 180,230,(250,250,250),None)
	ip_buttons.append(ip_window)
	ip_buttons.append(ip_itemt5_button)
	ip_buttons.append(ip_itemt4_button)
	ip_buttons.append(ip_itemt3_button)
	ip_buttons.append(ip_itemt2_button)
	ip_buttons.append(ip_itemt1_button)
	ip_buttons.append(ip_item_button)
	ip_buttons.append(ip_itemb1_button)
	ip_buttons.append(ip_itemb2_button)
	ip_buttons.append(ip_itemb3_button)
	ip_buttons.append(ip_itemb4_button)
	ip_buttons.append(ip_itemb5_button)
	ip_buttons.append(ipdesc_button)
	ip_buttons.append(ip_loot_window)
	ip_buttons.append(ip_loot)
				
	#Create a stats instance
	stats = Stats(settings)
	
	#Create item groups
	player = Player(settings, screen)
	loots = []
	hoods = []
	brands = []
	retailers = []
	mfrs = []
	
	def generate_world_brands():
		#Generate world brands
		current_ctgs = []
		while len(current_ctgs) < (len(ctg_retail)+len(ctg_industrial)):
			brand = Brand(settings,stats)
			if brand.ctg not in current_ctgs:
				current_ctgs.append(brand.ctg)
			if brand.ri == 'retail':
				retailers.append(brand)
			if brand.ri == 'industrial':
				mfrs.append(brand)
			brands.append(brand)
			
	#Generate world brands
	generate_world_brands()
	
	#Create clock to stabilize framerate
	clock = pygame.time.Clock()
	
	#Initialize Global Variables
	day = 1
	hour = 6
	minute = 0
	
	pygame.mixer.music.load('drunkman2 4.ogg')
	pygame.mixer.music.play(-1)
	
	while True:
		clock.tick(50)
		gf.check_events(	settings, screen, stats, buttons, 
							ig_buttons, lp_buttons, ip_buttons, mp_buttons,
							loots, hoods, brands, retailers, mfrs, player)
		gf.update_screen(	settings,screen, stats, buttons, ig_buttons, 
							lp_buttons, ip_buttons, mp_buttons,
							player, loots, hoods)
run()

