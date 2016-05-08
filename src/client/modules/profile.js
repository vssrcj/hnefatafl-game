var profile = (function() {
   var $login = $("#login");
   //var $picture = $("#picture");
   var $name = $("#name");

   function enableLogin() {
      $login.on('click', _loginClick);
      $login.removeClass("hidden");
   }
   function _loginClick() {
      google_auth.signin(immediate = false);
   }
   function _logoutClick() {
      //singin(immediate = false);
   }
   function setLoggedIn(src, name) {
      $name.html(name);
      $name.removeClass("hidden");
      $login.addClass("hidden");
   }
   return {
      enableLogin: enableLogin,
      setLoggedIn: setLoggedIn
   };
})();
