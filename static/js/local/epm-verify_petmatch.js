//This function uses the postIt j/s function to send a post request to the server to vevrify the petmatch
function post_user_response(message){
      var url = URL_VERIFY_PETMATCH+PETMATCH_ID+"/";
      var csrf_value = $("input").attr("value");
      var data= {"csrfmiddlewaretoken":csrf_value, "message":message};
      postIt(url,data);
}

$(document).ready(function(){
 
    if(USER_HAS_VERIFIED == true){
      $(".verification_message").text("You have already submitted a response for this Pet Match!");
      $("#prdp_buttons").remove();
    }

    //Retrieve and display the lost pet report fields
    display_PetReport_fields(LOST_PETREPORT, $(".lost_pmdpfields"));

    //Retrieve and display the found pet report fields
    display_PetReport_fields(FOUND_PETREPORT, $(".found_pmdpfields"));

});

