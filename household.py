import pygame

class Household(object):
	def __init__(	self,settings, screen, stats, lot_value=None, 
					materials=None, colors=None, num_proles=None):
		self.settings = settings
		self.screen = screen
		self.stats = stats
		self.lot_value = lot_value
		self.materials = materials
		self.colors = colors
		self.num_proles = num_proles
		adult1 = Prole(settings, screen, stats)


class Prole(object):
	def __init__(	self,settings, screen, stats, hh_value=None, 
					materials=None, colors=None, lname=None, fname=None,
					salary=None, age=None, sex=None):
		self.settings = settings
		self.screen = screen
		self.stats = stats
		self.hh_value = hh_value
		self.materials = materials
		self.colors = colors
		self.lname = lname
		self.fname = fname
		self.salary = salary
		self.age = age
		self.sex = sex
