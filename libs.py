from random import randint,choice
import pygame
from pygame.sprite import Sprite
#list of possible loot qualities
qualities = (				('shoddy ',0.5), 
							('cheapo ',0.75),
							('lousy ',0.9),
							('dated ',1.), 
							('passable ',1.05),
							('regular ',1.1),
							('impressive ',1.2), 
							('top notch ',1.5), 
							('special edition ',2), 
							('luxury ',3))
		
		#list of possible loot conditions
conditions = (				('junk ',0.2),
							('ruined ',0.3),
							('busted ',0.4),
							('dented ',0.5),
							('scratched ',0.6),
							('scuffed ',0.7),
							('lightly used ',0.8), 							
							('refurbished ',0.9),
							('new ',1.0),
							('polished ',1.2))
							
							
		#list of possible 'hard' metals, for cooking and what have you					
metals = ( 					['Tin ',13,(172,182,192),7.2], 
							['Copper ',4.4,(255,120,0),8.9],
							['Brass ',6.5,(218,165,32),8.5], 
							['Iron ',1.,(128,128,128),6.8],		
							['Steel ',1.2,(192,192,192),8.05],
							['Carbon Steel ',1.5,(108,118,128),7.85],
							['Stainless Steel ',2.8,(176,196,222),7.5],
							['Aluminium ',1.5,(206,228,233),2.8],
							['Bronze ',1.2,(223,158,92),8.2], 
							['Magnesium ',4.5,(203,203,203),1.7],
							['Zinc ',1.7,(184,202,216),7.1],
							['Titanium ',21,(145,159,163),4.5],
							['Platinum ',3024,(114,109,124),21.4],
							['Palladium ',16300,(215,226,232),12],
							['Silver ',480,(199,215,220),10.5], 
							['Gold ',39000,(255,210,48),19.32])
		
woods = (					['Ashwood ',0.8,(234,194,103),0.54], 
							['Basswood ',1.3,(226,208,175),0.4],
							['Beech ',0.8,(234,168,91),0.8], 
							['Birch ',1.3,(209,190,135),0.67],	
							['Butternut ',2.0,(199,134,42),0.38],		
							['Cherry ',1.2,(175,114,63),0.63],
							['Cedar ',0.3,(225,142,56),0.38],
							['Elm ',0.8,(195,164,132),0.56],
							['Hickory ',1.3,(166,110,68),0.83], 
							['Lauan ',1.1,(128,101,77),0.85],
							['Mahogany ',4.0,(151,44,15),0.65], 
							['Maple ',1.8,(230,209,153),0.68],		
							['Oak ',1.4,(187,166,108),0.75],
							['Pecan ',1.9,(205,159,113),0.77],
							['Poplar ',0.6,(225,214,173),0.42],
							['Pine ',0.42,(231,192,103),0.42], 
							['Redwood ',0.9,(147,55,0),0.45],
							['Rosewood ',1.7,(101,42,7),0.9], 
							['Satinwood ',1.6,(220,176,30),0.95],		
							['Sycamore ',0.8,(240,211,167),0.5],
							['Teak ',5.2,(180,90,29),0.98],
							['Walnut ',1.8,(101,59,31),0.5])
				
plastics = (				['PET ',4.0,(138,201,134),0.46], 
							['HDPE ',3.0,(255,255,255),0.97], 
							['PVC ',1.2,(255,255,255),0.83],
							['LDPE ',1.0,(255,255,255),0.91], 
							['Polypropylene ',2.75,(255,255,255),0.95],	
							['Polystyrene ',3.25,(255,255,255),0.8],		
							['Styrofoam ',3,(255,255,255),0.03],
							['ABS ',2.5,(255,255,255),1],
							['Acrylic ',3.25,(255,255,255),1.2],
							['Polycarbonate ',3.5,(255,255,255),1.2],
							['Acetal ',5,(255,255,255),1.41])
							
rubbers = ( 				['Lineoleum ',0.8,(241,231,188),1.2], 
							['Neoprene ',1.1,(0,0,0),1.2], 
							['Silicone ',3,(255,255,255),1.1],
							['Natural ',.8,(0,0,0),0.93], 
							['Latex ',0.8,(241,231,188),0.9])
							
ceramics = (				['Glass ',1.5,(169,196,211),2.4], 
							['Earthenware ',3,(157,54,32),2], 
							['Stoneware ',4,(222,202,189),2.1],
							['Porcelain ',15.,(238,236,211),2.4], 
							['Cement ',.8,(164,164,164),2.9],	
							['Fire Clay ',11,(163,135,130),2],
							['Red Clay ',2,(194,98,79),1.7],	
							['Terracotta ',6,(214,90,71),1.8])
									
