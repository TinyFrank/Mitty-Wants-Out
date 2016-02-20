from random import randint,choice
import pygame
from pygame.sprite import Sprite
#list of possible loot qualities
qualities = (				('shoddy ',0.2), 
							('cheapo ',0.4),
							('lousy ',0.6),
							('dated ',0.75), 
							('passable ',0.9),
							('regular ',1.0),
							('impressive ',1.25), 
							('top notch ',1.5), 
							('special edition ',2.0), 
							('luxury ',5.0))
		
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
metals = ( 					['Tin ',0.6,(172,182,192),7.2], 
							['Copper ',1.1,(255,120,0),8.9],
							['Brass ',0.8,(218,165,32),8.5], 
							['Iron ',0.9,(128,128,128),6.8],		
							['Steel ',1.0,(192,192,192),8.05],
							['Carbon Steel ',1.5,(108,118,128),7.85],
							['Stainless Steel ',3.0,(176,196,222),7.5],
							['Aluminium ',1.5,(206,228,233),2.8],
							['Bronze ',1.2,(223,158,92),8.2], 
							['Magnesium ',4.5,(203,203,203),1.7],
							['Titanium ',7.2,(145,159,163),4.5],
							['Silver ',30,(199,215,220),10.5], 
							['Gold ',80,(255,210,48),19.32])
		
woods = (					['Ashwood ',0.6,(234,194,103),0.54], 
							['Basswood ',0.7,(226,208,175),0.4],
							['Beech ',0.8,(234,168,91),0.8], 
							['Birch ',0.9,(209,190,135),0.67],	
							['Butternut ',1.0,(199,134,42),0.38],		
							['Cherry ',1.2,(175,114,63),0.63],
							['Cedar ',0.3,(225,142,56),0.38],
							['Elm ',0.8,(195,164,132),0.56],
							['Hickory ',1.3,(166,110,68),0.83], 
							['Lauan ',1.1,(128,101,77),0.85],
							['Mahogany ',2.5,(151,44,15),0.65], 
							['Maple ',1.1,(230,209,153),0.68],		
							['Oak ',1.1,(187,166,108),0.75],
							['Pecan ',1.5,(205,159,113),0.77],
							['Poplar ',0.6,(225,214,173),0.42],
							['Pine ',0.2,(231,192,103),0.42], 
							['Redwood ',0.9,(147,55,0),0.45],
							['Rosewood ',1.2,(101,42,7),0.9], 
							['Satinwood ',1.1,(220,176,30),0.95],		
							['Sycamore ',0.8,(240,211,167),0.5],
							['Teak ',3.5,(180,90,29),0.98],
							['Walnut ',1.8,(101,59,31),0.5])
				
plastics = (				['PET ',0.3,(138,201,134),0.46], 
							['HDPE ',0.7,(255,255,255),0.97], 
							['PVC ',0.8,(255,255,255),0.83],
							['LDPE ',0.6,(255,255,255),0.91], 
							['Polypropylene ',0.5,(255,255,255),0.95],	
							['Polystyrene ',0.2,(255,255,255),0.8],		
							['Styrofoam ',0.1,(255,255,255),0.03],
							['ABS ',0.5,(255,255,255),1],
							['Acrylic ',0.6,(255,255,255),1.2],
							['Polycarbonate ',1.2,(255,255,255),1.2],
							['Acetal ',0.5,(255,255,255),1.41])
							
rubbers = ( 				['Lineoleum ',0.8,(241,231,188),1.2], 
							['Neoprene ',2,(0,0,0),1.2], 
							['Silicone ',1.2,(255,255,255),1.1],
							['Natural ',0.4,(0,0,0),0.93], 
							['Latex ',0.3,(241,231,188),0.9])
							
ceramics = (				['Glass ',0.6,(169,196,211),2.4], 
							['Earthenware ',0.5,(157,54,32),2], 
							['Stoneware ',0.4,(222,202,189),2.1],
							['Porcelain ',1.5,(238,236,211),2.4], 
							['Cement ',0.1,(164,164,164),2.9],	
							['Fire Clay ',1.0,(163,135,130),2],
							['Red Clay ',0.3,(194,98,79),1.7],	
							['Terracotta ',0.8,(214,90,71),1.8])
									
fibres = (					['Silk ',2.5,(255,255,255),1.3], 
							['Cotton ',1,(255,255,255),1.5], 
							['Wool ',1.2,(255,255,255),1.3],
							['Hemp ',1.1,(177,183,115),1.5], 	
							['Jute ',0.8,(196,146,94),1.4],
							['Nylon ',0.6,(255,255,255),1.1],	
							['Polyester ',0.2,(255,255,255),1.4],	
							['Acrylic ',0.4,(255,255,255),1.2],		
							['Sinew ',0.2,(224,197,164),0.8],
							['Hair ',0.1,(0,0,0),1.5],
							['Thatch ',0.1,(210,197,86),1.5])
							
papers = (					['Card Paper ',0.3,(182,139,97),1.5], 	
							['Bond Paper ',0.1,(255,255,255),1.5],
							['Corrugated Card Board ',0.6,(182,139,97),1.5],	
							['Poster Paper ',0.4,(255,255,255),1.5],	
							['Wax Paper ',0.5,(255,255,255),1.5])
							
