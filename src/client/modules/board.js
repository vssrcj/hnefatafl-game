var board = (function() {

   var $board = $("#board");
   var $board_header = $("#board_header");
   var $new_game = $("#new_game");

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
            var result = google_apis.player_move(
               $selected.attr('id'),
               $cell.attr('id')
            );
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
      $board_header.addClass('hidden');
   }
   $new_game.on('click',new_game);

   function cellClick(target, params) {

   }

   function reset() {
      if($selected) {
         $selected.attr('class','attacker');
         $selected = null;
      }
   }

   function game_end(game_state) {
      if(game_state == 2 || game_state == 3) {
         if(game_state == 2){
            $board_header.append("Player won!");
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

   return {
      empty_board: empty_board,
      new_board: new_board,
      move: move,
      game_end: game_end,
      reset: reset
   };
})();