fibres = (					['Silk ',75,(255,255,255),1.3], 
							['Cotton ',5,(255,255,255),1.5], 
							['Wool ',8,(255,255,255),1.3],
							['Hemp ',6,(177,183,115),1.5], 	
							['Jute ',7,(196,146,94),1.4],
							['Nylon ',3,(255,255,255),1.1],	
							['Polyester ',2,(255,255,255),1.4],	
							['Acrylic ',2,(255,255,255),1.2],		
							['Sinew ',1,(224,197,164),0.8],
							['Human Hair ',0.5,(0,0,0),1.5],
							['Cat Felt ',1.5,(0,0,0),1.5],
							['Dog Felt ',1.5,(0,0,0),1.3],		
							['Leather ',30,(165,156,132),0.86],
							['Angora Felt ',20,(0,0,0),1.2])
							
papers = (					['Card Paper ',2,(182,139,97),1.5], 	
							['Bond Paper ',2,(255,255,255),1.5],
							['Corrugated Card Board ',3,(182,139,97),1.5],	
							['Poster Paper ',4,(255,255,255),1.5],	
							['Wax Paper ',4,(255,255,255),1.5])
							
fluids = (					['Water ',0.01,(129,240,255),1],
							['Liquid Detergent ',2,(129,240,255),1.3], 
							['Dish Soap ',4,(255,255,255),1.1],
							['Gasoline ',1,(234,228,168),0.71],		
							['Motor Oil ',3,(165,156,132),0.9],	
							['Paint ',12,(255,255,255),0.92],
							['Paint Thinner ',.8,(255,255,255),0.78],
							['Mud ',0.0,(105,83,57),1.2],
							['Butane ',3,(255,255,255),0.49],
							['Propane ',2,(255,255,255),0.49])

drinks = (					['Water ',0.01,(129,240,255),1],
							['Milk ',.4,(255,255,255),1], 
							['Soda ',.1,(129,240,255),1], 
							['Wine ',10,(255,255,255),.9])

lqd_foods = (				['Water ',0.01,(129,240,255),1],
							['Vegetable Oil ',0.7,(234,228,168),0.85], 
							['Soya Sauce ',3,(129,240,255),1], 	
							['Vinegar ',0.5,(255,255,255),1])
							
pwdr_foods = (				['Flour ',.4,(255,255,255),0.59],
							['Corn Starch ',.5,(255,255,180),0.59])

soft_foods = (				['Margarine ',2,(255,255,150),0.96],
							['Butter ',3,(255,255,120),0.96])
								
naturals = (				['Bone ',0.3,(234,228,168),1.9],
							['Bone ',0.3,(234,228,168),1.9]							
							)
		
minerals = (				['Granite ',0.2,(115,113,121),2.75],
							['Marble ',15,(20,20,20),2.8])

soft_solids = (				['Cork ',3,(105,83,57),0.23],
							['Wax ',1.8,(255,255,255),0.96])

pills = (					['Pain Killer ',50,(105,83,57),1.2],
							['Flu ',30,(255,255,255),1.2],
							['Antidepressant ',30,(255,255,255),1.2],
							['Stimulant ',30,(255,255,255),1.2],
							['Lessphine ',150,(255,255,255),1.2])

solid_chems = (				['Charcoal ',0.2,(20,20,20),2.0],
							['Charcoal ',0.2,(20,20,20),2.0])
							
		#list of available paint colours					
colors = (					('red ',(200,30,30)), 				
							('blue ',(30,30,200)),				
							('olive ',(128,128,0)), 			
							('khaki ',(240,230,140)),
							('dark green ',(0,100,0)),
							('lime green ',(50,205,50)),
							('teal ',(0,128,128)),
							('indigo ',(75,0,130)),
							('purple ',(128,0,128)), 
							('deep pink ',(255,20,147)),
							('pink ', (255,192,203)), 
							('beige ',(245,245,220)),
							('orange ', (255,165,0)), 
							('yellow ',(255,255,0)),				
							('indian red ',(176,23,31)),				
							('crimson ',(220,20,60)), 			
							('light pink ',(255,182,193)),
							('pale violet ',(219,112,147)),
							('raspberry ',(135,38,87)),
							('thistle ',(238,210,238)),
							('plum ',(139,102,139)),
							('magenta ',(255,0,255)), 
							('orchid ',(209,95,238)),
							('purple ', (147,112,219)), 
							('slate blue ',(106,90,205)),
							('navy ', (0,0,128)), 
							('cornflower blue ',(100,149,237)), 				
							('steel blue ',(188,210,238)),				
							('light blue ',(173,216,230)), 			
							('cadet blue ',(142,229,238)),
							('turquoise ',(0,245,255)),
							('aquamarine ',(127,255,212)),
							('spring green ',(0,255,127)),
							('sea green ',(67,205,128)),
							('mint ',(189,252,201)), 
							('chartreuse ',(127,255,0)),
							('green yellow ', (173,255,47)), 
							('banana ',(227,207,87)),
							('goldernrod ',(255,193,37)), 
							('moccasin ',(255,228,181)))
							
		#array of available loot types
