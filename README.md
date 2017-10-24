Dancing without Stars
=====================

## Details
On a `N x N` checker board, there are `c` groups of dancers in their initial positions. Each group will have a unique color and each group have `k` dancers.  

The choreographer is going to ask the dancers to make moves. The goal of the choreographer is to ensure that there are disjoint, contiguous vertical or horizontal line segments of dancers.  

For example, there are color `1`, `2`, `3`, `4`, and `k = 3`, then the following is a valid final state:
```
1234  1 
      2
1234  3
      4
```

The spoiler is going to place `k` stars on the board before choreographer starts to move, and try make choreographer to spend more steps to reach a final state.

Both players will have `120` seconds as thinking time.

## Choreographer
Choreographer will connect to server first. Server will send an `input_file` to choreographer. An `input_file` is similiar to `sample_dancedata.txt`.  

Server will then send some other parameters to Choreographer:  
`<board_size> <num_of_color> <k>`

After spoiler has placed all the stars, server will send choreographer all the stars in the following format:  
`<star_1_x> <star_1_y> <star_2_x> <star_2_y> ..... <star_k_x> <star_k_y>`  

The server will start counting time immediately after sending stars.  

The choreographer needs to send steps of parallel moves to the server. One `step` contains multiple `parallel move`s. Those dancers like to move at the same time that's why it's called "parallel". However, one dancer cannot move twice within one `step`. And no dancer can move on to a star. They can only move to an empty position or swap positions.  

Choreographer needs to send the steps one by one to the server in the following format:  
`<num_of_moves> <move1_start_x> <move1_start_y> <move1_end_x> <move1_end_y> ... <moveK_start_x> <moveK_start_y> <moveK_end_x> <moveK_end_y>`

Choreographer needs to send a flag `DONE` to the server when all the steps are sent.

## Spoiler
Spoiler will be the second to connect to the server. Server will send the `input_file` such like `sample_dancedata.txt` to the spoiler first.  

Server will then send the other parameters to spoiler same as what server will do to choreographer:  
`<board_size> <num_of_color> <k>`

The spoiler needs to send stars to the server in the following format:  
`<star_1_x> <star_1_y> <star_2_x> <star_2_y> ..... <star_k_x> <star_k_y>`  

Stars can only be placed on an empty spot.

And then spoiler can rest.

## Run the server
```bash
python3 game.py -H <host> -p <port> -f <filename> -s <size>
```  
Where `size` means the board size.

## Run the sample player
For Choreographer
```bash
python3 sample_player.py -H <host> -p <port> -s
```
For spoiler
```bash
python3 sample_player.py -H <host> -p <port> -c
```

Both uses randomized methods, so sample choreographer can hardly reach the goal.

## Scoring
Two players will play as choreographer and spoiler in turns.  
The player who make an invalid move will lose that round.
If each player lost a round then its a draw.  
If no one made any invalid move then the one choreographer who uses fewer steps will win.

## Graphic Interface
Under construction...

## Contact
Let me know if there is any bugs or problems.  
`taikun@nyu.edu`