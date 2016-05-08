# Hnefatafl

*By [CJ](https://github.com/vssrcj)*

This project exposes platform agnostic API's for the Hnefatafl game using Google App Engine backed by Google Datastore.

It also includes a client (web) platform, that consumes some of the endpoints, to showcase the API's.

You can find the web app [here](https://hnefatafl-game.appspot.com)
and the API Explorer [here](https://hnefatafl-game.appspot.com/_ah/api/explorer)

## How to play

* In this version you as the player (the attacker) face off against an AI (the defender).
  The goal for the defender is to get the king piece to any edge cell of the board.
  The goal for the attacker is to capture the king piece.

* The board consists of 9x9 squares. 
  Each cell/square is labeled as (row index, column index). i.e. the top left cell is (0,0) and the bottom right cell is (8,8).
  The attacker pieces are labeled as 1
  The defender pieces are labeled as 2, and the king as 3
  Empty pieces are labeled as 0
  
* You may make one move per turn.  You can move any of your pieces to any cell in a straight line.

* To capture an opposition piece, you must move your pieces on the opposite of an opponent's.
  Note that if you move your piece inbetween two opponent pieces, it won't be captured.
  
* To capture the king, you must surround it on four sides by attacking pieces, or on three sides if the fourth side is occupied by a defender piece.