loot_types ={				1:[
							'Propane Barbecue ',
							['pbbq'],
							[["base ","sheet ",1,6,['metal'],None,None],###
							["legs ","rod ",4,3,['metal'],None,None],
							["grill ","mesh ",1,5,['metal'],None,None],
							["trays ","sheet ",2,3,['wood','plastic'],None,None],
							["lid ","sheet ",1,5,['metal'],None,None],
							["handle ","sheet ",1,.25,['metal','plastic'],None,None],
							["wheels ","sheet ",2,.5,['metal','plastic','wood'],None,None],
							["screws ","chunk ",20,0.01,['metal'],None,None],
							["Propane Tank ","loot",1,4,['metal'],"fluid",None]],
							30,['fabricators'],['patio']],
							2:[
							'Stereo ',
							['stereo'],
							[["frame ","sheet ",1,6,['plastic','metal'],None,None],###
							["grill ","mesh ",2,2,['plastic','metal'],None,None],
							["drive motor ","chunk ",1,3,['metal'],None,None],
							["handle ","rod ",1,2,['plastic','metal'],None,None],
							["guts ","chunk ",1,6,['plastic'],None,None],
							["screws ","chunk ",20,0.25,['metal','plastic'],None,None],
							["cd ","chunk ",1,.1,['plastic'],None,None]],
							4,['semiconductor'],['entertainment','electronics']],
							3:[
							'Coffee Mug ',
							['cmug'],
							[["body ","chunk ",1,1,['ceramic','plastic','metal'],None,None]],
							0.5,['glassworks','fabricators','plastics'],['kitchenware','souvenirs']],
							4:[
							'T-Shirt ',
							['tshirt'],
							[["body ","roll ",1,1,['fibre'],None,None]],
							.3,['garment'],['clothing','souvenirs']],
							5:[
							'CD Case ',
							['cdcase'],
							[["front ","sheet ",1,1,['plastic'],None,None],
							["back ","sheet ",1,1,['plastic'],None,None]],
							.1,['plastics'],['entertainment','souvenirs']],
							6:[
							'Detergent Jug ',
							['detergent'],
							[["cap ","chunk ",1,1,['plastic'],None,None],
							["body ","sheet ",1,5,['plastic'],None,None],
							["contents ","Liquid Detergent ",1,20,['fluid'],None,None]],
							2,['plastics'],['sanitary']],
							7:[
							'Kids Shovel ',
							['kshovel'],
							[["handle ","rod ",1,1,['plastic','metal'],None,None],
							["scoop ","sheet ",1,2,['plastic','metal'],None,None],
							],
							.4,['plastics','fabricators'],['toys']],
							8:[
							'Soap Bar ',
							['soap'],
							[["body ","chunk ",1,1,['natural'],None,None]],
							.5,['soapworks'],['sanitary']],
							9:[
							'Baseball Cap ',
							['baseballcap'],
							[["cap ","sheet ",1,4,['fibre'],None,None],
							["brim ","sheet ",1,3,['plastic','fibre','paper'],None,None],
							["strap ","strip ",1,1,['plastic'],None,None]],
							.4,['garment'],['clothing','camping']],
							10:[
							'Propane Tank ',
							['ptank'],
							[["body ","sheet ",1,5,['metal'],None,None],
							["rim ","strip ",1,2,['metal'],None,None],
							["Valve ","loot ",1,2,['metal','plastic'],None,None],
							["screws ","chunk ",5,0.25,['metal','plastic'],None,None],
							["contents ","Propane ",1,30,['fluid'],None,None]],
							8,['fabricators'],['patio','camping']],
							11:[
							'Purse ',
							['purse'],
							[["body ","roll ",1,20,['fibre'],None,None],
							["latch ","chunk ",2,1,['metal'],None,None],
							["flap ","sheet ",1,8,['fibre'],None,None],
							["strap ","strap ",1,3,['fibre'],None,None]],
							2,['garment'],['clothing']],
							12:[
							'Valve ',
							['valve'],
							[["body ","chunk ",1,10,['metal','plastic'],None,None],
							["handle ","rod ",1,5,['metal','plastic'],None,None],
							["nozzle ","tube ",1,3,['metal','plastic'],None,None],
							["screws ","chunk ",2,0.25,['metal'],None,None]],
							1.5,['plastics','fabricators'],['plumbing','hardware']],
							13:[
							'Screws ',
							['screw'],
							[["body ","chunk ",10,10,['metal','plastic'],None,None]],
							.1,['fabricators','plastics'],['hardware']],
							14:[
							'2L Pop Bottle ',
							['2lpop'],
							[["body ","sheet ",1,4,['plastic'],None,None],
							["cap ","chunk ",1,1,['plastic'],None,None],
							["contents ","Soda ",1,100,['drink'],None,None]],
							2,['plastics'],['foods']],
							15:[
							'Charcoal Barbecue ',
							['bbq'],
							[["lid ","sheet ",1,4,['metal'],None,None],
							["legs ","rod ",3,2,['metal'],None,None],
							["grill ","mesh ",1,3,['metal'],None,None],
							["base ","sheet ",1,4,['metal'],None,None],
							["screws ","chunk ",10,1,['metal'],None,None],
							["contents ","Charcoal ",1,3,['solid chem'],None,None]],
							15,['fabricators'],['patio']],
							16:[
							'Jerry Can ',
							['jcan'],
							[["body ","sheet ",1,10,['metal','plastic'],None,None],
							["cap ","chunk ",1,1,['plastic','metal'],None,None],
							["spout ","tube ",1,1,['plastic','metal'],None,None],
							["contents ","Gasoline ",1,100,['fluid'],None,None]],
							12,['plastics','fabricators'],['automotive','camping']],
							17:[
							'Pain Killer Bottle ',
							['painkiller'],
							[["body ","sheet ",1,4,['plastic'],None,None],
							["cap ","chunk ",1,1,['plastic'],None,None],
							["contents ","Pain Killer ",1,100,['pills'],None,None]],
							.5,['plastics'],['medical']],
							18:[
							'Pill Bottle ',
							['pillbottle'],
							[["body ","sheet ",1,4,['plastic'],None,None],
							["cap ","chunk ",1,1,['plastic'],None,None],
							["contents ","Lessphine ",1,100,['pills'],None,None]],
							.1,['plastics'],['medical']],
							19:[
							'Scissors ',
							['scissor'],
							[["blades ","bar ",2,2,['plastic','metal'],None,None],
							["handles ","chunk ",2,1,['plastic','metal','wood'],None,None]],
							.3,['plastics','fabricators'],['stationery']],
							20:[
							'BBQ Lighter ',
							['bbqlighter'],
							[["body ","chunk ",1,10,['plastic'],None,None],
							["neck ","tube ",1,3,['metal'],None,None],
							["trigger ","chunk ",1,1,['plastic'],None,None],
							["contents ","Butane ",1,5,['fluid'],None,None]],
							.2,['plastics','fabricators'],['patio','stationery']],
							21:[
							'Bowl ',
							['bowl'],
							[["body ","chunk ",1,1,['metal','plastic','ceramic','wood','mineral','rubber'],None,None]],
							.2,['plastics','fabricators','carpentry','glassworks','masonry'],['kitchenware','pet supplies']],
							22:[
							'Classic Book ',
							['classicbook'],
							[["covers ","sheet ",2,1,['paper'],None,None],
							["pages ","sheet ",[100,500,0],10,['paper'],None,None]],
							.5,['printers'],['publishers']],
							23:[
							'Cookie Tin ',
							['cookietin'],
							[["tin ","sheet ",1,5,['metal'],None,None],
							["lid ","sheet ",1,1,['metal'],None,None],
							["contents ","Lessphine ",1,30,['pills'],None,None]],
							.8,['fabricators'],['foods']],
							24:[
							'Dish Soap Bottle ',
							['dishsoap'],
							[["body ","sheet ",1,4,['plastic'],None,None],
							["nozzle ","chunk ",1,1,['plastic'],None,None],
							["contents ","Dish Soap ",1,100,['fluid'],None,None]],
							.9,['plastics'],['kitchenware','sanitary']],
							25:[
							'Margarine Tub ',
							['margarine'],
							[["body ","sheet ",1,4,['plastic'],None,None],
							["lid ","chunk ",1,1,['plastic'],None,None],
							["contents ","Margarine ",1,100,['soft food','pwdr food'],None,None]],
							1.2,['plastics'],['foods']],
							26:[
							'Measuring Cup ',
							['measurecup'],
							[["body ","chunk ",1,1,['plastic','metal','ceramic'],None,None]],
							.4,['plastics','fabricators','glassworks'],['kitchenware']],
							27:[
							'Muffin Tin ',
							['muffintin'],
							[["body ","chunk ",1,1,['metal'],None,None]],
							.3,['fabricators'],['kitchenware']],
							28:[
							'Nil-Gene Bottle ',
							['nalgene'],
							[["body ","sheet ",1,4,['plastic'],None,None],
							["cap ","chunk ",1,1,['plastic'],None,None],
							["contents ","Water ",1,50,['drink'],None,None]],
							1.2,['plastics'],['camping','kitchenware']],
							29:[
							'Noodle Cup ',
							['noodlecup'],
							[["body ","sheet ",1,4,['paper','plastic'],None,None],
							["lid ","sheet ",1,1,['paper','plastic'],None,None],
							["contents ","Pain Killer ",1,200,['pills'],None,None]],
							.2,['paper','plastics'],['foods']],
							30:[
							'Patio Chair ',
							['patiochair'],
							[["seat ","sheet ",1,5,['plastic','metal','wood'],None,None],
							["legs ","bar ",4,4,['plastic','metal','wood'],None,None],
							["back ","sheet ",1,3,['plastic','metal','wood'],None,None],
							["screws ","chunk ",2,0.25,['metal','plastic'],None,None]],
							6,['fabricators','plastics','carpentry'],['furniture','patio']],
							31:[
							'Patio Table ',
							['patiotable'],
							[["surface ","sheet ",1,10,['plastic','metal','wood','ceramic'],None,None],
							["legs ","bar ",4,4,['plastic','metal','wood'],None,None],
							["frame ","sheet ",1,3,['plastic','metal','wood'],None,None],
							["screws ","chunk ",2,0.01,['metal','plastic'],None,None]],
							20,['fabricators','plastics','carpentry','glassworks'],['furniture','patio']],
							32:[
							'Magazine ',
							['peepmagazine'],
							[["covers ","sheet ",2,1,['paper'],None,None],
							["pages ","sheet ",[10,50,0],10,['paper'],None,None]],
							.1,['printers'],['publishers']],
							33:[
							'Smut Novel ',
							['smutnovel'],
							[["covers ","sheet ",2,1,['paper','plastic'],None,None],
							["pages ","sheet ",[100,200,0],10,['paper','plastic'],None,None]],
							.3,['printers'],['publishers']],
							34:[
							'Soy Bottle ',
							['soybottle'],
							[["body ","chunk ",1,4,['plastic','ceramic'],None,None],
							["lid ","chunk ",1,1,['plastic'],None,None],
							["contents ","Soya Sauce ",1,200,['lqd food','drink'],None,None]],
							.3,['plastics','glassworks'],['foods','kitchenware']],
							35:[
							'Toaster ',
							['toaster'],
							[["body ","sheet ",3,6,['metal'],None,None],
							["base ","bar ",1,5,['metal','plastic'],None,None],
							["element ","wire ",1,2,['metal'],None,None],
							["cable ","wire ",1,2,['metal'],None,None],
							["spring ","wire ",10,1,['metal'],None,None]],
							2.5,['fabricators'],['kitchenware','appliance','electronics']],
							36:[
							'Water Bottle ',
							['waterbottle'],
							[["body ","chunk ",1,4,['plastic',],None,None],
							["cap ","chunk ",1,1,['plastic'],None,None],
							["contents ","Water ",1,100,['drink'],None,None]],
							.9,['plastics'],['foods']],
							37:[
							'Wine Bottle ',
							['wine1','wine2'],
							[["body ","chunk ",1,1,['plastic','ceramic'],None,None],
							["stopper ","chunk ",1,1,['plastic','rubber','soft solid'],None,None],
							["contents ","Wine ",1,80,['drink'],None,None]],
							1.5,['glassworks','plastics'],['spirits','foods']]
							}
	
		#list of material categories
