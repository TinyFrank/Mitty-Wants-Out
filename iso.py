def iso_collide(rect1, rect2):
	""" return TRUE if a collision is detected between two 
	parallelograms. the parallelograms are defined by the collision
	boxes of two rectangles, truncated at 30 degrees on the lower left
	and upper right corners"""
	
	LR1 = get_edges(rect1)
	LR2 = get_edges(rect2)
	
	L = False
	R = False
	
	if LR1[0] > LR2[1]:
		L = True
	if LR2[0] > LR1[1]:
		R = True
	
	Collision = False
	
	if L == R:
		Collision = True
		
	#print('Collision is ' + str(Collision))
	return(Collision)

def get_edges(rect):
	"""Return the y-axis intercept for the left and right iso edges
	of a given rectangle"""
	
	Lx = rect.x
	Ly = rect.y + rect.height/2
	
	Rx = rect.x + rect.width
	Ry = rect.y + rect.height/2
	
	L = get_edge(Lx, Ly)
	R = get_edge(Rx, Ry)
	
	LR = [ L, R ]
	
	return(LR)
	
def get_edge(x,y):
	"""Return the y-axis intercept ('b') for a point, given a slope
	of 30 degrees"""
	
	b = ((1/1.732)*x)-y
	
	return(b)
