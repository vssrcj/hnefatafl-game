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