mat_cats = (			'metal','wood','plastic','rubber','ceramic',
						'fibre','paper','fluid','drink','lqd food','pwdr food',
						'soft food','natural','mineral','soft solid',
						'pills','solid chem')
		
		#list of standard weights for weigth baseline calculation
std_w={					'metal':(8.05,metals,'metal'),
						'wood':(0.5,woods,'wood'),
						'plastic':(0.9,plastics,'plastic'),
						'rubber':(1.1,rubbers,'rubber'),
						'ceramic':(2.5,ceramics,'ceramic'),
						'fibre':(1.3,fibres,'fibre'),
						'paper':(1.5,papers,'paper'),
						'fluid':(1,fluids,'fluid'),
						'drink':(1,drinks,'drink'),
						'lqd food':(1,lqd_foods,'lqd food'),
						'pwdr food':(.59,pwdr_foods,'pwdr food'),
						'soft food':(.96,soft_foods,'soft food'),
						'natural':(1,naturals,'natural'),
						'mineral':(2.75,minerals,'mineral'),
						'soft solid':(0.8,soft_solids,'soft solid'),
						'pills':(0.8,pills,'pills'),
						'solid chem': (0.8,solid_chems,'solid chem')}
		
		#list of possible material shapes 
shapes = {				'metal':(	'Threaded Rod','Bar','Tube','Wire',
									'Square Tube','T-Slot Extrusion','Pin',
									'Sheet','Expanded Sheet','Angle Bar',
									'Mesh','Strip','Chunk','I-Beam','Peg'),
						'wood':(	'Dowel','Plank','Board','Trim',
									'Scrap','Beam','Sawdust','Log','Branch'),
						'plastic':(	'Rod','Bar','Sheet','Strip','Tube','Hose',
									'Chunk','Beam','Pellets','Mesh'),
						'rubber':(	'Hose','Wire','Sheet','Gasket',
									'Mesh','Strip','Chunk'),
						'ceramic':(	'Tile','Brick','Strip','Fragment',
									'Scrap','Powder','Slab','Shard'),
						'fibre':(	'Thread','Yarn','Sheet','Strip',
									'Rope','Strap','Roll','Ribbon'),
						'paper':(	'Sheet','Tube','Confetti'),
						'fluid':(	'Liquid'),
						'drink':(	'Liquid'),
						'lqd food':('Liquid'),
						'pwdr food':('Powder','Powder'),
						'soft food':('Chunk','Slab','Bar','Chunk'),
						'natural':(	'Scrap','Chunk'),
						'mineral':(	'Chunk','Powder','Pebble','Slab'),
						'soft solid':(	'Scrap','Chunk'),
						'pills':	(	'Capsules','Tablets','Pills'),
						'solid chem':(	'Chunk', 'Powder', 'Pebble', 
										'Slab')
						}
									
		#dictionary of image sets for parts
