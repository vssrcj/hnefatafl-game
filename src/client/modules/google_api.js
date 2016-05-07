var google_apis = (function() {

   var KEY = null;

   function new_game() {
      gapi.client.hnefatafl.new_game().execute(function(response){
         KEY = response.key;
         board.new_board(JSON.parse(response.board));
         ai_move();
      });
   }

   function last_player_game() {

      gapi.client.hnefatafl.last_player_game().execute(function(response){
         console.log(response);
         if(response.code == 404) {
            new_game();
         }
         else {
            KEY = response.key;
            board.new_board(JSON.parse(response.board));
            var state = parseInt(response.state);
            if(!board.game_end(state))
               if(state == 1) ai_move();
         }
      });
   }

   function player_move(origin, destination) {
      var origins = origin.split(',');
      var destinations = destination.split(',');

      gapi.client.hnefatafl.player_move({
         "game_key": KEY,
         "origin_row": origins[0],
         "origin_column": origins[1],
         "destination_row": destinations[0],
         "destination_column": destinations[1]
      }).execute(function(response){
         console.log(response);
         board.move(
            response.origin_value,
            response.origin,
            response.destination,
            response.captures != "[]" ?
            JSON.parse(
               response.captures.replace('(','[').replace(')',']')
            ): null
         );
         if(!board.game_end(parseInt(response.game_state))) {
            ai_move();
         }
      });
   }

      function ai_move() {
         gapi.client.hnefatafl.ai_move({
            "game_key":KEY
         }).execute(function(response){
            console.log(response);
            board.move(
               response.origin_value,
               response.origin,
               response.destination,
               response.captures != "[]" ?
               JSON.parse(
                  response.captures.replace('(','[').replace(')',']')
               ): null
            );
            board.game_end(parseInt(response.game_state));
         });
      }
      return {
         new_game: new_game,
         player_move: player_move,
         ai_move: ai_move,
         last_player_game: last_player_game
      };
})();
