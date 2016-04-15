


$(document).foundation();

function new_board() {

	var xmlns = "http://www.w3.org/2000/svg";
	for(var row=0; row< BOARD.length; row++){

		for(var col=0; col< BOARD[row].length; col++) {

			var rect = document.createElementNS(xmlns, "rect");
			rect.setAttribute('x', col * 70);
			rect.setAttribute('y', row * 70);
			rect.setAttribute('id', row + ',' + col);

			var val = BOARD[row][col];
			var cls;
			if(val == '0') cls = 'empty';
			else if(val == '1') cls = 'attacker';
			else if(val == '2') cls = 'defender';
			else if(val == '3') cls = 'king';
			rect.setAttribute('class',cls);
			document.getElementById("svg").appendChild(rect);

		}
	}
}

function change_board() {
	for(var row=0; row< BOARD.length; row++){
		for(var col=0; col< BOARD[row].length; col++) {

			var val = BOARD[row][col];
			var rect = document.getElementById(row + ',' + col);

			if(val == '0') cls = 'empty';
			else if(val == '1') cls = 'attacker';
			else if(val == '2') cls = 'defender';
			else if(val == '3') cls = 'king';
			rect.setAttribute('class',cls);
		}
	}
}



$(function() {


	var from_cell = null;

	$("body").on("click","rect",function(){

		var cls = $(this).attr('class');
		//console.log(cls);
		//console.log(from_cell);
		if (cls == "empty" && from_cell != null) {

			var to_cell = $(this).attr('id').split(',');
			to_cell[0] = parseInt(to_cell[0]);
			to_cell[1] = parseInt(to_cell[1]);

			if (from_cell[0] == to_cell[0]) {
				console.log(from_cell);		// same row
				if(from_cell[1] < to_cell[1]) {				// goes right
					x = from_cell[1] + 1;
					console.log(x);
					while(x <= to_cell[1]) {
						console.log(x);
						if(BOARD[from_cell[0]][x] != 0) {
							return clear();
						}
						x++;
					}
				}
				else if(from_cell[1] > to_cell[1]) {		// goes left
					x = from_cell[1] - 1;
					while(x >= to_cell[1]) {
						if(BOARD[from_cell[0]][x] != 0) {
							return clear();
						}
						x--;
					}
				}
				else return clear();
			}
			else if (from_cell[1] == to_cell[1]) {		// same column
				if(from_cell[0] > to_cell[0]) {				// goes up
					y = from_cell[0] + 1;
					while(y <= to_cell[0]) {
						if(BOARD[y][cell[1]] != 0) {
							return clear();
						}
						y++;
					}
				}
				else if(from_cell[0] < to_cell[0]) {		// goes down
					y = from_cell[0] - 1;
					while(y >= to_cell[0]) {
						if(BOARD[y][cell[1]] != 0) {
							return clear();
						}
						y--;
					}
				}
				else return clear();
			}
			else return clear();
			api_player_move(from_cell.join(','), $(this).attr('id'));
			clear();
		}
		else if (cls == "attacker" && from_cell == null) {
			from_cell = $(this).attr('id').split(',');
			from_cell[0] = parseInt(from_cell[0]);
			from_cell[1] = parseInt(from_cell[1]);
			$(this).attr('class','attacker-select');
		}
		else clear();
	});

	function clear() {
		if(from_cell != null) document.getElementById(from_cell[0] + ',' + from_cell[1]).setAttribute('class',"attacker");
		from_cell = null;
	}
});
