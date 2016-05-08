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

* The board consists of 9x9 squares/cells. 
  
  Each cell's position is labeled as (row index, column index). *i.e.* the top left cell is **(0,0)** and the bottom right cell is **(8,8)**.  *The board values are store as an array of arrays*

  Each cell's value is represented as:
  
  Piece | Value
  --- | ---
  Empty | 0
  Attacker | 1
  Defender | 2
  King | 3
  
* You may make one move per turn.  You can move any of your pieces to any cell in a straight line.

* To capture an opposition piece, you must move your pieces on the opposite of an opponent's.
  *Note that if you move your piece inbetween two opponent pieces, it won't be captured.*

* To capture the king, you must surround it on four sides by attacking pieces, or on three sides if the fourth side is occupied by a defender piece.

## API Endpoints

Most of the endpoints require OAuth 2 autherization.  It will request the user's name and email address.
If no parameter is defined, it means it accepts none

* **new_game**
  * Creates a new game for the current user.
  * Returns the details of the newly created game:
    * ```key```           = datastore id
    * ```player_email```
    * ```board```         = the values of the board
    * ```state```         = the state of the game.  0: Player's turn. 1: AI's turn. 2: Player won. 3: AI won.
     
* 


