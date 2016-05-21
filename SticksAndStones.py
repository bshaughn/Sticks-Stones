import math
import random
from sys import stdout

class player:
	def __init__(self, name, gameboard):
		self.name = name
		self.boxes = []
		self.type = None
		self.possibleMoves = []
		self.board = gameboard
		self.assignType()

	def assignType(self):
		# if random.randrange(0,2) == 0:
		# 	self.type = "Basic"  #actually let's randomize this for now, Smart or Basic
		# else:
		# 	self.type = "Smart" #first level Smart will just look for 3-side boxes
		self.type = "Basic" #let's just get this working for now

	def pickMove(self):
		lastBoxCount = len(self.boxes)
		if self.type == "Basic":
			self.basicMove()
		else:
			self.smartMove()

		if self.board.sticksRemaining > 0 and lastBoxCount < len(self.boxes): #if you make a box after your move, go again (as long as there are sticks remaining)
			self.pickMove()

	def basicMove(self):
		choosingStick = True
		
		while choosingStick:  #find a horizontal or vertical stick that has not already been placed
			h_or_v = random.randrange(0, len(self.board.sticks))
			stick = random.randrange(0, len(self.board.sticks[h_or_v]))

			if len(self.board.sticks[h_or_v][stick])>0:
				choosingStick = False

		s1 = self.board.sticks[h_or_v][stick][0]
		s2 = self.board.sticks[h_or_v][stick][1]

		foundBox = self.board.connectStones(s1, s2)
		self.board.sticks[h_or_v][stick] = []

	def smartMove(self):
		if len(self.board.boxHash[3])>0:
			self.smartMoveChoice(3)
		elif len(self.board.boxHash[1])>0:
			self.smartMoveChoice(1)
		elif len(self.board.boxHash[2])>0:
			self.smartMoveChoice(2)
		else:
			self.basicMove()

	def smartMoveChoice(self, index):
		idx = random.randrange(0, len(self.board.boxHash[index]))
		stoneId = self.board.boxHash[index][idx]

		rightId = stoneId+1
		lowerId = stoneId+self.board.width
		lowerRightId = stoneId+self.board.width+1

		if stoneId not in self.board.adjList[lowerId]:
			foundBox = self.board.connectStones(stoneId, lowerId)
			self.board.sticks[1][stoneId] = []
			return
			
		if stoneId not in self.board.adjList[rightId]:
			foundBox = self.board.connectStones(stoneId, rightId)
			self.removeHorizontalStick(stoneId)
			return
			
		if lowerId not in self.board.adjList[lowerRightId]:
			foundBox = self.board.connectStones(lowerId, lowerRightId)
			self.removeHorizontalStick(lowerId)
			return
			
		if rightId not in self.board.adjList[lowerRightId]:
			foundBox = self.board.connectStones(rightId, lowerRightId)
			self.board.sticks[1][rightId] = []
			return

		print "no connection"
		return

	def removeHorizontalStick(self, index):
		for x in range(len(self.board.sticks[0])):
			if len(self.board.sticks[0][x])>0 and self.board.sticks[0][x][0] == index: #damn this is tricky
				self.board.sticks[0][x] = []
				return
			

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
		self.sticks = None
		self.boxHash = [[x for x in range(self.length*self.width)], [], [], [], []] #let's try maintaining a hash of boxes by number of completed sides
		self.populateSticksArray()

	def populateSticksArray(self):
		horiSticks = [[] for x in range((self.length)*(self.width-1))]
		vertSticks = [[] for x in range((self.width)*(self.length-1))]

		for y in range(self.length-1):
			for x in range(self.width):
				vertSticks[x+y*self.width] = [x+y*self.width, x+((y+1)*self.width)] 

		i = 0 # this is terrible
		for y in range(self.length):
			for x in range(self.width-1):
				horiSticks[i] = [y*self.width+x, y*self.width+x+1]
				i += 1

		self.sticks = [horiSticks, vertSticks] #this is really terrible

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

	# swap this to check the "4" position of the boxhash
	def boxIsFree(self, stoneId):
		# for p in self.players:
		# 	if stoneId in p.boxes:
		# 		return False

		# return True

		if stoneId in self.boxHash[4]:
			return False

		return True

	#rework this method
	# start by looking for each box in the boxhash, and move it if it gains an extra side
	def lookForBoxes(self):
		if self.activePlayer is None:
			return

		for y in range(0, self.length-1):
			for x in range(0, self.width-1):
				stoneId = x+(y*self.width)

				if self.boxIsFree(stoneId):
					boxSides = 0

					hashIndex = 0

					# for i in range(0,len(self.boxHash)):
					# 	if stoneId in self.boxHash[i]:
					# 		boxSides = i

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

					if self.boxes[stoneId] != boxSides:  #oooh that's tricky
						#print "boxSides: ", boxSides
						self.boxHash[self.boxes[stoneId]].remove(stoneId)
						self.boxHash[boxSides].append(stoneId)

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
		#self.b = board(10,8) #official board size
		self.b = board(15,15)
		self.maxBoxes = (self.b.length-1)*(self.b.width-1)
		# print "Number of possible boxes: ", self.maxBoxes
		self.winningTotal = 0
		self.winnerName = None
		self.play()

	def play(self):
		player_A = player("A", self.b)
		player_A.type = "Smart"
		player_B = player("B", self.b)
	 	player_B.type = "Smart"
		player_C = player("C", self.b)
		player_C.type = "Smart"
		player_D = player("D", self.b)
		player_D.type = "Smart"
		player_E = player("E", self.b)
		player_E.type = "Smart"
		player_F = player("F", self.b)
		player_F.type = "Smart"
		player_G = player("G", self.b)
		player_H = player("H", self.b)
		player_I = player("I", self.b)
		player_J = player("J", self.b)
		player_K = player("K", self.b)
		player_L = player("L", self.b)
		player_M = player("M", self.b)
		player_N = player("N", self.b)
		player_O = player("O", self.b)
		player_P = player("P", self.b)
		player_Q = player("Q", self.b)
		player_R = player("R", self.b)
		player_S = player("S", self.b)
		player_T = player("T", self.b)
		player_U = player("U", self.b)
		player_V = player("V", self.b)
		player_W = player("W", self.b)
		player_X = player("X", self.b)
		player_Y = player("Y", self.b)
		player_Z = player("Z", self.b)

		self.b.players.append(player_A)
		self.b.players.append(player_B)
		self.b.players.append(player_C)
		self.b.players.append(player_D)
		self.b.players.append(player_E)
		self.b.players.append(player_F)
		# self.b.players.append(player_G)
		# self.b.players.append(player_H)
		# self.b.players.append(player_I)
		# self.b.players.append(player_J)
		# self.b.players.append(player_K)
		# self.b.players.append(player_L)
		# self.b.players.append(player_M)
		# self.b.players.append(player_N)
		# self.b.players.append(player_O)
		# self.b.players.append(player_P)
		# self.b.players.append(player_Q)
		# self.b.players.append(player_R)
		# self.b.players.append(player_S)
		# self.b.players.append(player_T)
		# self.b.players.append(player_U)
		# self.b.players.append(player_V)
		# self.b.players.append(player_W)
		# self.b.players.append(player_X)
		# self.b.players.append(player_Y)
		# self.b.players.append(player_Z)

		#activePlayerIndex = 1
		activePlayerIndex = 0
		self.b.activePlayer = self.b.players[activePlayerIndex]

		#================================ Game Loop ==============================================

		while self.b.sticksRemaining > 0:
			self.b.activePlayer.pickMove()

			activePlayerIndex = (activePlayerIndex+1)%len(self.b.players)
			self.b.activePlayer = self.b.players[activePlayerIndex]

			#self.b.printBoard()

		maxBoxes = 0
		winner = None
		for p in range(0,len(self.b.players)):
			if len(self.b.players[p].boxes) > self.winningTotal:
				#maxBoxes = len(self.b.players[p].boxes)
				self.winningTotal = len(self.b.players[p].boxes)
				winner = self.b.players[p]

		#not optimized...
		tie = True

		for p in self.b.players:
			if len(p.boxes) != self.winningTotal:
				tie = False
		if tie is True:
			print "Tie! Each player has ", self.winningTotal, " boxes!"
			#self.b.printBoard()
		else:	
			#print winner.name, " is the winner with ", self.winningTotal, " boxes!"
			self.winnerName = winner.name

		self.b.printBoard()

avg = 0
max = 0
min = 100000

# winnerHash = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "G": 0, "H": 0, "I": 0, "J": 0, "K": 0, "L": 0, "M": 0, "N": 0, "O": 0, "P": 0, "Q": 0, "R": 0, "S": 0, "T": 0, "U": 0, "V": 0, "W": 0, "X": 0, "Y": 0, "Z": 0}
winnerHash = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0}
#for x in range(1, 100001):
for x in range(1, 1001):
	g = game()
	if g.winnerName is not None:
		winnerHash[g.winnerName] = winnerHash[g.winnerName]+1
	print x, ": "
	#print "\r"+str(winnerHash),
	#stdout.flush()
	print winnerHash

	if g.winningTotal > max:
		max = g.winningTotal
	if g.winningTotal < min:
		min = g.winningTotal

	avg += g.winningTotal
	# print "x: ", x
	# print "g.winningTotal: ", g.winningTotal
avg /= x

# print "max: ", max
# print "min: ", min
# print "avg: ", avg
#print winnerHash
print "DONE"


