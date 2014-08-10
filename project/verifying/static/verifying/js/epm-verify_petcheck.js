$(document).ready(function(){
 

  $("#lost-prdp-link").click(function(){ 
    launch_dialog($("#epm-modal"), URL_PRDP + LOST_PETREPORT_ID); 
  });

  $("#found-prdp-link").click(function(){ 
    launch_dialog($("#epm-modal"), URL_PRDP + FOUND_PETREPORT_ID); 
  });

  if(USER_HAS_VERIFIED == "True"){
    $("#messages").append("<li class='info'>You have already submitted a response for this Pet Match!</li>");
  }

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