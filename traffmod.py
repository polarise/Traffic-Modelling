#!/usr/bin/env python
from __future__ import division
import sys
import time
import random
import scipy
import scipy.stats

class Distribution( object ):
	def __init__( self, Vmax ):
		self.V = Vmax
		self.velocities = list( scipy.stats.truncnorm.rvs( 0, self.V, loc=5, scale=10, size=1000 ))
	
	def __repr__( self ):
		return "Velocities are drawn from a truncated normal on [0,%s] with mu=%s, sigma=%s." % ( self.V, 5, 10 )

class Car( object ):
	def __init__( self, velocity, car_ahead ):
		self.velocity = velocity
		self.position = 0
		self.car_ahead = car_ahead
		self.cumul_time = 0
		self.visible = False
	
	def advance( self, dt ):
		self.cumul_time += dt
		self.position += self.velocity*dt
		if self.car_ahead == None:
			return
		elif self.position >= self.car_ahead.position:
			self.position = self.car_ahead.position - 1
			return
			
class Lane( object ):
	def __init__( self, name, length, direction, distribution, alpha=1 ):
		self.name = name
		self.length = length
		self.direction = direction
		self.distribution = distribution
		self.alpha = alpha
		
		self.cars = list()
	
	def __repr__( self ):
		lane = [ " " ] * self.length
		
		for c in self.cars:
			if c.position < self.length:
				if self.direction == "right": lane[ int( c.position ) ] = ">"
				elif self.direction == "left": lane[ int( c.position ) ] = "<"
		
		lane_str = "".join( lane )
		
		if self.direction == "right":
			return lane_str
		elif self.direction == "left":
			return lane_str[::-1]
		
	def add_car( self, dt ):
		p = 1 - scipy.exp( -self.alpha * dt )
		if random.random() <= p:		
			velocity = random.choice( self.distribution.velocities )
			if len( self.cars ) == 0:
				car_ahead = None
			else:
				car_ahead = self.cars[-1]
			self.cars.append( Car( velocity, car_ahead ))
			return
		else:
			return
	
	def update( self, dt ):				# update the positions
		if len( self.cars ) == 0: 
			return
		for c in self.cars:
			c.advance( dt )
			if c.position <= self.length:
				c.visible = True
			elif c.position > self.length:
				c.visible = False
		return
	
	def get_cumul_time( self ):
		cumul_time = 0
		for c in self.cars:
			if c.visible:
				cumul_time += c.cumul_time
			
		return cumul_time
		
class Road( object ):
	def __init__( self, name, lanes ): # lanes is a list of lanes
		self.name = name
		self.lanes = lanes
		self.length = lanes[0].length
		
	def __repr__( self ):
		kerb = "-" * self.length
		lanes = [ lane.__repr__() for lane in self.lanes ]
		
		return "\n".join( [ kerb ] + lanes + [ kerb ] )

	def operate( self, dt ):
		with open( "cumul_time.txt", 'w' ) as f:
			T = 0
			while True:
				cumul_time = list()
				for lane in self.lanes:
					lane.add_car( dt ) # add a car with P = 1 - exp( -lambda*dt )
					lane.update( dt )
					cumul_time += [ lane.get_cumul_time() ]
				print "Cumulative time: %s" % "|".join( map( str, cumul_time ))
				for lane in self.lanes:
					print lane.distribution
				print self
				print >> f, "%s\t%s" % ( T, "\t".join( map( str, cumul_time )))
				time.sleep( dt )
				T += dt
				

if __name__ == "__main__":
	distr1 = Distribution( 30 )
	distr2 = Distribution( 20 )
	lane1 = Lane( "Lane1", 130, "right", distr1 )
	lane2 = Lane( "Lane2", 130, "left", distr2 )
	lane3 = Lane( "Lane3", 130, "right", distr2 )
	lane4 = Lane( "Lane4", 130, "left", distr1 )
	road = Road( "My Road", [ lane1, lane3, lane2, lane4 ] )
	try:
		road.operate( 0.1 )
	except KeyboardInterrupt:
		print
		sys.exit( 0 )