fluids = (					['Water ',0.01,(129,240,255),1],
							['Milk ',0.05,(255,255,255),1], 
							['Soda ',0.01,(129,240,255),1], 
							['Gasoline ',2.0,(234,228,168),0.71],	
							['Vegetable Oil ',0.08,(234,228,168),0.85],		
							['Motor Oil ',1.0,(165,156,132),0.9],		
							['Vinegar ',0.02,(255,255,255),1],
							['Paint ',0.5,(255,255,255),0.92],
							['Paint Thinner ',0.3,(255,255,255),0.78],
							['Mud ',0.0,(105,83,57),1.2],
							['Propane ',1.5,(255,255,255),0.49])
								
naturals = (				['Bone ',0.3,(234,228,168),1.9],		
							['Leather ',2.0,(165,156,132),0.86],
							
							)
		
minerals = (				['Charcoal ',0.2,(20,20,20),2.0],
							['Charcoal ',0.2,(20,20,20),2.0])

soft_solids = (				['Cork ',0.5,(105,83,57),0.23],
							['Wax ',1.0,(255,255,255),0.96])
							
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
loot_types ={	1:[
							'Propane Barbecue ',
							'pbbq',
							[["base ","sheet ",1,6,'metal',None],
							["legs ","rod ",4,3,'metal',None],
							["grill ","mesh ",1,5,'metal',None],
							["lid ","sheet ",1,5,'metal',None],
							["screws ","chunk ",20,0.25,'metal',None],
							["Propane Tank ","loot",1,4,'metal',"fluid"]],
							30],
							2:[
							'Stereo ',
							'stereo',
							[["frame ","sheet ",1,6,'plastic',None],
							["grill ","mesh ",2,2,'plastic',None],
							["drive motor ","chunk ",1,3,'metal',None],
							["handle ","rod ",1,2,'plastic',None],
							["guts ","chunk ",1,6,'plastic',None],
							["screws ","chunk ",20,0.25,'metal',None],
							["cd ","chunk ",1,.1,'plastic',None]],
							4],
							3:[
							'Coffee Mug ',
							'cmug',
							[["body ","chunk ",1,1,'ceramic',None]],
							0.5],
							4:[
							'T-Shirt ',
							'tshirt',
							[["body ","roll ",1,1,'fibre',None]],
							.3],
							5:[
							'CD Case ',
							'cdcase',
							[["front ","sheet ",1,1,'plastic',None],
							["back ","sheet ",1,1,'plastic',None]],
							.1],
							6:[
							'Detergent Jug ',
							'detergent',
							[["cap ","chunk ",1,1,'plastic',None],
							["body ","sheet ",1,5,'plastic',None],
							["contents ","fluid",1,20,'fluid',None]],
							2],
							7:[
							'Kids Shovel ',
							'kshovel',
							[["handle ","rod ",1,1,'plastic',None],
							["scoop ","sheet ",1,2,'plastic',None],
							],
							.4],
							8:[
							'Soap Bar ',
							'soap',
							[["body ","chunk ",1,1,'natural',None]],
							.5],
							9:[
							'Baseball Cap ',
							'baseballcap',
							[["cap ","sheet ",1,4,'fibre',None],
							["brim ","sheet ",1,3,'plastic',None],
							["strap ","strip ",1,1,'plastic',None]],
							.4],
							10:[
							'Propane Tank ',
							'ptank',
							[["body ","sheet ",1,5,'metal',None],
							["rim ","strip ",1,2,'metal',None],
							["Valve ","loot ",1,2,'metal',None],
							["screws ","chunk ",5,0.25,'metal',None],
							["contents ","fluid",1,30,'fluid',None]],
							8],
							11:[
							'Purse ',
							'purse',
							[["body ","roll ",1,20,'fibre',None],
							["latch ","chunk ",2,1,'metal',None],
							["flap ","sheet ",1,8,'fibre',None],
							["strap ","strap ",1,3,'fibre',None]],
							2],
							12:[
							'Valve ',
							'valve',
							[["body ","chunk ",1,10,'metal',None],
							["handle ","rod ",1,5,'metal',None],
							["nozzle ","tube ",1,3,'metal',None],
							["screws ","chunk ",2,0.25,'metal',None]],
							1.5],
							13:[
							'Screws ',
							'screw',
							[["body ","chunk ",10,10,'metal',None]],
							.1],
							14:[
							'2L Pop Bottle ',
							'2lpop',
							[["body ","sheet ",1,4,'plastic',None],
							["cap ","chunk ",1,1,'plastic',None],
							["contents ","fluid ",1,100,'fluid',None]],
							2],
							15:[
							'Charcoal Barbecue ',
							'bbq',
							[["legs ","rod ",3,2,'metal',None],
							["grill ","mesh ",1,3,'metal',None],
							["lid ","sheet ",1,4,'metal',None],
							["base ","sheet ",1,4,'metal',None],
							["screws ","chunk ",10,1,'metal',None],
							["contents ","chunk ",1,3,'mineral',None]],
							15],
							16:[
							'Jerry Can ',
							'jcan',
							[["body ","sheet ",1,10,'metal',None],
							["cap ","chunk ",1,1,'plastic',None],
							["spout ","tube ",1,1,'plastic',None],
							["contents ","fluid ",1,100,'fluid',None]],
							12]
							}
	
		#list of material categories
mat_cats = (			'metal','wood','plastic','rubber','ceramic',
						'fibre','paper','fluid','natural','mineral',
						'soft solid')
		
		#list of standard weights for weigth baseline calculation
