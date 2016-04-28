var google_apis = (function() {

   var KEY = null;

   function new_game() {
      gapi.client.hnefatafl.new_game().execute(function(response){
         KEY = response.key;
         board.new_board(JSON.parse(response.board));
      });
   }
   function player_move(cell_from, cell_to) {
      gapi.client.hnefatafl.player_move({
         "game_key": KEY,
         "cell_from": cell_from,
         "cell_to": cell_to
      }).execute(function(response){
         console.log(response.board);
         //parse_board(response.board);
         //change_board();
         //ai_move(false);
      });

   }

      function ai_move(first) {
         alert('ai_move');
         gapi.client.hnefatafl.ai_move({"game_key":KEY}).execute(function(response){
            parse_board(response.board);
            if(first) new_board();
            else change_board();
         });
      }
      return {new_game, player_move};
})();


		function ai_move(first) {
			alert('ai_move');
			gapi.client.hnefatafl.ai_move({"game_key":KEY}).execute(function(response){
				parse_board(response.board);
				if(first) new_board();
				else change_board();
			});
		}


		function api_player_move(cell_from, cell_to) {
			alert('player_move');
			gapi.client.hnefatafl.player_move({
				"game_key": KEY,
				"cell_from": cell_from,
				"cell_to": cell_to
			}).execute(function(response){
				parse_board(response.board);
				change_board();
				ai_move(false);
			});

		}

		function parse_board(board) {
			var b = board.replace(/(],)+/g, '|'); //  split('],');
			b = b.replace(/[\[\]]+/g, ''); //replace(/(],)+/g, '');
			b = b.split('|');
			s = [];
			for(var i=0; i < b.length; i++) {
				var row = b[i].split(',');
				var push_row = [];
				for(var y=0; y < row.length; y++) {
					push_row.push(parseInt(row[y].trim()));
				}
				s.push(push_row);
			}
      }
