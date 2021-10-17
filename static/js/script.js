$(document).ready(function(){
    $(".sidenav").sidenav({edge: "right"});
    $('.collapsible').collapsible();
    $('.tooltipped').tooltip();
    $('select').formSelect();
    $('.datepicker').datepicker({
      format: "dd mmmm, yyyy",
      yearRange: 3,
      showClearBtn: true,
      i18n: {
        done: "Select"
      }
    });
  });

  /* https://cloud.mongodb.com/v2/6161957c0e2a2e5a7ca22c8f#metrics/replicaSet/6161968a5a178b03967a4674/explorer/food_manager/catergories/find */
  $('.delete').on("click", function (e) {
    e.preventDefault();

    let choice = confirm($(this).attr('data-confirm'));

    if (choice) {
        window.location.href = $(this).attr('href');
    }
});