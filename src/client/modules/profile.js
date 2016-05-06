var profile = (function() {
   var $login = $("#login");
   //var $picture = $("#picture");
   var $name = $("#name");

   function enableLogin() {
      $login.on('click', _loginClick);
      console.log('enabled');
      $login.removeClass("hidden");
   }
   function _loginClick() {
      console.log('clik');
      google_auth.signin(immediate = false);
   }
   function _logoutClick() {
      //singin(immediate = false);
   }
   function setLoggedIn(src, name) {
      console.log(name);
   //   enableLogin();
   //   $picture.attr('src', src);
     $name.html(name);
        $name.removeClass("hidden");
      $login.addClass("hidden");
   //   $btn.addClass("alert");
   ////   $btn.off('click');
   //   $btn.on('click', _logoutClick);
   }
   return {
      enableLogin: enableLogin,
      setLoggedIn: setLoggedIn
   };
})();
