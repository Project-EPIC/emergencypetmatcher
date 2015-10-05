$(document).ready(function(){

  if(USER_HAS_VERIFIED == "True")
    add_flash_message("info", "You have already submitted a response for this Pet Match!")

  /***** Start things off. *****/

  //Use the Zoom plugin to zoom Lost pet pic.
  $("#lost_pet_pic_wrapper img").on("mouseover", function(){
    $(this).parent().zoom();
    $("#lost_pet_pic_wrapper img:not(:first)").remove();
  });    

  //Use the Zoom plugin to zoom Found pet pic.
  $("#found_pet_pic_wrapper img").on("mouseover", function(){
    $(this).parent().zoom();
    $("#found_pet_pic_wrapper img:not(:first)").remove();
  });

  //Highlight the matches.
  highlight_field_matches ($("#pmdp-info-table"));
});