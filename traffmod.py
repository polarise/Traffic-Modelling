#!/usr/bin/env python
from __future__ import division
import sys
import time
import random
import scipy
import scipy.stats

class Distribution( object ):
	def __init__( self, V, P ):
		self.C = len( V	)				# no. of V categories
		self.V = V
		self.P = P
		self.velocities = list()

		for i in xrange( self.C ):
			self.velocities += [ V[i] ]*int( P[i]*1000 )
	
	def __repr__( self ):
		return "There are %s velocity categories. " % ( self.C ) + "These are [m/s]: " + "; ".join( map( str, self.V ))
		

class Car( object ):
	def __init__( self, velocity, car_ahead ):
		self.velocity = velocity
		self.position = 0
		self.car_ahead = car_ahead
	
	def advance( self, dt ):
		self.position += self.velocity*dt
		if self.car_ahead == None:
			return
		elif self.position >= self.car_ahead.position:
			self.position = self.car_ahead.position - 1
			return
		
class Road( object ):
	def __init__( self, name, length, distribution ):
		self.name = name
		self.length = length
		self.distribution = distribution
		self.cars = list()
		self.srac = list()
		self.appear_prob = 0.8 # probability of a new car
		
	def __repr__( self ):
		lane1 = [ " " ]*self.length
		lane2 = [ " " ]*self.length
		
		top = "-" * self.length
		
		for c in self.cars:
			if c.position < self.length:
				lane1[ int( c.position ) ] = ">"
		
		for c in self.srac:
			if c.position < self.length:
				lane2[ int( c.position ) ] = "<"
			
		lane1_str = "".join( lane1 )
		lane2_str = "".join( lane2 )
		
		bot = "-" * self.length
		
		return top + "\n" + lane1_str + "\n" + lane2_str[::-1] + "\n" + bot
		
	def add_car_for( self ):
		# pick a velocity category
		velocity = random.choice( self.distribution.velocities )
		if len( self.cars ) == 0:
			car_ahead = None
		else:
			car_ahead = self.cars[-1]
		self.cars.append( Car( velocity, car_ahead ))
		return
		
	def add_car_rev( self ):
		velocity = random.choice( self.distribution.velocities )
		if len( self.srac ) == 0:
			car_ahead = None
		else:
			car_ahead = self.srac[-1]
		self.srac.append( Car( velocity, car_ahead ))
		
	def update_for( self, dt ):
		# update the positions
		if len( self.cars ) == 0:
			return
		for c in self.cars:
			c.advance( dt )
		return
		
	def update_rev( self, dt ):
		if len( self.srac ) == 0:
			return
		for c in self.srac:
			c.advance( dt )
		return
	
	def operate( self, dt ):
		while True:
			if random.random() <= self.appear_prob:
				self.add_car_for()
			if random.random() <= self.appear_prob:
				self.add_car_rev()
			self.update_for( dt )
			self.update_rev( dt )
			print self.distribution
			print self
			time.sleep( dt )

if __name__ == "__main__":
	distr = Distribution( [5, 9, 15, 20], [ .15, .20, .50, .15 ] )
	road = Road( "My Road", 130, distr )
	try:
		road.operate( 1 )
	except KeyboardInterrupt:
		sys.exit( 0 )
