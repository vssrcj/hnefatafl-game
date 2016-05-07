var dialogs = (function(){

   var $how = $("#how");
   var $history = $("#history");
   var $about = $("#about");

   var how_dialog = document.getElementById('how-dialog');
   var history_dialog = document.getElementById('history-dialog');
   var about_dialog = document.getElementById('about-dialog');

   function openHow(){
      how_dialog.showModal();
   }

   function openHistory() {
      history_dialog.showModal();
   }

   function openAbout() {
      about_dialog.showModal();
   }

   function closeHow() {
      how_dialog.close();
   }

   function closeHistory() {
      history_dialog.close();
   }

   function closeAbout() {
      about_dialog.close();
   }

   $how.on('click', openHow);
   $history.on('click', openHistory);
   $about.on('click', openAbout);

   how_dialog.querySelector('.close').addEventListener('click', closeHow);
   history_dialog.querySelector('.close').addEventListener('click', closeHistory);
   about_dialog.querySelector('.close').addEventListener('click', closeAbout);

})();
