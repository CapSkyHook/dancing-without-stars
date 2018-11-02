#!/usr/bin/python
import sys, random
from copy import deepcopy
from client import Client
from getopt import getopt, GetoptError
import heapq 
from sklearn.neighbors import DistanceMetric
from sklearn.metrics.pairwise import pairwise_distances

"""
python3 sample_player.py -H <host> -p <port> <-c|-s>
"""
def process_file(file_data):
	"""read in input file"""
	dancers = {}
	dancer_id = -1
	f = file_data.split("\n")
	for line in f:
		print(line)
		tokens = line.split()
		if len(tokens) == 2:
			dancer_id+=1
			dancers[dancer_id] = (int(tokens[0]), int(tokens[1]), latest_color)
		elif len(tokens)>2:
			latest_color = int(tokens[-1])
	return dancers

def print_usage():
	print("Usage: python3 sample_player.py -H <host> -p <port> [-c/-s]")

def get_args():
	host = None
	port = None
	player = None
	##########################################
	#PLEASE ADD YOUR TEAM NAME#
	##########################################
	name = "Sunflower"
	##########################################
	#PLEASE ADD YOUR TEAM NAME#
	##########################################
	try:
		opts, args = getopt(sys.argv[1:], "hcsH:p:", ["help"])
	except GetoptError:
		print_usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			print_usage()
			sys.exit()
		elif opt == "-H":
			host = arg
		elif opt == "-p":
			port = int(arg)
		elif opt == "-c":
			player = "c"
		elif opt == "-s":
			player = "s"
	if host is None or port is None or player is None:
		print_usage()
		sys.exit(2)
	return host, port, player, name

def get_buffer_stars(stars):
	stars_str = ""
	for s in stars:
		stars_str += (str(s[0]) + " " + str(s[1]) + " ")
	return stars_str

class Player:
	def __init__(self, board_size, num_color, k, dancers):
		self.board_size = board_size
		self.num_color = num_color
		# k dancers for each color
		self.k = k
		# self.dancers is a dictionary with key as the id of the dancers
		# with value as the tuple of 3 (x, y, c)
		# where (x,y) is initial position of dancer
		# c is the color id of the dancer
		self.dancers = dancers
		self.dist = DistanceMetric.get_metric('manhattan')
        # arr_patients = [ [patient[0], patient[1]] for dancier in self.danciers.values()]

        # D = pairwise_distances(arr_patients, metric='manhattan')

	# TODO add your method here
	# Add your stars as a spoiler
	def get_stars(self):
		#
		#
		# You need to return a list of coordinates representing stars
		# Each coordinate is a tuple of 2 values (x, y)
		#
		#
		stars = []
		x = -1
		y = -1
		occupied = set()
		for id in self.dancers:
			occupied.add((self.dancers[id][0], self.dancers[id][1]))
		while len(stars) < self.k:
			x = random.randint(0, self.board_size - 1)
			y = random.randint(0, self.board_size - 1)
			if (x, y) not in occupied:
				# check manhattan distance with other stars
				ok_to_add = True
				for s in stars:
					if abs(x - s[0]) + abs(y - s[1]) < self.num_color + 1:
						ok_to_add = False
						break
				if ok_to_add:
					stars.append((x, y))
					occupied.add((x, y))
		return stars

	# TODO add your method here
	# Add your moves as a choreographer

	def return_and_delete_middle_elem(self, arr):
		mid_point = len(arr) // 2
		return_elem = arr[mid_point]
		del arr[mid_point]
		return return_elem

	def get_moves(self, stars):
		#
		#
		# You need to return a list of moves from the beginning to the end of the game
		# Each move is a dictionary with key as the id of the dancer you want to move
		# with value as a tuple of 2 values (x, y) representing the new position of the dancer
		#
		#

		# pick 5 random dancers from dancers


		dancerPriorityQueues = {}
		for centerId in range(self.dancers[[*self.dancers][-1]][2] + 1):
			dancerPriorityQueues[centerId] = [[] for _ in range((self.dancers[[*self.dancers][-1]][2] + 1))]

		for centerDancerID, dancerCenter in self.dancers.items():

			for outerDancerID, dancerOuter in self.dancers.items():
				if dancerCenter[2] == dancerOuter[2]: continue
				distance = self.dist.pairwise([[dancerCenter[0], dancerCenter[1]], [dancerOuter[0], dancerOuter[1]]])[0][1]
				
				dancerPriorityQueues[dancerCenter[2]][dancerOuter[2]].append(( centerDancerID, outerDancerID, distance))
		num_groups = int(len(self.dancers)/self.dancers[[*self.dancers][-1]][2])
		final_clusters = None 
		final_cluster_dist = 1000000

		num_types_dancers = self.dancers[[*self.dancers][-1]][2]
		
		# this needs to be changed so we instead calculate the 
		for centerId in range(1, num_types_dancers + 1):
			clusters = {}
			usedCenters = set()
			usedTargetIDs = set()
			total_traveled_distance = 0
			for targetId in range(1, num_types_dancers + 1):
				usedCenters = set()
				usedTargetIDs = set()
				if centerId == targetId: continue
				sortedItems = sorted(dancerPriorityQueues[centerId][targetId], key=lambda x: x[2])
				print("Target Id: ", targetId)
				while len(usedCenters) < num_groups:
					print(len(usedCenters))
					middle_elem = self.return_and_delete_middle_elem(sortedItems)
					if middle_elem[0] not in usedCenters and middle_elem[1] not in usedTargetIDs:
						if middle_elem[0] not in clusters:
							clusters[middle_elem[0]] = {}
							clusters[middle_elem[0]][centerId] = middle_elem[0]

						clusters[middle_elem[0]][targetId] = middle_elem[1]
						usedCenters.add(middle_elem[0])
						usedTargetIDs.add(middle_elem[1])
						total_traveled_distance += middle_elem[2]	
			avg_dist = total_traveled_distance / len(self.dancers)
			if avg_dist < final_cluster_dist:
				final_clusters = clusters
				final_cluster_dist = avg_dist


		import pdb; pdb.set_trace()
		return moves

