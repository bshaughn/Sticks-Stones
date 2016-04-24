import math
import random
from sys import stdout

class player:
	def __init__(self, name):
		self.name = name
		self.boxes = []

class board:
	def __init__(self, length, width):
		self.length = length
		self.width = width
		self.boxes = [0 for x in range(self.length*self.width)]
		self.adjList = [[] for x in range(self.length*self.width)]
		self.sticksRemaining = self.width*(self.length-1)+self.length*(self.width-1)
		self.boardState = [0 for x in range(self.length*self.width)]  #just for testing and screwing around
		self.players = [] #ultimately this will be part of a Game instance
		self.activePlayer = None

	def areAdjacent(self, x, y):
		x_col = x%self.width
		x_row = int(math.floor(x/self.width))
		y_col = y%self.width
		y_row = int(math.floor(y/self.width))

		if abs(y_col-x_col) == 1 and y_row==x_row:
			return True

		if y_col==x_col and abs(y_row-x_row) == 1:
			return True

		return False

	def connectStones(self, x, y):
		if not self.areAdjacent(x,y):
			#print "Those are not adjacent!"
			return

		if self.sticksRemaining == 0:
			return

		if y in self.adjList[x]:
			#print x, " and ", y, " are already connected!"
			return

		self.adjList[x].append(y)
		self.adjList[y].append(x)
		self.sticksRemaining -= 1

		return self.lookForBoxes()

	def boxIsFree(self, stoneId):
		for p in self.players:
			if stoneId in p.boxes:
				return False

		return True

	def lookForBoxes(self):
		if self.activePlayer is None:
			return

		for y in range(0, self.length-1):
			for x in range(0, self.width-1):
				stoneId = x+(y*self.width)
				
				if self.boxIsFree(stoneId):
					boxSides = 0

					rightId = stoneId+1
					lowerId = stoneId+self.width
					lowerRightId = stoneId+self.width+1

					# connectedBelow
					if len(self.adjList[lowerId])>=1 and stoneId in self.adjList[lowerId]:
						boxSides += 1

					# connectedRight
					if len(self.adjList[rightId])>=1 and stoneId in self.adjList[rightId]:
						boxSides += 1

					# connectedLowerRightToBelow
					if len(self.adjList[lowerRightId])>=1 and lowerId in self.adjList[lowerRightId]:
						boxSides += 1

					# connectedLowerRightToRight
					if len(self.adjList[lowerRightId])>=1 and rightId in self.adjList[lowerRightId]:
						boxSides += 1

					self.boxes[stoneId] = boxSides

					if boxSides == 4:
						self.activePlayer.boxes.append(stoneId)
						return self.lookForBoxes()

		return False

	def printBoard(self):
		for y in range(0,self.length-1):
			for x in range(0,self.width-1):
				sideCount = self.boxes[x+y*self.width]
				if sideCount == 4:
					for p in self.players:
						if x+y*self.width in p.boxes:
							print p.name,
				else:
					print sideCount,

				print " | ",

			print "" 

class game:
	def __init__(self):

		#b = board(8,10) #official board size
		self.b = board(10,8) #official board size
		self.maxBoxes = (self.b.length-1)*(self.b.width-1)
		print "Number of possible boxes: ", self.maxBoxes
		self.winningTotal = 0
		self.play()

	def play(self):
		horiSticks = [[] for x in range((self.b.length)*(self.b.width-1))]
		vertSticks = [[] for x in range((self.b.width)*(self.b.length-1))]

		for y in range(self.b.length-1):
			for x in range(self.b.width):
				vertSticks[x+y*self.b.width] = [x+y*self.b.width, x+y*self.b.width+self.b.width] 

		i = 0 # this is terrible
		for y in range(self.b.length):
			for x in range(self.b.width-1):
				horiSticks[i] = [y*self.b.width+x, y*self.b.width+x+1]
				i += 1

		sticks = [horiSticks, vertSticks] #this is really terrible

		player_A = player("A")
		player_B = player("B")
		player_C = player("C")
		player_D = player("D")
		player_E = player("E")
		player_F = player("F")
		player_G = player("G")
		player_H = player("H")
		player_I = player("I")
		player_J = player("J")
		player_K = player("K")

		self.b.players.append(player_A)
		self.b.players.append(player_B)
		self.b.players.append(player_C)
		self.b.players.append(player_D)
		self.b.players.append(player_E)
		self.b.players.append(player_F)
		self.b.players.append(player_G)
		self.b.players.append(player_H)
		self.b.players.append(player_I)
		self.b.players.append(player_J)
		self.b.players.append(player_K)

		activePlayerIndex = 1
		self.b.activePlayer = self.b.players[activePlayerIndex]

		#================================ Game Loop ==============================================

		while self.b.sticksRemaining > 0:
			choosingStick = True
			while choosingStick:
				h_or_v = random.randrange(0, len(sticks))
				stick = random.randrange(0, len(sticks[h_or_v]))

				if len(sticks[h_or_v][stick])>0:
					choosingStick = False

			s1 = sticks[h_or_v][stick][0]
			s2 = sticks[h_or_v][stick][1]

			foundBox = self.b.connectStones(s1, s2)

			activePlayerIndex = (activePlayerIndex+1)%len(self.b.players)
			self.b.activePlayer = self.b.players[activePlayerIndex]

			sticks[h_or_v][stick] = []

			#b.printBoard()

		#maxBoxes = 0
		winner = None
		for p in range(0,len(self.b.players)):
			if len(self.b.players[p].boxes) > self.winningTotal:
				#maxBoxes = len(self.b.players[p].boxes)
				self.winningTotal = len(self.b.players[p].boxes)
				winner = self.b.players[p]

		print winner.name, " is the winner with ", self.winningTotal, " boxes!"
		self.b.printBoard()


avg = 0
max = 0
min = 100000
for x in range(1, 100001):
	g = game()
	if g.winningTotal > max:
		max = g.winningTotal
	if g.winningTotal < min:
		min = g.winningTotal

	avg += g.winningTotal
	print "x: ", x
	print "g.winningTotal: ", g.winningTotal
avg /= x

print "max: ", max
print "min: ", min
print "avg: ", avg


