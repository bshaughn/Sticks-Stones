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
				
				if self.boxes[stoneId] != 4 and self.boxIsFree(stoneId):
					boxSides = []
					missingSides = []

					rightId = stoneId+1
					lowerId = stoneId+self.width
					lowerRightId = stoneId+self.width+1

					connectedBelow = True if (len(self.adjList[lowerId])>=1 and stoneId in self.adjList[lowerId]) else False
					connectedRight = True if (len(self.adjList[rightId])>=1 and stoneId in self.adjList[rightId]) else False
					connectedLowerRightToBelow = True if (len(self.adjList[lowerRightId])>=1 and lowerId in self.adjList[lowerRightId]) else False
					connectedLowerRightToRight = True if (len(self.adjList[lowerRightId])>=1 and rightId in self.adjList[lowerRightId]) else False

					if connectedBelow:
						boxSides.append([lowerId, stoneId])
					else:
						missingSides.append([lowerId, stoneId])

					if connectedRight:
						boxSides.append([rightId, stoneId])
					else:
						missingSides.append([rightId, stoneId])

					if connectedLowerRightToBelow:
						boxSides.append([lowerId, lowerRightId])
					else:
						missingSides.append([lowerId, lowerRightId])

					if connectedLowerRightToRight:
						boxSides.append([rightId, lowerRightId])
					else:
						missingSides.append([rightId, lowerRightId])

					self.boxes[stoneId] = len(boxSides)

					if len(boxSides) == 4:
						self.activePlayer.boxes.append(stoneId)
						return self.lookForBoxes()

		return False

	def printBoard(self):
		for y in range(0,self.length-1):
			for x in range(0,self.width-1):
				sideCount = self.boxes[x+y*self.width]
				if sideCount == 4:
					for p in b.players:
						if x+y*self.width in p.boxes:
							print p.name,
				else:
					print sideCount,

				print " | ",

			print "" 

#b = board(8,10) #official board size
b = board(21,23) #official board size

horiSticks = [[] for x in range((b.length)*(b.width-1))]
vertSticks = [[] for x in range((b.width)*(b.length-1))]

for y in range(b.length-1):
	for x in range(b.width):
		vertSticks[x+y*b.width] = [x+y*b.width, x+y*b.width+b.width] 

i = 0 # this is terrible
for y in range(b.length):
	for x in range(b.width-1):
		horiSticks[i] = [y*b.width+x, y*b.width+x+1]
		i += 1

sticks = [horiSticks, vertSticks] #this is really terrible

player_A = player("A")
player_B = player("B")

b.players.append(player_A)
b.players.append(player_B)

activePlayerIndex = 1
b.activePlayer = b.players[activePlayerIndex]

#================================ Game Loop ==============================================

while b.sticksRemaining > 0:
	choosingStick = True
	while choosingStick:
		h_or_v = random.randrange(0, len(sticks))
		stick = random.randrange(0, len(sticks[h_or_v]))

		if len(sticks[h_or_v][stick])>0:
			choosingStick = False

	s1 = sticks[h_or_v][stick][0]
	s2 = sticks[h_or_v][stick][1]

	foundBox = b.connectStones(s1, s2)

	activePlayerIndex = (activePlayerIndex+1)%len(b.players)
	b.activePlayer = b.players[activePlayerIndex]

	sticks[h_or_v][stick] = []

	#b.printBoard()

maxBoxes = 0
winner = None
for p in range(0,len(b.players)):
	if len(b.players[p].boxes) > maxBoxes:
		maxBoxes = len(b.players[p].boxes)
		winner = b.players[p]

print winner.name, " is the winner with ", maxBoxes, " boxes!"
b.printBoard()
