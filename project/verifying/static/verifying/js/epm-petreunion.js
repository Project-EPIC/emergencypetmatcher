$(document).ready(function(){

  //Use the Zoom plugin to zoom into pictures.
  $(".img-wrapper img").on("mouseover", function(){
    $(this).css("display", "block");
    $(this).parent().zoom();
    $(".pet_picwrapper img:not(:first)").remove();
  });


});