part_sprites = {			'Rod':['rod'],
							'Bar':['bar'],
							'I-Beam':['ibeam'],
							'Mesh':['mesh'],
							'Sheet':['sheet'],
							'Chunk':['chunk'],
							'Threaded Rod':['rod'],
							'Tube':['rod'],
							'Wire':['wire'],
							'Square Tube':['squarebar'],
							'T-Slot Extrusion':['t-extrude'],
							'Pin':['dowel'],
							'Expanded Sheet':['mesh'],
							'Angle Bar':['ibeam'],
							'Beam':['ibeam'],
							'Strip':['strip'],
							'Peg':['rod'],
							'Dowel':['dowel'],
							'Plank':['board'],
							'Board':['board'],
							'Trim':['trim'],
							'Scrap':['chunk'],
							'Sawdust':['sawdust'],
							'Log':['log'],
							'Branch':['branch'],
							'Pellets':['pellet'],
							'Tile':['tile'],
							'Brick':['brick'],
							'Powder':['powder'],
							'Slab':['slab'],
							'Shard':['shard'],
							'Fragment':['fragment'],
							'Thread':['spool'],
							'Roll':['roll'],
							'Yarn':['yarn'],
							'Rope':['spool'],
							'Strap':['strip'],
							'Ribbon':['strip'],
							'Confetti':['confetti'],
							'Pebble':['pebble'],
							'Gasket':['gasket'],
							'Hose':['hose'],
							'Tablets':['pellet'],
							'Capsules':['confetti'],
							'Pills':['pellet']
							}
		
									
		#list of materials which can be dyed
dyed = ['plastic','rubber','fibre','paper','ceramic','pills','wood']
