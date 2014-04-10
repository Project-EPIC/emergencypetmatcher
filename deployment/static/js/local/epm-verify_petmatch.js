$(document).ready(function(){
 
    if(USER_HAS_VERIFIED == true){
      $(".verification_message").text("You have already submitted a response for this Pet Match!");
      $("#prdp_buttons").remove();
    }

    /***** Start things off. *****/

    //Retrieve and display the lost pet report fields
    display_PetReport_fields({ "petreport": LOST_PETREPORT, "list":$("#lost_prdpfields") });
    display_PetReport_fields({ "petreport": FOUND_PETREPORT, "list":$("#found_prdpfields") });    

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
    highlight_matches ($("#found_prdpfields"), $("#lost_prdpfields"));
    
});

//This function uses the postIt j/s function to send a post request to the server to verify the petmatch
function post_user_response(message){
      var url = URL_VERIFY_PETMATCH+PETMATCH_ID+"/";
      var csrf_value = $("input").attr("value");
      var data= {"csrfmiddlewaretoken":csrf_value, "message":message};
      postIt(url,data);
}
