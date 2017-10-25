#!/usr/bin/python
import sys, socket, time, os
from Server import Server
from copy import deepcopy
from getopt import getopt

"""
Usage: python3 game.py -H <host> -p <port> -f <filename> -s <size>
"""


class Game(object):

  def __init__(self, host, port, input_file, size):
    """Initialize game"""
    # read file input
    self.file_input, self.dancers = self.__process_input(input_file)
    # setup board
    self.board_size = size
    self.num_color = len(self.dancers)
    self.board = self.__setup_board(self.dancers, size)
    self.stars = set()
    self.k = len(self.dancers[0]) # the max number of stars
    self.dancer_steps = 0
    # initialize server
    self.server, self.choreographer, self.spoiler = self.__setup_server(host, port)

  def __setup_server(self, host, port):
    server = Server(host, port)
    choreographer, spoiler = server.establish_connection()
    return server, choreographer, spoiler # return server and both players' name

  def __process_input(self, filename):
    """read in input file"""
    f = open(filename)
    file_input = ""
    dancers = list()
    cur = -1
    for line in f:
      file_input += line
      tokens = line.split()
      if len(tokens) == 0:
        continue # skip empty lines
      elif len(tokens) == 2:
        dancers[cur].add((int(tokens[0]), int(tokens[1])))
      else:
        cur = int(tokens[len(tokens) - 1]) - 1
        dancers.append(set())
    return file_input, dancers

  def __setup_board(self, dancers, size):
    """Initialize board"""
    # fill all the space with 0
    board = [[0 for i in range(size)] for j in range(size)]
    # fill in all the dancers with their colors
    for index in range(len(dancers)):
      for pos in dancers[index]:
        board[pos[0]][pos[1]] = index + 1
    return board

  def __inside_board(self, x, y):
    """check if this position is inside board"""
    if x not in range(self.board_size) or y not in range(self.board_size):
      return False
    return True

  def __manhattan_distance(self, x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

  def __is_star_valid(self, x, y):
    """
    Check if it is valid to place a start at this position\n
    1. Star can be only placed in an empty spot\n
    2. two stars cannot closer then c+1 manhattan distance
    """
    # if it is a valid position on board
    if not self.__inside_board(x, y):
      print("Star not inside board")
      return False # outside board
    # check if it is an empty spot
    if self.board[x][y] == 0:
      valid = True
      # check manhattan distance with other stars
      for s in self.stars:
        if self.__manhattan_distance(s[0], s[1], x, y) < self.num_color + 1:
          print("Manhattan distance not satisfied with " + str(s[0]) + ", " + str(s[1]))
          valid = False # manhattan distance can't smaller than c + 1
          break
      return valid
    else: # not an empty spot
      return False

  def __is_dancer_move_valid(self, start_x, start_y, end_x, end_y):
    """
    Check if this dancer move is valid\n
    1. dancer cannot move to a position that has a star\n
    2. dancer cannot move to a position outside the board
    """
    # check if both positions are inside the board
    if not (self.__inside_board(start_x, start_y) and self.__inside_board(end_x, end_y)):
      print("Position outside board")
      return False # one of points outside board
    # check if there is a dancer at the start position
    elif self.board[start_x][start_y] in (0, -1):
      print("no dancer at this start location")
      return False # no dancer at this location
    # check if start == end
    elif start_x == end_x and start_y == end_y:
      print("no movement at all")
      return False # no movement at all
    # check if the dancer will move to a star
    elif self.board[end_x][end_y] == -1:
      print("There is a star at end location")
      return False # there is a star at end location
    else:
      return True

  def __check_finish(self):
    """check if the current game is finished"""
    return self.__is_game_finish(self.board, self.dancers)

  def __check_one_direction(self, start_x, start_y, x_act, y_act, board, dancers):
    """
    direction means vertically or horizontally\n
    it depends on x_act and y_act\n
    This function will start with a node\n
    move to one end of this line and start checking if this line contains all colors.
    """
    n_board = deepcopy(board)
    n_dancers = deepcopy(dancers)
    cur_x = start_x
    cur_y = start_y
    # move to one end first
    while n_board[cur_x+x_act][cur_y+y_act] not in (0, -1):
      cur_x += x_act
      cur_y += y_act
    # start to check one by one, use a set to keep track of color
    colorset = set()
    while n_board[cur_x][cur_y] not in (0, -1) and n_board[cur_x][cur_y] not in colorset:
      c = n_board[cur_x][cur_y]
      colorset.add(c)
      n_board[cur_x][cur_y] = 0 # unmark
      n_dancers[c-1].remove((cur_x, cur_y)) # remove from set
      cur_x -= x_act # move towards the other end
      cur_y -= y_act
    # check if set contains all the colors
    if len(colorset) == self.num_color:
      return True, n_board, n_dancers
    else:
      return False, n_board, n_dancers

  def __is_game_finish(self, board, dancers):
    """Check if this game state is finished"""
    # check if all dancers are removed
    empty = True
    index = 0
    for i in range(len(dancers)):
      group = dancers[i]
      index = i
      if len(group) != 0:
        empty = False
        break
    if empty:
      return True
    # not empty, pick one dancer from group
    start = next(iter(dancers[index]))
    cur_x = start[0]
    cur_y = start[1]
    # check vertically
    validline, n_board, n_dancers = self.__check_one_direction(cur_x, cur_y, -1, 0, board, dancers)
    if validline:
      return self.__is_game_finish(n_board, n_dancers)
    # check horizontally
    validline, n_board, n_dancers = self.__check_one_direction(cur_x, cur_y, 0, -1, board, dancers)
    if validline:
      return self.__is_game_finish(n_board, n_dancers)
    # not valid still not finish
    return False

  def __place_stars(self, stars):
    """
    Place a list of stars on the board\n
    return true if success and false and error message if fail
    """
    success = True
    msg = None
    for s in stars:
      if self.__is_star_valid(s[0], s[1]):
        self.stars.add(s)
        self.board[s[0]][s[1]] = -1 # mark it on board
      else:
        success = False
        msg = "Spoiler placed an invalid star at: " + str(s[0]) + ", " + str(s[1])
        break
    return success, msg
  
  def __update_dancers(self, moves):
    """
    Make a list of parallel movements.\n
    Those movements count as 1 step since they happen at the same time.
    """
    self.dancer_steps += 1
    success = True
    msg = None
    moved = set()
    for m in moves:
      # start pos
      x1 = m[0]
      y1 = m[1]
      # end pos
      x2 = m[2]
      y2 = m[3]
      # check if this dancer has already been moved
      # also check the end position
      # because if the end position is moved then we can't swap them
      if (x1, y1) in moved or (x2, y2) in moved:
        success = False
        msg = "Choreographer attempt to move a dance twice in one move from " + str(x1) + ", " + str(y1) \
          + " to " + str(x2) + ", " + str(y2)
        break
      if self.__is_dancer_move_valid(x1, y1, x2, y2):
        # make the move
        s_c = self.board[x1][y1] # color of start point
        e_c = self.board[x2][y2] # color of end point
        if s_c != e_c: # they have the same color then nothing need to be done
          # check if there is a dancer at end point
          if e_c != 0:
            self.dancers[e_c-1].remove((x2, y2))
            self.dancers[e_c-1].add((x1, y1))
            moved.add((x1, y1))
          self.dancers[s_c-1].remove((x1, y1))
          self.dancers[s_c-1].add((x2, y2))
          moved.add((x2, y2))
          self.board[x1][y1], self.board[x2][y2] = e_c, s_c # swap them on board
      else:
        success = False
        msg = "Choreographer made an invalid move from " + str(x1) + ", " + str(y1) \
          + " to " + str(x2) + ", " + str(y2)
        break
    return success, msg

  def get_board(self):
    """Get the current board"""
    return self.board

  def start_game(self):
    # send input file to both players
    print("Sending input file to both players...")
    self.server.send_all(self.file_input)

    # send other parameters to both players
    # board size, numOfColor, k
    print("Sending other parameters to both players...")
    self.server.send_all(str(self.board_size) + " " + str(self.num_color) + " " + str(self.k))

    # now wait for spoiler to send stars
    print("Waiting for spoiler to send the stars...")
    start_time = time.time()
    star_data = ""
    while not star_data:
      star_data = self.server.receive(1)
    end_time = time.time()
    print(star_data)
    if time.time() - start_time > 120:
      print("Spoiler exceeds time limit!")
      sys.exit()
    print("Received stars!")

    # parse stars
    s_list = star_data.split()
    stars = list()
    for i in range(int(len(s_list)/2)):
      stars.append((int(s_list[2*i]), int(s_list[2*i+1])))
    print(stars)

    print("Adding stars to the board...")
    # process stars
    success, msg = self.__place_stars(stars)
    if not success:
      print(msg)
      sys.exit()
    print("Done.")

    # send stars to choreographer
    print("Sending stars to the choreographer...")
    self.server.send_to(0, star_data)

    # receive moves from choreographer
    print("Receiving moves from choreographer...")
    start_time = time.time()
    move_data = ""
    while True:
      if time.time() - start_time > 120:
        print("Choreographer exceeds time limit!")
        self.server.close()
        sys.exit()
      # receive data
      data = self.server.receive(0)
      print(data)
      if data == "DONE": # received DONE flag
        break
      move_data += data

    # parse move data
    md_l = move_data.split()
    steps = list()
    while len(md_l) != 0:
      # get the move count
      c = int(md_l.pop(0))
      moves = list()
      for i in range(c):
        x1 = md_l.pop(0)
        y1 = md_l.pop(0)
        x2 = md_l.pop(0)
        y2 = md_l.pop(0)
        moves.append([int(x1), int(y1), int(x2), int(y2)])
      steps.append(moves)
    
    # now execute the moves
    for m in steps:
      move_success, msg = self.__update_dancers(m)
      if not move_success:
        print(msg) # invalid move
        self.server.close()
        sys.exit()
    
    # check if the choreographer has reached the goal
    if self.__check_finish():
      print("Game finished!")
      print(self.choreographer + " has taken " + self.dancer_steps + " steps.")
    else:
      print("Game finished!")
      print(self.choreographer + " didn't reach the goal.")
    self.server.close()

def print_usage():
  print("Usage: python3 game.py -H <host> -p <port> -f <filename> -s <size>")

def main():
  host = None
  port = None
  filename = None
  size = None
  try:
    opts, args = getopt(sys.argv[1:], "hH:p:f:s:", ["help"])
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
    elif opt == "-f":
      filename = arg
    elif opt == "-s":
      size = int(arg)
  # initialize game    
  game = Game(host, port, filename, size)
  # run game
  game.start_game()

if __name__ == "__main__":
  main()