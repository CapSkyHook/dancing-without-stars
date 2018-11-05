#!/usr/bin/python
import sys, random
from copy import deepcopy
from client import Client
from getopt import getopt, GetoptError
import heapq 
from sklearn.neighbors import DistanceMetric
from sklearn.metrics.pairwise import pairwise_distances
from operator import itemgetter
import collections

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
        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self.board = [[False for i in range(0, self.board_size)] for j in range(0, self.board_size)]
        # arr_patients = [ [patient[0], patient[1]] for dancier in self.danciers.values()]

        # D = pairwise_distances(arr_patients, metric='manhattan')

<<<<<<< HEAD
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
		clusters, centers = self.get_clusters(stars)
		print("Got clusters")
		end_coordinates, board = self.place_clusters(clusters, stars, centers)
		print("Got end_coordinates")

		# CURRENT THIS PLATEAUS AT 42 PEOPLE SO NEED TO DO A LITTLE MORE
		move = self.route(self.dancers, end_coordinates, board)
		import pdb; pdb.set_trace()
		return move


	def place_clusters(self, clusters, stars, centers):
		centerType = self.dancers[centers[1]][2]
		board = self.set_up_board(stars, clusters, centerType)
		clusters_by_distance = sorted(list(clusters.values()), key=itemgetter('distance'), reverse=True) 
		final_poses = {}
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

			for key, position in best_positions.items():
				final_poses[key] = position
				if key != center:
					board[position[0]][position[1]] = key
		return final_poses, board

	def route(self, dancers, end_coordinates, oriboard):
		curr_poses = {}
		moves = []
		positions = {}
		for dancerId, (x, y, colorType) in dancers.items():
			curr_poses[dancerId] = [x, y]
			board[x][y] = dancerId
		
		# import pdb; pdb.set_trace()
		turn_round = 0
		bfs = []
		limit = maxiter #some number
		while not self.finished(curr_poses, end_coordinates):
			# import pdb; pdb.set_trace()
			curr_turn_other_viable_moves = {}
			moves_this_turn = {}
			best_move = {}
			'''for dancerId in self.dancers.keys():
				if dancerId in moves_this_turn: continue
				curr_pos = curr_poses[dancerId]
				try:
					end_pos = end_coordinates[dancerId]
				except Exception as e:
					import pdb; pdb.set_trace()

				valid_moves = self.find_viable_moves(curr_pos, end_pos, board)

				for i in range(len(valid_moves)):
					if board[valid_moves[i][0]][valid_moves[i][1]] == 0:
						board[curr_pos[0]][curr_pos[1]] = 0
						board[valid_moves[i][0]][valid_moves[i][1]] = dancerId
						curr_poses[dancerId] = [valid_moves[i][0], valid_moves[i][1]]

						# dumb but this needs to come last because I am popping out the coordinate
						moves_this_turn[dancerId] = valid_moves.pop(i)
						curr_turn_other_viable_moves[dancerId] = valid_moves # keep this for later when we do tiebreaking
						#bfs.append(valid_moves)
						break
					
			moves.append(moves_this_turn)
			turn_round += 1'''

			it = 0
			while it < int(len(self.dancers)/2):
				#for move_this_turn, we try to start from different dancers, we could control the number of start point it
				# reason for this is becasuse although we start from dancerid = 0 in each turn move, we still likely get a 
				# move_this_turn less than len(self.dancer)
				#this mainly wants to spend more time in move_this_turn
				bfs = self.find_viable_moves(curr_poses[it], end_coordinates[it], board)

    # incase dancer = it don't have availiable neighbor to move
				while len(bfs) == 0 and it < len(self.dancers):
					it += 1
					bfs = self.find_viable_moves(curr_poses[it], end_coordinates[it], board)

				while len(bfs) > 0:
					board = oriboard
					moves_this_turn[it] = bfs.pop()
					for dancerId in range(it+1, int(len(self.dancers))):
						curr_pos = curr_poses[dancerId]
						end_pos = end_coordinates[dancerId]
				  '''try:
					  end_pos = end_coordinates[dancerId]
				  except Exception as e:
					  import pdb; pdb.set_trace()'''

					valid_moves = self.find_viable_moves(curr_pos, end_pos, board)

						for i in range(len(valid_moves)):
							if board[valid_moves[i][0]][valid_moves[i][1]] == 0:
								board[curr_pos[0]][curr_pos[1]] = 0
								board[valid_moves[i][0]][valid_moves[i][1]] = dancerId
								curr_poses[dancerId] = [valid_moves[i][0], valid_moves[i][1]]

						# dumb but this needs to come last because I am popping out the coordinate
								moves_this_turn[dancerId] = valid_moves[i]
						 #curr_turn_other_viable_moves[dancerId] = valid_moves # keep this for later when we do tiebreaking
						#bfs.append(valid_moves)
						#for one loop of move_this_turn, once we find a valid move for one dancer, we go to next(not sure here)
								break

						if len(moves_this_turn) > len(best_move):
							best_move = moves_this_turn

				it += 1
				move.append(best_move)

		return moves


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
=======
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
        clusters, centers = self.get_clusters(stars)
        print("Got clusters")
        end_coordinates, board = self.place_clusters(clusters, stars, centers)
        print("Got end_coordinates")

        # CURRENT THIS PLATEAUS AT 42 PEOPLE SO NEED TO DO A LITTLE MORE
        moves = self.route(end_coordinates, board)
        
        for move in moves:
            foo = set()
            for dancerId, coord in move.items():
                # import pdb; pdb.set_trace()
                if coord not in foo:
                    foo.add(coord)
                else:
                    import pdb; pdb.set_trace()
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

            if (self.num_color != len(best_positions) and len(best_positions) > 0 ) or not found_one:
                import pdb; pdb.set_trace()
            for key, position in best_positions.items():
                final_poses[key] = position
                if key != center:
                    board[position[0]][position[1]] = key
        if len(final_poses) != len(self.dancers):
            import pdb; pdb.set_trace()


        # If we can't place a cluster, place them anywhere
        for cluster in positions_not_found:

            poses = self.place_cluster_anywhere_close(board, self.dancers[center])

            for dancerId, distance_deprecated in cluster.items():
                final_poses[key] = poses.pop()
                if key != center:
                    board[final_poses[key][0]][final_poses[key][1]] = key

        return final_poses, board


    def place_cluster_anywhere_close(board, center):
        visited, queue = set(), collections.deque([center])
        while queue: 
            vertex = queue.popleft()
            for coord in [(vertex[0] + x, vertex[1] + y) for x, y in self.directions]: 
                if coord not in visited and board[coord[0]][coord[1]] == 0:
                    for direction in range(2):
                        for one_side in range(self.num_color):
                            other_side = self.num_color - 1 - one_side 
                            valid_pos, poses = self.place_cluster(board, one_side, other_side, direction, center)
                            if valid_pos:
                                return poses
                    visited.add(neighbour) 
                    queue.append(neighbour) 
        import pdb; pdb.set_trace()
        return []


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
            # import pdb; pdb.set_trace()
            curr_turn_other_viable_moves = {}
            moves_this_turn = {}
            moves_used = set()
            for dancerId in self.dancers.keys():
                if dancerId in moves_this_turn: continue
                curr_pos = curr_poses[dancerId]
                try:
                    end_pos = end_coordinates[dancerId]
                except Exception as e:
                    import pdb; pdb.set_trace()
                if len(end_coordinates) != len(self.dancers):
                    import pdb; pdb.set_trace()
                valid_moves = self.find_viable_moves(curr_pos, end_pos, board)

                for i in range(len(valid_moves)):
                    if board[valid_moves[i][0]][valid_moves[i][1]] == 0 and valid_moves[i] in moves_used:
                        import pdb; pdb.set_trace()
                    if board[valid_moves[i][0]][valid_moves[i][1]] == 0 and valid_moves[i] not in moves_used:
                        moves_used.add(valid_moves[i])
                        board[curr_pos[0]][curr_pos[1]] = 0
                        board[valid_moves[i][0]][valid_moves[i][1]] = dancerId
                        curr_poses[dancerId] = [valid_moves[i][0], valid_moves[i][1]]

                        # dumb but this needs to come last because I am popping out the coordinate
                        moves_this_turn[dancerId] = valid_moves.pop(i)
                        curr_turn_other_viable_moves[dancerId] = valid_moves # keep this for later when we do tiebreaking
                        break
            if moves_this_turn: 
                moves.append(moves_this_turn)
            turn_round += 1
        return moves


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
        if len(end_coordinates) != len(self.dancers):
            import pdb; pdb.set_trace()
        for key, value in curr_poses.items():
            try:
                if end_coordinates[key][0] != value[0] and end_coordinates[key][1] != value[1]:
                    off_count += 1
            except:
                import pdb; pdb.set_trace()
        
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
                        #   continue
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
>>>>>>> 4877cddf0ed42aa28d53ebcf64bcad717d657b8d



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
            # print(move)
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
