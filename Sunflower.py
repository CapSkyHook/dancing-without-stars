#!/usr/bin/python
import sys, random
from copy import deepcopy
from client import Client
from getopt import getopt, GetoptError
from sklearn.neighbors import DistanceMetric
from sklearn.metrics.pairwise import pairwise_distances
from operator import itemgetter
import collections
import copy
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
		self.board = [[False for i in range(self.board_size)] for j in range(self.board_size)]
		self.dancersbycolor = {}
		self.left = 9999
		self.right = -1
		self.top = -1
		self.bot = 9999
		self.dist = DistanceMetric.get_metric('manhattan')
		self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

	# TODO add your method here
	# Add your stars as a spoiler
	def get_stars(self):
		#
		#
		# You need to return a list of coordinates representing stars
		# Each coordinate is a tuple of 2 values (x, y)
		#
		#
		self.collectcolor()
		dancers = self.dancers.copy()
		print("I'm alive")
		stars = self.adjPlaceStars(dancers)
		'''x = -1
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
					occupied.add((x, y))'''
		return stars

	def collectcolor(self):
		for color in range(1, self.num_color+1):
			self.dancersbycolor[color] = []

		for k,v in self.dancers.items():
			self.board[v[0]][v[1]] = True
			self.left = min(self.left, v[0])
			self.right = max(self.right, v[0])
			self.top = max(self.top, v[1])
			self.bot = min(self.bot, v[1])
			self.dancersbycolor[v[2]].append([k, v])

	def adjPlaceStars(self, dancers):
		boardSize = self.board_size
		numDancers = self.k
		numColors = self.num_color
		numStars = numDancers
		colors = [i for i in range(1, self.num_color+1)]
		dx = [1,-1,0,0]
		dy = [0,0,1,-1]

		candidates = []

		while len(colors) > 0:
			start = random.choice(colors)
			colors.remove(start)

			for v in self.dancersbycolor[start]:
				for direc in range(0,4):
					nx = v[1][0]+dx[direc]
					ny = v[1][1]+dy[direc]
					if nx > self.board_size or ny > self.board_size or nx < 0 or ny < 0:
						continue

					if self.board[nx][ny] == True:
						continue
					candidates.append([nx, ny])
					#print(len(candidates))
		
		fail = 0
		#print(candidates)

		stars = []
		while len(stars) < numStars and len(candidates) > 0:
			point = candidates[0]
			print(point)
			candidates.pop(0)

			tooClose = False

			for star in stars:
				if self.manDist(point, star) < numColors + 1:
					tooClose = True
					fail += 1
					break

			if not tooClose:
				print("add one point")
				stars.append(point)

		#print(len(stars))
		#print(fail)

		while len(stars) < numStars:
			x = random.randint(self.left, self.right)
			y = random.randint(self.bot, self.top)

			point = [x,y]
			for star in stars:
				if self.manDist(point, star) < numColors + 1:
					tooClose = True
					break

				if not tooClose:
					stars.append(point)

		return stars

	def manDist(self, p1, p2):
		return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
	  
	# TODO add your method here
	# Add your moves as a choreographer

	def fillboard(self, board):
		for k, v in self.dancers.items():
			board[v[0]][v[1]] = True

	def find_viable_moves(self, curr_pos, end_pos, board):
		valid_poses = []
		for direction in self.directions:
			new_pos = (curr_pos[0] + direction[0], curr_pos[1] + direction[1])
			if self.is_closer(curr_pos, new_pos, end_pos):
				valid_poses.append(new_pos)

		return valid_poses

	def is_closer(self, curr_pos, new_pos, end_pos):
		return self.dist.pairwise([[curr_pos[0], curr_pos[1]], [end_pos[0], end_pos[1]]])[0][1] > self.dist.pairwise([[new_pos[0], new_pos[1]], [end_pos[0], end_pos[1]]])[0][1]

	def finished(self, curr_poses, end_coordinates):
		off_count = 0
		for key, value in curr_poses.items():
			if end_coordinates[key][0] != value[0] and end_coordinates[key][1] != value[1]:
				off_count += 1
		
		print("Off count: ", off_count)

		if off_count > 0:
			return False

		return True


	def place_cluster(self, board, one_side, other_side, direction, center):
		poses = []
		if direction == 0: # horizontal
			for i in range(1, one_side + 1):
				test_pos = (center[0] + i, center[1])
				if (test_pos[0] >= self.board_size or test_pos[1] >= self.board_size) or board[test_pos[0]][test_pos[1]] != 0:
					return False, []
				poses.append(test_pos)

			for i in range(1, other_side + 1):
				test_pos = (center[0] - i, center[1])
				if test_pos[0] < 0 or test_pos[1] < 0 or board[test_pos[0]][test_pos[1]] != 0:
					return False, []
				poses.append(test_pos)
		else: # vertical
			for i in range(1, one_side + 1):
				test_pos = (center[0], center[1] + i)
				if test_pos[0] >= self.board_size or test_pos[1] >= self.board_size or board[test_pos[0]][test_pos[1]] != 0:
					return False, []
				poses.append(test_pos)

			for i in range(1, other_side + 1):
				test_pos = (center[0], center[1] - i)
				if test_pos[0] < 0 or test_pos[1] < 0 or board[test_pos[0]][test_pos[1]] != 0:
					return False, []
				poses.append(test_pos)
		return True, poses

	def within(self, centerPoint, obstacle, targetPoint):
		return centerPoint <= obstacle <= targetPoint or targetPoint <= obstacle <= centerPoint

	def get_clusters(self, stars):
		dancerPriorityQueues = {}
		for centerId in range(self.dancers[[*self.dancers][-1]][2] + 1):
			dancerPriorityQueues[centerId] = [[] for _ in range((self.dancers[[*self.dancers][-1]][2] + 1))]

		for centerDancerID, dancerCenter in self.dancers.items():
			for outerDancerID, dancerOuter in self.dancers.items():
				if dancerCenter[2] == dancerOuter[2]: continue
				distance = self.dist.pairwise([[dancerCenter[0], dancerCenter[1]], [dancerOuter[0], dancerOuter[1]]])[0][1]
				obstacle = 0
				for star in stars:
					if self.within((dancerCenter[0], dancerCenter[1]), star, (dancerOuter[0], dancerOuter[1])):
						distance += 2 # Penalty to account for star
						obstacle += 1

				dancerPriorityQueues[dancerCenter[2]][dancerOuter[2]].append(( centerDancerID, outerDancerID, distance))
		num_groups = int(len(self.dancers)/self.dancers[[*self.dancers][-1]][2])
		final_clusters = None 
		final_moves = None
		final_centers = None
		final_cluster_dist = 1000000

		num_types_dancers = self.dancers[[*self.dancers][-1]][2]
		
		# this needs to be changed so we instead calculate the 
		for centerId in range(1, num_types_dancers + 1):
			clusters = {}
			centers = {}
			usedCenters = set()
			usedTargetIDs = set()
			total_traveled_distance = 0
			
			for targetId in range(1, num_types_dancers + 1):
				usedCenters = set()
				usedTargetIDs = set()
				if centerId == targetId: continue
				sortedItems = sorted(dancerPriorityQueues[centerId][targetId], key=lambda x: x[2])
				while len(usedCenters) < num_groups and sortedItems:
					middle_elem = self.return_and_delete_middle_elem(sortedItems)
					if middle_elem[0] not in usedCenters and middle_elem[1] not in usedTargetIDs:
						# if not self.mark_space(middle_elem, grid):
						# 	continue
						if middle_elem[0] not in clusters:
							clusters[middle_elem[0]] = {}
							clusters[middle_elem[0]][centerId] = [middle_elem[0], 0]
							clusters[middle_elem[0]]["distance"] = 0
							centers[middle_elem[0]] = middle_elem[0]

						clusters[middle_elem[0]][targetId] = [middle_elem[1], middle_elem[2]]
						centers[middle_elem[1]] = middle_elem[0]
						usedCenters.add(middle_elem[0])
						usedTargetIDs.add(middle_elem[1])
						clusters[middle_elem[0]]["distance"] += middle_elem[2]	
						total_traveled_distance += middle_elem[2]	
				if not sortedItems and len(usedCenters) < num_groups:
					total_traveled_distance += 99999999999
					break
			avg_dist = total_traveled_distance / len(self.dancers)

			if avg_dist < final_cluster_dist:
				final_clusters = clusters
				final_cluster_dist = avg_dist
				final_centers = centers
		return final_clusters, final_centers

	def set_up_board(self, stars, clusters, centerType):
		board = [[0 for i in range(self.board_size)] for j in range(self.board_size)]

		for star in stars:
			board[star[0]][star[1]] = -1

		for cluster in clusters:
			x, y, color = self.dancers[cluster]
			if color == centerType:
				board[x][y] = -2 
		return board
	# TODO add your method here
	# Add your stars as a spoiler

	def collectcolor(self):
		for color in range(1, self.num_color+1):
			self.dancersbycolor[color] = []

		for k,v in self.dancers.items():
			self.board[v[0]][v[1]] = True
			self.left = min(self.left, v[0])
			self.right = max(self.right, v[0])
			self.top = max(self.top, v[1])
			self.bot = min(self.bot, v[1])
			self.dancersbycolor[v[2]].append([k, v])

	def adjPlaceStars(self, dancers):
		boardSize = self.board_size
		numDancers = self.k
		numColors = self.num_color
		numStars = numDancers
		colors = [i for i in range(1, self.num_color+1)]
		dx = [1,-1,0,0]
		dy = [0,0,1,-1]

		candidates = []

		while len(colors) > 0:
			start = random.choice(colors)
			colors.remove(start)

			for v in self.dancersbycolor[start]:
				for direc in range(0,4):
					nx = v[1][0]+dx[direc]
					ny = v[1][1]+dy[direc]
					if nx >= self.board_size or ny >= self.board_size or nx < 0 or ny < 0:
						continue

					if self.board[nx][ny] == True:
						continue
					candidates.append([nx, ny])
					#print(len(candidates))
		
		fail = 0
		#print(candidates)

		stars = []
		while len(stars) < numStars and len(candidates) > 0:
			point = candidates[0]
			print(point)
			candidates.pop(0)

			tooClose = False

			for star in stars:
				if self.manDist(point, star) < numColors + 1:
					tooClose = True
					fail += 1
					break

			if not tooClose:
				print("add one point")
				stars.append(point)

		#print(len(stars))
		#print(fail)

		while len(stars) < numStars:
			x = random.randint(self.left, self.right)
			y = random.randint(self.bot, self.top)

			point = [x,y]
			for star in stars:
				if self.manDist(point, star) < numColors + 1:
					tooClose = True
					break

				if not tooClose:
					stars.append(point)

		return stars
	
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
		clusters, centers = self.get_clusters(stars)
		# print("Got clusters")
		end_coordinates, board = self.place_clusters(clusters, stars, centers)
		# print("Got end_coordinates")

		# CURRENT THIS PLATEAUS AT 42 PEOPLE SO NEED TO DO A LITTLE MORE
		moves = self.route(end_coordinates, board)
		roundT = 0
		for move in moves:
			foo = set()
			for dancerId, coord in move.items():
				# import pdb; pdb.set_trace()
				if coord not in foo:
					foo.add(coord)
				else:
					pass
					# import pdb; pdb.set_trace()
			roundT += 1
		# import pdb; pdb.set_trace()
		return moves


	def place_clusters(self, clusters, stars, centers):
		centerType = self.dancers[centers[1]][2]
		board = self.set_up_board(stars, clusters, centerType)
		clusters_by_distance = sorted(list(clusters.values()), key=itemgetter('distance'), reverse=True) 
		final_poses = {}
		positions_not_found = []
		for cluster in clusters_by_distance:
			center = cluster[centerType][0]
			best_balance = self.k
			best_positions = {}
			found_one = False
			for direction in range(2):
				for one_side in range(self.num_color):
					other_side = self.num_color - 1 - one_side

					valid_pos, poses = self.place_cluster(board, one_side, other_side, direction, self.dancers[center])
					potential_balance = abs(one_side - other_side)
					if valid_pos:
						if found_one and potential_balance >= best_balance:
							break
						found_one = True
						best_balance = potential_balance
						for key, value in cluster.items():
							if key == "distance": continue

							if centerType == self.dancers[value[0]][2]:
								best_positions[value[0]] = (self.dancers[value[0]][0], self.dancers[value[0]][1])
							else:
								best_positions[value[0]] = poses.pop()

			if not found_one:
				positions_not_found.append(cluster)

			# if (self.num_color != len(best_positions) and len(best_positions) > 0 ) or not found_one:
			# 	import pdb; pdb.set_trace()
			for key, position in best_positions.items():
				final_poses[key] = position
				if key != center:
					board[position[0]][position[1]] = key
		# if len(final_poses) != len(self.dancers):
		# 	import pdb; pdb.set_trace()


		# If we can't place a cluster, place them anywhere
		for cluster in positions_not_found:

			poses = self.place_cluster_anywhere_close(board, self.dancers[center])

			for dancerId, distance_deprecated in cluster.items():
				if poses:
					final_poses[key] = poses.pop()
				else:
					for i in range(self.board_size):
						for j in range(self.board_size):
							if (board[i][j] == 0 and 0 not in final_poses) or ((i, j) != final_poses[0]):
								final_poses[key] = (i, j)

				if key != center:
					board[final_poses[key][0]][final_poses[key][1]] = key

		return final_poses, board


	# def place_cluster_anywhere_close(self, board, center):
		# visited, queue = set(), collections.deque([center])
		# while queue: 
		# 	vertex = queue.popleft()
		# 	for coord in [(vertex[0] + x, vertex[1] + y) for x, y in self.directions]: 
		# 		if coord not in visited and board[coord[0]][coord[1]] == 0:
		# 			for direction in range(2):
		# 				for one_side in range(self.num_color):
		# 					other_side = self.num_color - 1 - one_side 
		# 					valid_pos, poses = self.place_cluster(board, one_side, other_side, direction, center)
		# 					if valid_pos:
		# 						return poses
		# 			visited.add(neighbour) 
		# 			queue.append(neighbour) 
		# # import pdb; pdb.set_trace()
		# return []


	def route(self, end_coordinates, board):
		curr_poses = {}
		moves = []
		positions = {}
		for dancerId, (x, y, colorType) in self.dancers.items():
			curr_poses[dancerId] = [x, y]
			board[x][y] = dancerId
		
		# import pdb; pdb.set_trace()
		turn_round = 0
		# import pdb; pdb.set_trace()
		while not self.finished(curr_poses, end_coordinates) and turn_round < 100:
			
			# if self.getOffCount(curr_poses, end_coordinates) < 5:
			# 	off_nodes = self.getOffNodes(curr_poses, end_coordinates)
			# 	import pdb; pdb.set_trace()



			curr_turn_other_viable_moves = {}
			moves_this_turn = {}
			moves_used = set()
			for dancerId in self.dancers.keys():
				if dancerId in moves_this_turn: continue
				curr_pos = curr_poses[dancerId]
				try:
					end_pos = end_coordinates[dancerId]
				except Exception as e:
					pass
					# import pdb; pdb.set_trace()
				# if len(end_coordinates) != len(self.dancers):
				# 	import pdb; pdb.set_trace()
				valid_moves = self.find_viable_moves(curr_pos, end_pos, board)
				for i in range(len(valid_moves)):
					if i == len(valid_moves): continue
					# if board[valid_moves[i][0]][valid_moves[i][1]] == 0 and (0 in moves_this_turn and valid_moves[i] != moves_this_turn[0]) and valid_moves[i] in moves_used:
					# 	import pdb; pdb.set_trace()
					if board[valid_moves[i][0]][valid_moves[i][1]] == 0 and valid_moves[i] not in moves_used:
						# if valid_moves[i] in moves_used:
						# 	import pdb; pdb.set_trace()
						moves_used.add(valid_moves[i])
						board[curr_pos[0]][curr_pos[1]] = 0
						board[valid_moves[i][0]][valid_moves[i][1]] = dancerId
						curr_poses[dancerId] = [valid_moves[i][0], valid_moves[i][1]]

						# dumb but this needs to come last because I am popping out the coordinate
						moves_this_turn[dancerId] = valid_moves.pop(i)
						curr_turn_other_viable_moves[dancerId] = valid_moves # keep this for later when we do tiebreaking
						break
					elif (board[valid_moves[i][0]][valid_moves[i][1]] > 0 and valid_moves[i] not in moves_used) or valid_moves[i] in moves_used and board[valid_moves[i][0]][valid_moves[i][1]] in moves_this_turn and valid_moves[i] == moves_this_turn[board[valid_moves[i][0]][valid_moves[i][1]]]:
						# try:
						other_dancer = board[valid_moves[i][0]][valid_moves[i][1]]
						if other_dancer in curr_turn_other_viable_moves and curr_pos in curr_turn_other_viable_moves[other_dancer]:
							# if curr_pos in moves_used:
							# 	import pdb; pdb.set_trace()
							moves_used.add(curr_pos)
							board[curr_pos[0]][curr_pos[1]] = other_dancer
						
							curr_poses[other_dancer] = [curr_pos[0], curr_pos[1]]
							moves_this_turn[other_dancer] = curr_pos 

							# if valid_moves[i] in moves_used:
							# 	import pdb; pdb.set_trace()
							moves_used.add(valid_moves[i])
							board[valid_moves[i][0]][valid_moves[i][1]] = dancerId
							curr_poses[dancerId] = [valid_moves[i][0], valid_moves[i][1]]
							moves_this_turn[dancerId] = valid_moves.pop(i)
							curr_turn_other_viable_moves[dancerId] = valid_moves 
						elif not other_dancer in curr_turn_other_viable_moves:
							tmp_board = copy.deepcopy(board)
							tmp_board[curr_pos[0]][curr_pos[1]] = 0
							valid_moves_other = self.find_viable_moves(valid_moves[i], end_coordinates[other_dancer], tmp_board)
							for index in range(len(valid_moves_other)):
								if index == len(valid_moves_other): continue
								# try:

									# board[valid_moves[i][0]][valid_moves[i][1]] == 0 and valid_moves[i] not in moves_used
								if valid_moves_other[index] == curr_pos or (valid_moves_other[index] not in moves_used and board[valid_moves_other[index][0]][valid_moves_other[index][1]] == 0):
								# if (board[valid_moves_other[i][0]][valid_moves_other[i][1]] == 0 and valid_moves_other[i] not in moves_used):

									# if valid_moves_other[index] in moves_used:
									# 	import pdb; pdb.set_trace()
									moves_used.add(valid_moves_other[index])
									board[valid_moves_other[index][0]][valid_moves_other[index][1]] = other_dancer
								
									curr_poses[other_dancer] = [valid_moves_other[index][0], valid_moves_other[index][1]]
									moves_this_turn[other_dancer] = valid_moves_other.pop(index)
									curr_turn_other_viable_moves[other_dancer] = valid_moves_other 
									board[curr_pos[0]][curr_pos[1]] = 0

									# if valid_moves[i] in moves_used:
									# 	import pdb; pdb.set_trace()
									moves_used.add(valid_moves[i])
									board[valid_moves[i][0]][valid_moves[i][1]] = dancerId
									curr_poses[dancerId] = [valid_moves[i][0], valid_moves[i][1]]
									moves_this_turn[dancerId] = valid_moves.pop(i)
									curr_turn_other_viable_moves[dancerId] = valid_moves # keep this for later when we do tiebreaking
								



								# except:
								# 	import pdb; pdb.set_trace()
							# for move in curr_turn_other_viable_moves[board[valid_moves[i][0]][valid_moves[i][1]]]:



			if moves_this_turn: 
				moves.append(moves_this_turn)
			turn_round += 1
		return moves


	def find_viable_moves(self, curr_pos, end_pos, board):
		valid_poses = []
		bad_poses = []
		for direction in self.directions:
			new_pos = (curr_pos[0] + direction[0], curr_pos[1] + direction[1])
			if self.is_closer(curr_pos, new_pos, end_pos):
				valid_poses.append(new_pos)

		return valid_poses

	def is_closer(self, curr_pos, new_pos, end_pos):
		return self.dist.pairwise([[curr_pos[0], curr_pos[1]], [end_pos[0], end_pos[1]]])[0][1] > self.dist.pairwise([[new_pos[0], new_pos[1]], [end_pos[0], end_pos[1]]])[0][1]

	def finished(self, curr_poses, end_coordinates):
		off_count = 0
		# if len(end_coordinates) != len(self.dancers):
		# 	import pdb; pdb.set_trace()
		for key, value in curr_poses.items():
			try:
				if end_coordinates[key][0] != value[0] and end_coordinates[key][1] != value[1]:
					off_count += 1
			except:
				pass
				# import pdb; pdb.set_trace()
		
		# print("Off count: ", off_count)

		if off_count > 0:
			return False

		return True

	def getOffCount(self, curr_poses, end_coordinates):
		off_count = 0
		# if len(end_coordinates) != len(self.dancers):
		# 	import pdb; pdb.set_trace()
		for key, value in curr_poses.items():
			try:
				if end_coordinates[key][0] != value[0] and end_coordinates[key][1] != value[1]:
					off_count += 1
			except:
				pass
				# import pdb; pdb.set_trace()

		if off_count > 0:
			return off_count

		return 0

	def getOffNodes(self, curr_poses, end_coordinates):
		off_nodes = []
		# if len(end_coordinates) != len(self.dancers):
		# 	import pdb; pdb.set_trace()
		for key, value in curr_poses.items():
			try:
				if end_coordinates[key][0] != value[0] and end_coordinates[key][1] != value[1]:
					off_nodes.append(key)
			except:
				pass
				# import pdb; pdb.set_trace()

		return off_nodes



	def place_cluster(self, board, one_side, other_side, direction, center):
		poses = []
		if direction == 0: # horizontal
			for i in range(1, one_side + 1):
				test_pos = (center[0] + i, center[1])
				if (test_pos[0] >= self.board_size or test_pos[1] >= self.board_size) or board[test_pos[0]][test_pos[1]] != 0:
					return False, []
				poses.append(test_pos)

			for i in range(1, other_side + 1):
				test_pos = (center[0] - i, center[1])
				if test_pos[0] < 0 or test_pos[1] < 0 or board[test_pos[0]][test_pos[1]] != 0:
					return False, []
				poses.append(test_pos)
		else: # vertical
			for i in range(1, one_side + 1):
				test_pos = (center[0], center[1] + i)
				if test_pos[0] >= self.board_size or test_pos[1] >= self.board_size or board[test_pos[0]][test_pos[1]] != 0:
					return False, []
				poses.append(test_pos)

			for i in range(1, other_side + 1):
				test_pos = (center[0], center[1] - i)
				if test_pos[0] < 0 or test_pos[1] < 0 or board[test_pos[0]][test_pos[1]] != 0:
					return False, []
				poses.append(test_pos)
		return True, poses

	def within(self, centerPoint, obstacle, targetPoint):
		return centerPoint <= obstacle <= targetPoint or targetPoint <= obstacle <= centerPoint

	def set_up_board(self, stars, clusters, centerType):
		board = [[0 for i in range(self.board_size)] for j in range(self.board_size)]

		for star in stars:
			board[star[0]][star[1]] = -1

		for cluster in clusters:
			x, y, color = self.dancers[cluster]
			if color == centerType:
				board[x][y] = -2 
		return board

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
	k = int(parameters_l[2]) # max num of stars
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
				__dancers[id] = (nx, ny, color)

			client.send(move_str)

		# send DONE flag
		client.send("DONE")
		client.send(getLines(num_color, __dancers))

	# close connection
	client.close()

