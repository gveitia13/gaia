$(function () {
  // Amount Of Scrolling Before Button Is Shown/Hidden.
  let Offset = 100;
  // Fade Duration
  let Duration = 500;
  // Toggle View Of Button When Scrolling.
  $(window).scroll(function () {
    if ($(this).scrollTop() > Offset) {
      $('#C-Go-Top').fadeIn(Duration);
    } else {
      $('#C-Go-Top').fadeOut(Duration);
    }
  });
  // Scroll To Top When Button Is Clicked.
  $('#C-Go-Top').click(function (Event) {
    Event.preventDefault();
    $('Html, Body').animate({
      scrollTop: 0
    }, Duration);
    return false;
  });
});