def main():
	host, port, p, name = get_args()
	# create client
	client = Client(host, port)
	# send team name
	client.send(name)
	# receive other parameters
	parameters = client.receive()
	parameters_l = parameters.split()
	board_size = int(parameters_l[0])
	num_color = int(parameters_l[1])
	k = int(parameters_l[2]) # max num of stars\\\\\\\
	# receive file data
	file_data = client.receive()
	# process file
	dancers = process_file(file_data) # a set of initial dancers
	__dancers = deepcopy(dancers)
	player = Player(board_size, num_color, k, dancers)
	# now start to play
	if p == "s":
		print("Making stars")
		stars = player.get_stars()
		print(stars)
		# send stars
		client.send(get_buffer_stars(stars))
	else: # choreographer
		# receive stars from server
		stars_str = client.receive()
		stars_str_l = stars_str.split()
		stars = []
		for i in range(int(len(stars_str_l)/2)):
			stars.append((int(stars_str_l[2*i]), int(stars_str_l[2*i+1])))

		moves = player.get_moves(stars)
		for move in moves: # iterate through all the moves
			print(move)
			move_str = str(len(move))
			for id in move: # for each dancer id in this move
				x, y, color = __dancers[id]
				nx, ny = move[id]
				move_str += " " + str(x) + " " + str(y) + " " + str(nx) + " " + str(ny)
				__dancers[id] = (nx, ny, 0)

			client.send(move_str)

		# send DONE flag
		client.send("DONE")
		# send a line to signal the server to stop
		rid = random.sample(__dancers.keys(), 1)[0]
		random_dancer = __dancers[rid]
		client.send(str(random_dancer[0]) + " " + str(random_dancer[1]) + " " + str(random_dancer[0]) + " " + str(random_dancer[1] + 4))

	# close connection
	client.close()

if __name__ == "__main__":
	main()