def getLines(num_color, dancers):
	nonvis = {}
	for x,y,c in dancers.values():
		nonvis[(x, y)] = c
	lines = []
	dx = [1, -1, 0, 0]
	dy = [0, 0, 1, -1]
	while True:
		if len(nonvis) == 0:
			break
		removing = set()
		endpoints = set()
		for x, y in nonvis:
			cnt = 0
			dir = -1
			for i in range(4):
				xx = x + dx[i]
				yy = y + dy[i]
				if (xx, yy) in nonvis:
					cnt += 1
					dir = i
			if cnt == 0:
				return "0 0 0 0"
			elif cnt == 1:
				nx = x + dx[dir]*(num_color-1)
				ny = y + dy[dir]*(num_color-1)
				if (nx, ny) not in endpoints and (x,y) not in endpoints:
					isGood = True
					colors = set()
					for cc in range(num_color):
						ix = x + dx[dir]*cc
						iy = y + dy[dir]*cc
						if (ix, iy) not in nonvis:
							isGood = False
						else:
							colors.add(nonvis[(ix, iy)])
					if len(colors) != num_color:
						isGood = False
					if isGood:
						endpoints.add((nx, ny))
						endpoints.add((x, y))
						lines.append((x, y, nx, ny))
						for cc in range(num_color):
							ix = x + dx[dir]*cc
							iy = y + dy[dir]*cc
							removing.add((ix, iy))
		if len(removing) == 0:
			break
		for x,y in removing:
			del nonvis[(x,y)]
	if len(lines) == 0:
		return "0 0 0 0"
	res = ""
	for line in lines:
		for coor in line:
			res += str(coor) + " "
	return res

if __name__ == "__main__":
	main()
