var board = (function() {

   let $board = $("#board");
   let $board_header = $("#board_header");
   let $new_game = $("#new_game");

   const HEIGHT = 9;
   const WIDTH = 9;

   var board;

   var $selected = null;

   const typeNames = [
      'empty',
      'attacker',
      'defender',
      'king'
   ];

   function onClick() {
      var $cell = $(this);
      var type = $cell.attr('class');

      if(type == "attacker") {
         if($selected) {
            $selected.attr('class','attacker');
            $selected = null;
         }
         else {
            $cell.attr('class','attacker-select');
            $selected = $cell;
         }
      }
      else if($selected){
         if(type == "empty") {
            google_apis.player_move(
               $selected.attr('id'),
               $cell.attr('id')
            )
            $selected = null;
         }
         else {
            $selected.attr('class','attacker');
            $selected = null;
         }
      }
   }
   function new_game() {
         $board.on('click','.row > div > div', onClick);
      google_apis.new_game();
      $board_header.hide();
   }
   $new_game.on('click',new_game);
   function cellClick(target, params) {

   }

   function game_end(game_state) {
      if(game_state == 2 || game_state == 3) {
         if(game_state == 2){
            $board_header.append("Player won!")
            $board_header.addClass("attacker-header");
         }
         else {
             $board_header.addClass("defender-header");
             $board_header.append("AI won!");
          }
         $board.off();
         $board_header.removeClass('hidden');
         return true;
      }
      return false;
   }

   function empty_board() {

      $board = $("#board");
      var table_builder = "";
   	for(var row=0; row< HEIGHT; row++){
         var row_builder = "<div class='row'>";
   		for(var col=0; col< WIDTH; col++) {
            row_builder += "<div><div data-val='0' class='empty' id='" + row + "," + col + "'></div></div>";
   		}
         row_builder += "</div>";

         table_builder += row_builder;
   	}

      $board.append(table_builder);

      $board.on('click','.row > div > div', onClick);

   }

   function fadeInNewClass(source, from_class, to_class) {
      source.switchClass(from_class, to_class, 1000);
   }

   function move(origin_value, origin, destination, captures) {
      var or = document.getElementById(origin);
      var $or = $(or);
      $or.attr('class',typeNames[0]);

      var de = document.getElementById(destination);
      var $de = $(de);
      $de.attr('class',typeNames[origin_value]);

      if(captures && captures[0]) {

         for(var i=0; i< captures.length; i++) {
            f = captures[i][0];
            t = captures[i][1];
            console.log(f);
            var ca = document.getElementById(f + "," + t);
            var $ca = $(ca);
            $ca.attr('class',typeNames[0]);
         }
      }
   }

   function new_board(board) {
      board = board;
   	for(var row=0; row < board.length; row++){
         var columnWidth = board[row].length;
   		for(var col=0; col < columnWidth; col++) {
            var val = board[row][col];

               var t = document.getElementById(row + "," + col);

               var $cell = $(t);

               $cell.attr('class',typeNames[val]);

   		}
   	}

   }

   function make_move(from_r, from_c, to_r, to_c, captures, value) {

      board[from_r][from_c] = 0;
      board[to_r][to_c] = value;
      $("#" + from_r + "," + from_c).attr('class','empty');
      $("#" + to_r + "," + to_c).attr('class',typeNames[value]);
      for(var capture in captures) {
         var r = capture[0];
         var c = capture[1];
         board[r][c] = 0;
         $("#" + r + "," + c).attr('class','empty');
      }

   }

         return {empty_board , new_board , move, game_end};
})();

//
// function change_board() {
// 	for(var row=0; row< BOARD.length; row++){
// 		for(var col=0; col< BOARD[row].length; col++) {
//
// 			var val = BOARD[row][col];
// 			var rect = document.getElementById(row + ',' + col);
//
// 			if(val == '0') cls = 'empty';
// 			else if(val == '1') cls = 'attacker';
// 			else if(val == '2') cls = 'defender';
// 			else if(val == '3') cls = 'king';
// 			rect.setAttribute('class',cls);
// 		}
// 	}
// }
//
//
//
// $(function() {
//
//
// 	var from_cell = null;
//
// 	$("body").on("click","rect",function(){
//
// 		var cls = $(this).attr('class');
// 		//console.log(cls);
// 		//console.log(from_cell);
// 		if (cls == "empty" && from_cell != null) {
//
// 			var to_cell = $(this).attr('id').split(',');
// 			to_cell[0] = parseInt(to_cell[0]);
// 			to_cell[1] = parseInt(to_cell[1]);
//
// 			if (from_cell[0] == to_cell[0]) {
// 				console.log(from_cell);		// same row
// 				if(from_cell[1] < to_cell[1]) {				// goes right
// 					x = from_cell[1] + 1;
// 					console.log(x);
// 					while(x <= to_cell[1]) {
// 						console.log(x);
// 						if(BOARD[from_cell[0]][x] != 0) {
// 							return clear();
// 						}
// 						x++;
// 					}
// 				}
// 				else if(from_cell[1] > to_cell[1]) {		// goes left
// 					x = from_cell[1] - 1;
// 					while(x >= to_cell[1]) {
// 						if(BOARD[from_cell[0]][x] != 0) {
// 							return clear();
// 						}
// 						x--;
// 					}
// 				}
// 				else return clear();
// 			}
// 			else if (from_cell[1] == to_cell[1]) {		// same column
// 				if(from_cell[0] > to_cell[0]) {				// goes up
// 					y = from_cell[0] + 1;
// 					while(y <= to_cell[0]) {
// 						if(BOARD[y][cell[1]] != 0) {
// 							return clear();
// 						}
// 						y++;
// 					}
// 				}
// 				else if(from_cell[0] < to_cell[0]) {		// goes down
// 					y = from_cell[0] - 1;
// 					while(y >= to_cell[0]) {
// 						if(BOARD[y][cell[1]] != 0) {
// 							return clear();
// 						}
// 						y--;
// 					}
// 				}
// 				else return clear();
// 			}
// 			else return clear();
// 			api_player_move(from_cell.join(','), $(this).attr('id'));
// 			clear();
// 		}
// 		else if (cls == "attacker" && from_cell == null) {
// 			from_cell = $(this).attr('id').split(',');
// 			from_cell[0] = parseInt(from_cell[0]);
// 			from_cell[1] = parseInt(from_cell[1]);
// 			$(this).attr('class','attacker-select');
// 		}
// 		else clear();
// 	});
//
// 	function clear() {
// 		if(from_cell != null) document.getElementById(from_cell[0] + ',' + from_cell[1]).setAttribute('class',"attacker");
// 		from_cell = null;
// 	}
// });
