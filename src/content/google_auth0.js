var KEY;
var BOARD;
var SIGNEDIN = false;

function init() {
   var apisToLoad;
   var callback = function() {
      if(--apisToLoad == 0) {
         enableLogin();
         signin(true);
      }
   }

   apisToLoad = 2;

   gapi.client.load(
      'oauth2',
      'v2',
      callback
   );

   gapi.client.load(
      'hnefatafl',
      'v1',
      callback,
      'http://localhost:8080/_ah/api'
   );


}

function enableLogin() {
/*	var currentDiv = document.getElementById("here");
   var inp = document.createElement("input");
   inp.type = "button";
   inp.value = "signin";
   inp.id = "signin";

   inp.addEventListener('click', auth);
   currentDiv.addEventListener('click', api_new_game);
   document.body.insertBefore(inp, currentDiv);*/

}

function signin(immediate) {
   gapi.auth.authorize({
      client_id: '314272160250-ucrqg44c1oj9knlrfatqvqf1b3pm9819.apps.googleusercontent.com',
      scope: 'https://www.googleapis.com/auth/userinfo.email',
      immediate: immediate
   }, userAuthed);
}

var auth = function() {
   if(!SIGNEDIN) {
      signin(false);
      //enableLogin();
   }
   else {
      SIGNEDIN = false;
   //	document.querySelector('#signin').textContent = 'Sign in';
   }
}
/*
* Loads the ui after authenticated
*/
var userAuthed = function(mode) {
   var request = gapi.client.oauth2.userinfo.get().execute(function(resp) {
      if (!resp.code) {
         console.log(resp);

         var currentDiv = document.getElementById("image");
         currentDiv.src = resp.picture;

         name = document.getElementById("user-name");
         name.innerText = resp.name;


         SIGNEDIN = true;
      //	document.querySelector('#signin').textContent = 'Sign out';
         //document.querySelector('#authedGreeting').disabled = false;
         api_new_game();
       }
  });
}

var api_new_game = function() {
   gapi.client.hnefatafl.new_game().execute(function(response){
      console.log(response);
      KEY = response.key;
      board  = parse_board(response.board);
      //ai_move(true);
      //new_board();
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

   BOARD = s;

   //console.log(b);
   /*var b = board.replace(/[\[\]]+/g, '').split(',');
   var t = '';
   for(var i=0; i < b.length; i++) {
      t += b[i] + ',';
   }*/
}
