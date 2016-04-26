var google_auth = (function(){

   const url = 'http://localhost:8080/_ah/api';
   var signedin = false;

   function loadModules(){
      console.log('gogo');
      gapi.client.load(
         'oauth2',
         'v2'
      );
      gapi.client.load(
         'hnefatafl',
         'v1',
         afterLoaded,
         url
      );
   }

   function afterLoaded() {
      console.log('here');
      profile.enableLogin();
      console.log('here2');
      signin(immediate = true);
      console.log('here3');
   }

   function signin(immediate) {
      gapi.auth.authorize({
         client_id: '314272160250-ucrqg44c1oj9knlrfatqvqf1b3pm9819.apps.googleusercontent.com',
         scope: 'https://www.googleapis.com/auth/userinfo.email',
         immediate: immediate
      }, userAuthed);
   }

   function isAuthed() {
      return signedin;
   }

   function userAuthed(mode) {
      var request = gapi.client.oauth2.userinfo.get().execute(function(resp) {
         if (!resp.code) {
            profile.setLoggedIn(resp.picture, resp.name);
            signedin = true;
            google_apis.new_game();
          }
     });
   }
   return {
      loadModules: loadModules,
      isAuthed: isAuthed,
      signin: signin
   };

})();