std_w={					'metal':(8.05,metals,'metal'),
						'wood':(0.5,woods,'wood'),
						'plastic':(0.9,plastics,'plastic'),
						'rubber':(1.1,rubbers,'rubber'),
						'ceramic':(2.5,ceramics,'ceramic'),
						'fibre':(1.3,fibres,'fibre'),
						'paper':(1.5,papers,'paper'),
						'fluid':(1,fluids,'fluid'),
						'natural':(1,naturals,'natural'),
						'mineral':(2,minerals,'mineral'),
						'soft solid':(0.8,soft_solids,'soft solid')}
		
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
									'Scrap','Powder','Plate','Shard'),
						'fibre':(	'Thread','Yarn','Sheet','Strip',
									'Rope','Strap','Roll','Ribbon'),
						'paper':(	'Sheet','Tube','Confetti'),
						'natural':(	'Scrap','Chunk'),
						'mineral':(	'Chunk','Powder','Pebble'),
						'soft solid':(	'Scrap','Chunk')}
									
		#dictionary of image sets for parts
part_sprites = {'Rod':'rod',
							'Bar':'bar',
							'I-Beam':'ibeam',
							'Mesh':'mesh',
							'Sheet':'sheet',
							'Chunk':'chunk',
							'Threaded Rod':'rod',
							'Tube':'rod',
							'Wire':'wire',
							'Square Tube':'bar',
							'T-Slot Extrusion':'bar',
							'Pin':'rod',
							'Expanded Sheet':'sheet',
							'Angle Bar':'bar',
							'Beam':'ibeam',
							'Strip':'strip',
							'Peg':'rod',
							'Dowel':'rod',
							'Plank':'board',
							'Board':'board',
							'Trim':'bar',
							'Scrap':'chunk',
							'Sawdust':'chunk',
							'Log':'mesh',
							'Branch':'mesh',
							'Pellets':'chunk',
							'Tile':'tile',
							'Brick':'brick',
							'Powder':'chunk',
							'Plate':'tile',
							'Shard':'chunk',
							'Fragment':'chunk',
							'Thread':'spool',
							'Roll':'roll',
							'Yarn':'roll',
							'Rope':'spool',
							'Strap':'strip',
							'Ribbon':'strip',
							'Confetti':'chunk',
							'Pebble':'chunk',
							'Gasket':'gasket',
							'Hose':'hose'
							}
		
									
		#list of materials which can be dyed
dyed = ['plastic','rubber','fibre','paper','ceramic']
					
