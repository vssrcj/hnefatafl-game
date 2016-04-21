var KEY;
var BOARD;
var SIGNEDIN = false;

function init() {
   gapi.client.load(
      'oauth2',
      'v2'
   );

   gapi.client.load(
      'hnefatafl',
      'v1',
      apisLoaded,
      'http://localhost:8080/_ah/api'
   );
}

function apisLoaded() {
   sidenav.enableLogin();
   signin(immediate = true);   // tries signing in without popup screen (else browser blocks it)
}

var sidenav = (function() {
   var $btn = $("#loginButton");
   var $img = $("#profilePicture");
   var $name = $("#userName");

   function enableLogin() {
      $btn.on('click', _loginClick);
      console.log('enabled');
      $btn.removeClass("disabled");
   }
   function _loginClick() {
      console.log('clik');
      singin(immediate = false);
   }
   function _logoutClick() {
      //singin(immediate = false);
   }
   function setLoggedIn(src, name) {
      console.log('here');
      $img.attr('src', src);
      $name.html(name);
      $btn.text("Logout");
      $btn.addClass("alert");
      $btn.off('click');
      $btn.on('click', _logoutClick);
   }
   return {
      enableLogin: enableLogin,
      setLoggedIn: setLoggedIn
   };
})();


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