class Loot(object):
	def __init__(	self,settings,screen,level=None,value=None,color=None,
					condition=None,quality=None,material=None,val_normal=None,
					ref=None,l_type=None,shape=None,parts=None,trim=None,
					den=1,num=10,raw=None,weight=None,q_num=None,val_x=None,
					alt_color=None):	
			
		#list of possible loot qualities
		self.qualities = (	('shoddy ',0.2), 
							('cheapo ',0.4),
							('lousy ',0.6),
							('dated ',0.75), 
							('passable ',0.9),
							('regular ',1.0),
							('impressive ',1.25), 
							('top notch ',1.5), 
							('special edition ',2.0), 
							('luxury ',5.0))
		
		#list of possible loot conditions
		self.conditions = (	('junk ',0.2),
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
		self.metals = ( 	['Tin ',0.6,(172,182,192),7.2], 
							['Copper ',1.1,(255,120,0),8.9],
							['Brass ',0.8,(218,165,32),8.5], 
							['Iron ',0.9,(128,128,128),6.8],		
							['Steel ',1.0,(192,192,192),8.05],
							['Carbon Steel ',1.5,(108,118,128),7.85],
							['Stainless Steel ',3.0,(176,196,222),7.5],
							['Aluminium ',1.5,(206,228,233),2.8],
							['Bronze ',1.2,(223,158,92),8.2], 
							['Magnesium ',4.5,(203,203,203),1.7],
							['Titanium ',7.2,(145,159,163),4.5],
							['Silver ',30,(199,215,220),10.5], 
							['Gold ',80,(255,210,48),19.32])
		
		self.woods = (		['Ashwood ',0.6,(234,194,103),0.54], 
							['Basswood ',0.7,(226,208,175),0.4],
							['Beech ',0.8,(234,168,91),0.8], 
							['Birch ',0.9,(209,190,135),0.67],	
							['Butternut ',1.0,(199,134,42),0.38],		
							['Cherry ',1.2,(175,114,63),0.63],
							['Cedar ',0.3,(225,142,56),0.38],
							['Elm ',0.8,(195,164,132),0.56],
							['Hickory ',1.3,(166,110,68),0.83], 
							['Lauan ',1.1,(128,101,77),0.85],
							['Mahogany ',2.5,(151,44,15),0.65], 
							['Maple ',1.1,(230,209,153),0.68],		
							['Oak ',1.1,(187,166,108),0.75],
							['Pecan ',1.5,(205,159,113),0.77],
							['Poplar ',0.6,(225,214,173),0.42],
							['Pine ',0.2,(231,192,103),0.42], 
							['Redwood ',0.9,(147,55,0),0.45],
							['Rosewood ',1.2,(101,42,7),0.9], 
							['Satinwood ',1.1,(220,176,30),0.95],		
							['Sycamore ',0.8,(240,211,167),0.5],
							['Teak ',3.5,(180,90,29),0.98],
							['Walnut ',1.8,(101,59,31),0.5])
				
		self.plastics = (	['PET ',0.3,(138,201,134),0.46], 
							['HDPE ',0.7,(255,255,255),0.97], 
							['PVC ',0.8,(255,255,255),0.83],
							['LDPE ',0.6,(255,255,255),0.91], 
							['Polypropylene ',0.5,(255,255,255),0.95],	
							['Polystyrene ',0.2,(255,255,255),0.8],		
							['Styrofoam ',0.1,(255,255,255),0.03],
							['ABS ',0.5,(255,255,255),1],
							['Acrylic ',0.6,(255,255,255),1.2],
							['Polycarbonate ',1.2,(255,255,255),1.2],
							['Acetal ',0.5,(255,255,255),1.41])
							
		self.rubbers = ( 	['Lineoleum ',0.8,(241,231,188),1.2], 
							['Neoprene ',2,(0,0,0),1.2], 
							['Silicone ',1.2,(255,255,255),1.1],
							['Natural ',0.4,(0,0,0),0.93], 
							['Latex ',0.3,(241,231,188),0.9])
							
		self.ceramics = (	['Glass ',0.6,(169,196,211),2.4], 
							['Earthenware ',0.5,(157,54,32),2], 
							['Stoneware ',0.4,(222,202,189),2.1],
							['Porcelain ',1.5,(238,236,211),2.4], 
							['Cement ',0.1,(164,164,164),2.9],	
							['Fire Clay ',1.0,(163,135,130),2],
							['Red Clay ',0.3,(194,98,79),1.7],	
							['Terracotta ',0.8,(214,90,71),1.8])
									
		self.fibres = (		['Silk ',2.5,(255,255,255),1.3], 
							['Cotton ',1,(255,255,255),1.5], 
							['Wool ',1.2,(255,255,255),1.3],
							['Hemp ',1.1,(177,183,115),1.5], 	
							['Jute ',0.8,(196,146,94),1.4],
							['Nylon ',0.6,(255,255,255),1.1],	
							['Polyester ',0.2,(255,255,255),1.4],	
							['Acrylic ',0.4,(255,255,255),1.2],		
							['Sinew ',0.2,(224,197,164),0.8],
							['Hair ',0.1,(0,0,0),1.5],
							['Thatch ',0.1,(210,197,86),1.5])
							
		self.papers = (		['Card Paper ',0.3,(182,139,97),1.5], 	
							['Bond Paper ',0.1,(255,255,255),1.5],
							['Corrugated Card Board ',0.6,(182,139,97),1.5],	
							['Poster Paper ',0.4,(255,255,255),1.5],	
							['Wax Paper ',0.5,(255,255,255),1.5])
							
		self.fluids = (		['Water ',0.01,(129,240,255),1],
							['Milk ',0.05,(255,255,255),1], 
							['Soda ',0.01,(129,240,255),1], 
							['Gasoline ',2.0,(234,228,168),0.71],	
							['Vegetable Oil ',0.08,(234,228,168),0.85],		
							['Motor Oil ',1.0,(165,156,132),0.9],		
							['Vinegar ',0.02,(255,255,255),1],
							['Paint ',0.5,(255,255,255),0.92],
							['Paint Thinner ',0.3,(255,255,255),0.78],
							['Mud ',0.0,(105,83,57),1.2],
							['Propane ',1.5,(255,255,255),0.49])
							
		self.naturals = (	['Bone ',0.3,(234,228,168),1.9],		
							['Leather ',2.0,(165,156,132),0.86],
							['Cork ',0.5,(105,83,57),0.23],
							['Wax ',1.0,(255,255,255),0.96])
		
		self.minerals = (	['Charcoal ',0.2,(20,20,20),2.0])
							
		#list of available paint colours					
		self.colors = (		('red ',(200,30,30)), 				
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
		self.loot_types ={	1:[
							'Propane Barbecue ',
							'pbbq',
							[["base ","sheet ",1,6,'metal',None],
							["legs ","rod ",4,3,'metal',None],
							["grill ","mesh ",1,5,'metal',None],
							["lid ","sheet ",1,5,'metal',None],
							["screws ","chunk ",20,0.25,'metal',None],
							["Propane Tank ","loot",1,4,'metal',"fluid"]],
							30],
							2:[
							'Stereo ',
							'stereo',
							[["frame ","sheet ",1,6,'plastic',None],
							["grill ","mesh ",2,2,'plastic',None],
							["drive motor ","chunk ",1,3,'metal',None],
							["handle ","rod ",1,2,'plastic',None],
							["guts ","chunk ",1,6,'plastic',None],
							["screws ","chunk ",20,0.25,'metal',None],
							["cd ","chunk ",1,.1,'plastic',None]],
							4],
							3:[
							'Coffee Mug ',
							'cmug',
							[["body ","chunk ",1,1,'ceramic',None]],
							0.5],
							4:[
							'T-Shirt ',
							'tshirt',
							[["body ","roll ",1,1,'fibre',None]],
							.3],
							5:[
							'CD Case ',
							'cdcase',
							[["front ","sheet ",1,1,'plastic',None],
							["back ","sheet ",1,1,'plastic',None]],
							.1],
							6:[
							'Detergent Jug ',
							'detergent',
							[["cap ","chunk ",1,1,'plastic',None],
							["body ","sheet ",1,5,'plastic',None],
							["contents ","fluid",1,20,'fluid',None]],
							2],
							7:[
							'Kids Shovel ',
							'kshovel',
							[["handle ","rod ",1,1,'plastic',None],
							["scoop ","sheet ",1,2,'plastic',None],
							],
							.4],
							8:[
							'Soap Bar ',
							'soap',
							[["body ","chunk ",1,1,'natural',None]],
							.5],
							9:[
							'Baseball Cap ',
							'baseballcap',
							[["cap ","sheet ",1,4,'fibre',None],
							["brim ","sheet ",1,3,'plastic',None],
							["strap ","strip ",1,1,'plastic',None]],
							.4],
							10:[
							'Propane Tank ',
							'ptank',
							[["body ","sheet ",1,5,'metal',None],
							["rim ","strip ",1,2,'metal',None],
							["Valve ","loot ",1,2,'metal',None],
							["screws ","chunk ",5,0.25,'metal',None],
							["contents ","fluid",1,30,'fluid',None]],
							8],
							11:[
							'Purse ',
							'purse',
							[["body ","roll ",1,20,'fibre',None],
							["latch ","chunk ",2,1,'metal',None],
							["flap ","sheet ",1,8,'fibre',None],
							["strap ","strap ",1,3,'fibre',None]],
							2],
							12:[
							'Valve ',
							'valve',
							[["body ","chunk ",1,10,'metal',None],
							["handle ","rod ",1,5,'metal',None],
							["nozzle ","tube ",1,3,'metal',None],
							["screws ","chunk ",2,0.25,'metal',None]],
							1.5],
							13:[
							'Screws ',
							'screw',
							[["body ","chunk ",10,10,'metal',None]],
							.1],
							14:[
							'2L Pop Bottle ',
							'2lpop',
							[["body ","sheet ",1,4,'plastic',None],
							["cap ","chunk ",1,1,'plastic',None],
							["contents ","fluid ",1,100,'fluid',None]],
							2],
							15:[
							'Charcoal Barbecue ',
							'bbq',
							[["legs ","rod ",3,2,'metal',None],
							["grill ","mesh ",1,3,'metal',None],
							["lid ","sheet ",1,4,'metal',None],
							["base ","sheet ",1,4,'metal',None],
							["screws ","chunk ",10,1,'metal'],
							["contents ","chunk ",1,3,'mineral',None]],
							15],
							16:[
							'Jerry Can ',
							'jcan',
							[["body ","sheet ",1,10,'metal',None],
							["cap ","chunk ",1,1,'plastic',None],
							["spout ","tube ",1,1,'plastic',None],
							["contents ","fluid ",1,100,'fluid',None]],
							12]
							}
	
		#list of material categories
		self.mat_cats = (	'metal','wood','plastic','rubber','ceramic',
							'fibre','paper','fluid','natural')
		
		#list of standard weights for weigth baseline calculation
		self.std_w={	'metal':(8.05,self.metals,'metal'),
						'wood':(0.5,self.woods,'wood'),
						'plastic':(0.9,self.plastics,'plastic'),
						'rubber':(1.1,self.rubbers,'rubber'),
						'ceramic':(2.5,self.ceramics,'ceramic'),
						'fibre':(1.3,self.fibres,'fibre'),
						'paper':(1.5,self.papers,'paper'),
						'fluid':(1,self.fluids,'fluid'),
						'natural':(1,self.naturals,'natural'),
						'mineral':(2,self.minerals,'mineral')}
		
		#list of possible material shapes 
		self.shapes = {	'metal':(	'Threaded Rod','Bar','Tube','Wire',
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
									'Scrap','Powder','Plate','Shard'),
						'fibre':(	'Thread','Yarn','Sheet','Strip',
									'Rope','Strap','Roll','Ribbon'),
						'paper':(	'Sheet','Tube','Confetti'),
						'natural':(	'Scrap','Chunk'),
						'mineral':('Chunk','Powder','Pebble'),
						'soft solid':('Chunk','Scrap')}
									
		#dictionary of image sets for parts
		self.part_sprites = {'Rod':'rod',
							'Bar':'bar',
							'I-Beam':'ibeam',
							'Mesh':'mesh',
							'Sheet':'sheet',
							'Chunk':'chunk',
							'Threaded Rod':'rod',
							'Tube':'rod',
							'Wire':'wire',
							'Square Tube':'bar',
							'T-Slot Extrusion':'bar',
							'Pin':'rod',
							'Expanded Sheet':'sheet',
							'Angle Bar':'bar',
							'Beam':'ibeam',
							'Strip':'strip',
							'Peg':'rod',
							'Dowel':'rod',
							'Plank':'board',
							'Board':'board',
							'Trim':'bar',
							'Scrap':'chunk',
							'Sawdust':'chunk',
							'Log':'mesh',
							'Branch':'mesh',
							'Pellets':'chunk',
							'Tile':'tile',
							'Brick':'brick',
							'Powder':'chunk',
							'Plate':'tile',
							'Shard':'chunk',
							'Fragment':'chunk',
							'Thread':'spool',
							'Roll':'roll',
							'Yarn':'roll',
							'Rope':'spool',
							'Strap':'strip',
							'Ribbon':'strip',
							'Confetti':'chunk',
							'Pebble':'chunk',
							'Gasket':'gasket',
							'Hose':'hose'
							}
		
									
		#list of materials which can be dyed
		self.dyed = ['plastic','rubber','fibre','paper','ceramic']
		
		self.spritepath = "images/"
		self.raw = raw
		self.level = level
		self.l_type = l_type
		self.settings = settings
		self.screen = screen
		self.weight = weight
		self.value = value
		self.color = color
		self.shape = shape
		self.condition = condition
		self.quality = quality
		self.material = material
		self.ref = ref
		self.trim = trim
		self.parts = parts
		self.num = num
		self.den = den
		self.alt_color = alt_color
		self.sha_forbid = []
		self.qua_forbid = []
		self.mat_forbid = []
		self.col_forbid = []
		self.con_forbid = []
		self.typ_forbid = []		
		self.val_x = val_x
		self.weight = weight
		self.val_normal = val_normal
		self.short_name='uninitialized'
		self.construct()
	def construct(self):
		if not self.raw:
			self.raw = choice(['part','loot'])	
		if self.raw ==	'part':
			self.construct_part()
		elif self.raw ==	'loot':
			self.construct_loot()
			
	def construct_loot(self):
		#pick a loot type if none was given
		if not self.l_type:	
			self.specify_l_type()
		self.specify_short_name()
		self.specify_sprite()
		self.specify_quality()
		self.specify_condition()
		self.specify_color()
		self.specify_mat()
		self.include_parts()
		self.specify_trim()
		self.specify_value()
		self.compose_name()	
		self.compose_desc()
		self.roll_image()
		self.create_rects()	
	def specify_l_type(self):
		if not self.l_type:
			while True:
				self.l_type = randint(1,len(self.loot_types))	
				if self.l_type not in self.typ_forbid:
					break
		
	def set_images(self):
		#compose image from source and alter based on qual/mat/color
		"""
		Loads in the three images(Dirt, Line and Material) that are
		used to generate the procedural graphic.
		The material layer is full of coloured fragments and is used
		twice; once in the bottom layer for MAT and again in the second
		from top layer for COL. Each time it's colours are changed to 
		match that of the chosen paint and material. In the case of the
		paint, some of the fragments are made transparent to reveal
		the material layer below.
		"""
		self.image_dirt = pygame.image.load('images/' + self.sprite[0])
		self.image_dirt.convert_alpha()
		self.image_line = pygame.image.load('images/' + self.sprite[1])
		self.image_line.convert_alpha()
		self.image_mat = pygame.image.load('images/' + self.sprite[2])
		self.image_mat.convert_alpha()
		
		#num of colour layers in 'M' palette
		self.layers = (len(self.image_mat.get_palette())) 
		
		#set number of dents based on condition
		self.dents=0
		for i,con in enumerate(self.conditions):
			if con == self.condition:
				self.dents = len(self.conditions)-i
				self.con_num = i
				
		#apply the dents by make paint fragments transparent	
		if self.dents == len(self.conditions):
			for i in range(self.layers):
				self.image_mat.set_palette_at(i,self.material[2])
		elif self.dents == 0:
			for i in range(self.layers):
				self.image_mat.set_palette_at(i,self.color[2]) 
			
		else:	
			for i in range(1,self.layers-1):
				if self.dents:
					self.image_mat.set_palette_at(i,self.material[2])
					self.dents -= 1
				else:
					self.image_mat.set_palette_at(i,self.color[1])
				
		#pick an alpha between 0 and 255 based on condition number		
		self.alpha = (self.con_num * 51)-25
		if self.alpha > 255:
			self.alpha = 255
		if self.alpha < 0:
			self.alpha = 0
		self.alpha = 255 - self.alpha
		
	def blit_alpha(self,target, source, location, opacity):
		"""
		workaround to blit a pixel-alpha containing surface at an
		opacity other than 100
		"""
		self.x = location[0]
		self.y = location[1]
		self.temp = pygame.Surface((source.get_width(), source.get_height())).convert()
		self.temp.blit(target, (-self.x, -self.y))
		self.temp.blit(source, (0, 0))
		self.temp.set_alpha(opacity)        
		target.blit(self.temp, location)	
        
	def blitme(self):
		"""Draw the loot at it's current location."""
		self.screen.blit(self.image_mat,self.rect) #Color (Paintjob)
		try:
			self.screen.blit(self.image_trim,self.rect) #Trim (Paintjob)
		except:
			pass
		try:
			self.screen.blit(self.image_col,self.rect) #Colored Labels
		except:
			pass
		self.screen.blit(self.image_line,self.rect) #Line art
		try:
			#dirt layer
			self.blit_alpha(self.screen,self.image_dirt,self.rect,self.alpha)
		except:
			pass
	
	def specify_quality(self):
		"""if no quality was specified, select one randomly"""
		if not self.quality:
			while True:
				self.q_num = randint(0,len(self.qualities)-1)
				if self.q_num not in self.qua_forbid:
					self.quality = self.qualities[self.q_num]
					break
	
	def specify_mat(self):
		"""specify a primary material if none was given"""
		if not self.material:
			self.mat_cat=self.loot_types[self.l_type][2][0][4]
			self.material = choice(self.std_w[self.mat_cat][1])
	
	def specify_condition(self):
		"""define a state-of-repair or 'conditon' if none was given"""
		if not self.condition:
			while True:
				ct = randint(0,len(self.conditions)-1)
				if ct not in self.con_forbid:
					self.condition = self.conditions[ct]
					break
						
	def specify_color(self):
		"""specify color if none was given"""
		if not self.color:
			while True:
				self.ct = randint(0,len(self.colors)-1)
				if self.ct not in self.col_forbid:
					self.color = self.colors[self.ct]
					break
	
	def specify_trim(self):
		"""specify trim if none was given"""
		if not self.trim:
			if len(self.parts)>1:
				self.trim = self.parts[1][-1]
				self.trim_cat = self.parts[1][4]
			
				if self.trim_cat in self.dyed:
					self.trim[2] = choice(self.colors)
					self.trim_color = self.trim[2][0]
					self.trim[2] = self.trim[2][1]
			
	def include_parts(self):
		""""
		this very busy function first calls specify_parts() to pull down
		a list of parts from this loot's dictionary entry, so long
		as this is not already done.
		
		'parts' contains a list of lists, each one representing a part
		from which the loot is built. Each part prototype come with a 
		[0]name, [1]material form factor, [2]quantity, [3]relative 
		contribution to total value/weight, [5]material type and an 
		optional [6]th var which represents materials stored in this 
		part.
		
		As an example, there are 3 'legs' that contribute 2 to the overall
		mass, while the 10 'screws' only contribute 1. The legs are 
		metal 'rod' material whil the screws are metal 'chunks'. 
		
		The 'num'erator and 'den'ominator define the probability that 
		a part will get trim. ex. (10,3) gives a 30% for any given part.
		"""
		#get weight and parts from loot_types dictionary
		if not self.parts:
			self.specify_parts()
			self.weight = self.loot_types[self.l_type][3]
			
			#figure out what the standard weight ought to be
			self.trial_w = 0
			for part in self.parts:
				self.trial_w += part[2]*part[3]*self.std_w[part[4]][0]
			self.w_x = self.weight / self.trial_w
			#calculate a weigth factor based on the quotient above
			for part in self.parts:
				part[3] *= self.w_x		
			#for each part...
			if len(self.parts[0])<6:
				for num,i in enumerate(self.parts):
					#chance to change the material to different material
					if num == 0:
						i.append(self.material)
					elif randint(0,self.num) > self.den:
						while True:
							sel = randint(0,len(self.std_w[i[4]][1])-1)
							if sel not in self.mat_forbid:
								self.mat_cat=self.std_w[i[4]][1]
								i.append(self.mat_cat[sel])
								break
					else:
						i.append(self.material)
			
			
		self.desc_parts()	
	
	def desc_parts(self):
		self.val_x=0
		self.val_normal=0
		self.parts_desc = []
		for n,i in enumerate(self.parts):
			#val_x is the part contribtuion(i[3]) * material value
			self.val_x += i[3]*i[-1][1]
			#val_normal is the sum of all the part contributions
			self.val_normal += i[3]
			#create a final factor by dividing the contribution back out
			self.val_x /= self.val_normal
			self.weight+=i[2]*i[3]*i[-1][3]
			self.parts_desc.append(str(i[2]))
			self.parts_desc[n]+=' '+str(i[-1][0])
			self.parts_desc[n]+=' '+str(i[0])
		self.weight = round(self.weight-self.loot_types[self.l_type][3],2)
	def specify_value(self):
		if not self.value:
			self.value = self.level * 20 #cost of a 'new, steel' bbq IRL, for balancing
			self.value *= self.quality[1]
			self.value *= self.val_x
			self.value *= self.weight
			self.value = round(self.condition[1]*self.value,2)
	def compose_name(self):
		#compose name
		self.name = self.quality[0].title() + self.material[0] + self.short_name
			
	def compose_desc(self):
		#compose descriptive string for Loot PIP
		self.desc = []
		self.desc.append("Material: " + self.material[0].upper())
		try:
			self.desc.append("Trim: " + self.trim[0].upper())
		except:
			self.desc.append("Trim: N/A")
		self.desc.append("Quality: " + self.quality[0].upper())
		try:
			self.desc.append("Shape: " + self.shape.upper())
		except:
			self.desc.append("Shape: N/A")
		try:
			self.desc.append("Condition: " + self.condition[0].upper())
		except:
			self.desc.append("Condition: N/A")
		try:
			self.desc.append("Color: " + self.color[0].upper())
		except:
			self.desc.append("Color: N/A")
		self.desc.append("Value: $" + str(round(self.value,2)))
		self.desc.append("Weight: " + str(self.weight).upper() + 'kg')
		
	def create_rects(self):
		#create rects
		self.rect = self.image_line.get_rect()
		self.rect.inflate(-10,-10)
		self.rect.normalize()
		self.collide_rect = self.rect.copy()
		self.screen_rect = self.screen.get_rect()
		self.collide_rect.inflate(-10,-10)
		self.collide_rect.normalize()
	
	def specify_parts(self):
		self.parts = self.loot_types[self.l_type][2]
	
	def specify_sprite(self):
		self.sprite = self.loot_types[self.l_type][1]
		
	def specify_short_name(self):
		if self.raw == 'loot':
			self.short_name = self.loot_types[self.l_type][0]
		elif self.raw == 'part':
			self.short_name = self.material[0]

	def construct_part(self):
		self.roll_weight()
		if self.shape and not self.material:
			self.roll_material()
		elif self.material and not self.shape:
			self.roll_shape()
		elif not self.material and not self.shape:
			self.roll_material()
			self.roll_shape()
		self.specify_quality()
		self.name = ''
		self.roll_name()
		self.specify_short_name()
		self.roll_value()
		self.compose_desc()
		self.roll_sprite()
		self.roll_image()
		self.create_rects()

	def roll_weight(self):
		if not self.weight:
			self.weight	= round((self.level**2)*(randint(0,400)/100),2)
		
	def roll_material(self):
		if not self.material:
			self.mat_cat = 'fluid'
			while self.mat_cat == 'fluid':
				self.mat_cat = self.mat_cats[randint(0,len(self.mat_cats)-1)]
			self.material = choice(self.std_w[self.mat_cat][1])
		
			if self.mat_cat in self.dyed:
				self.ct = randint(0,len(self.colors)-1)
				self.color =  self.colors[self.ct]
				self.material[2] = self.colors[self.ct][1]
			
			self.alt_color = choice(self.colors)
			
	def roll_shape(self):
		if not self.shape:
			self.shape = choice(self.shapes[self.mat_cat])
		
	def roll_name(self):
		if not self.name:
			if self.color:
				if (self.color[0] != 'N/A') and (self.color[0]!= self.material[0]):
					self.name = self.color[0].title()
			else:
				self.name = ''
		self.name += self.material[0]			
		self.name += self.shape + ' '
	
	def roll_value(self):
		if self.value:
			return None 
		if not self.value:
			self.value = round(self.level*self.weight*self.material[1],2)
	def roll_sprite(self):
		self.sprite = self.part_sprites[self.shape]
						
	def roll_image(self):
		self.image_line = pygame.image.load(self.spritepath+"L_" + str(self.sprite)+'.png')
		self.image_line.convert_alpha()
		
		self.image_mat = pygame.image.load(self.spritepath+"M_" + str(self.sprite)+'.png')
		self.image_mat.convert_alpha()
			
		self.layers = (len(self.image_mat.get_palette()))
	
		for i in range(0,self.layers-1):
			self.x_color = self.image_mat.get_palette_at(i)
			if not self.color:
				self.color = ['N/A',[0,0,0,0]]
				self.color[1] = self.material[2]
				self.color[0] = self.material[0]
			self.grey_offset = -(self.x_color[0]-127)
			self.n_color = [self.color[1][0]+self.grey_offset,
							self.color[1][1]+self.grey_offset,
							self.color[1][2]+self.grey_offset]
			self.n_color2=[0,0,0]
			for num,rgbint in enumerate(self.n_color):
				if rgbint>255:
					self.n_color2[num]=255
				elif rgbint<0:
					self.n_color2[num]=0
				elif 0<rgbint<256:
					self.n_color2[num]=rgbint
					
			self.n_color=(self.n_color2[0],self.n_color2[1],self.n_color2[2])
			self.image_mat.set_palette_at(i,self.n_color2)
		
		try:	
			self.image_trim = pygame.image.load('images/M2_' + str(self.sprite)+'.png')
			self.image_trim.convert_alpha()	
			self.layers = len(self.image_trim.get_palette())
			
			for i in range(0,self.layers-1):
				self.x_color = self.image_trim.get_palette_at(i)
				self.color2 = ['N/A',[0,0,0,0]]
				if not self.trim:
					if self.color[1] == self.material[2]:
						self.color2[1] = self.alt_color[1]
					elif self.color[1] != self.material[2]:
						self.color2[1] = self.material[2]
						self.color2[0] = self.material[0]
				elif self.trim:
					self.color2[1] = self.trim[2]
					self.color2[0] = self.trim[0]
				self.grey_offset = -(self.x_color[0]-127)
				self.n_color = [self.color2[1][0]+self.grey_offset,
								self.color2[1][1]+self.grey_offset,
								self.color2[1][2]+self.grey_offset]
				self.n_color2=[0,0,0]
				for num,rgbint in enumerate(self.n_color):
					if rgbint>255:
						self.n_color2[num]=255
					elif rgbint<0:
						self.n_color2[num]=0
					elif 0<rgbint<256:
						self.n_color2[num]=rgbint
						
				self.n_color=(self.n_color2[0],self.n_color2[1],self.n_color2[2])
				print(self.n_color)
				self.image_trim.set_palette_at(i,self.n_color)
				
		except:
			pass
		
		try:	
			self.image_col = pygame.image.load('images/C_' + str(self.sprite)+'.png')
			self.image_col.convert_alpha()	
			
			self.layers = len(self.image_col.get_palette())
			
			for i in range(0,self.layers-1):
				self.n_color = choice(self.colors)[1]
				self.image_col.set_palette_at(i,self.n_color)
		except:
			pass
		
		try:
			self.image_dirt = pygame.image.load('images/D_' + str(self.sprite)+'.png')
			self.image_dirt.convert_alpha()
		except:
			pass
	def roll_rects(self):
		#create rects
		self.rect = self.image_line.get_rect()
		self.rect.inflate(-10,-10)
		self.rect.normalize()
		self.collide_rect = self.rect.copy()
		self.screen_rect = self.screen.get_rect()
		self.collide_rect.inflate(-10,-10)
		self.collide_rect.normalize()
	"""	
	def blitme(self):
		#Draw the loot at it's current location.
		self.screen.blit(self.image_mat,self.rect) #Color (Paintjob)
		self.screen.blit(self.image_line,self.rect) #Line art	
		"""

		
		
		
