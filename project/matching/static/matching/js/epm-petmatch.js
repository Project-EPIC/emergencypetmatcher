//This function allows us to prepare HTML elements and their activites upon load of the HTML page.
$(document).ready(function(){

  $("#lost-prdp-link").click(function(){ 
    launch_dialog($("#epm-modal"), REPORTING_URLS["PETREPORT"] + LOST_PETREPORT_ID); 
  });

  $("#found-prdp-link").click(function(){ 
    launch_dialog($("#epm-modal"), REPORTING_URLS["PETREPORT"] + FOUND_PETREPORT_ID); 
  });

    //Variables to control for upvoting and downvoting and for readability.
    var downvote_button = $("#pmdp_downvote_button");
    var upvote_button = $("#pmdp_upvote_button");

    //When the User clicks on the DOWNVOTE Button...
    downvote_button.click(function(){ 
      //If the button hasn't been pushed yet.
      if ($(this).attr("src") != DOWNVOTE_BUTTON_INACTIVE_LINK){

        //Perform the vote.
        if (vote (DOWNVOTE) == true){
          $(this).attr("src", DOWNVOTE_BUTTON_INACTIVE_LINK);
          $(this).css("cursor", "default");

          //Make sure the other button is all set up to change too.
          upvote_button.attr("src", UPVOTE_BUTTON_ACTIVE_LINK);
          upvote_button.css("cursor", "pointer");
        }
      }
    });

    //When the User clicks on the UPVOTE Button...
    upvote_button.click(function(){ 
      //If the button hasn't been pushed yet.
      if ($(this).attr("src") != UPVOTE_BUTTON_INACTIVE_LINK){

        //Perform the vote.
        if (vote (UPVOTE) == true){
          $(this).attr("src", UPVOTE_BUTTON_INACTIVE_LINK);
          $(this).css("cursor", "default");

          //Make sure the other button is all set up to change too.
          downvote_button.attr("src", DOWNVOTE_BUTTON_ACTIVE_LINK);
          downvote_button.css("cursor", "pointer");
        }
      }
    });

    //Update the share buttons' click event.
    $("#facebook_share_pm").click(function(){
      share_on_facebook(PETMATCH_URL, PETMATCH_IMAGE, PETMATCH_TITLE, PETMATCH_CAPTION, PETMATCH_SUMMARY);
    });

    $("#pmdp-share").click(function(){
      share_on_twitter(PETMATCH_URL, PETMATCH_IMAGE, PETMATCH_TITLE, PETMATCH_SUMMARY);
    });

    /***** Start things off. *****/

    //User has upvoted before
    if (USER_HAS_VOTED == UPVOTE){
      upvote_button.attr("src", UPVOTE_BUTTON_INACTIVE_LINK);
      upvote_button.css("cursor", "default");
    }

    //User has downvoted before
    else if (USER_HAS_VOTED == DOWNVOTE){
      downvote_button.attr("src", DOWNVOTE_BUTTON_INACTIVE_LINK);
      downvote_button.css("cursor", "default");
    }

    highlight_field_matches ($("#pmdp-info-table"));

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

    //If the PetMatch is closed, then disallow voting.
    if (PETMATCH_IS_BEING_CHECKED == "True"){
      $("#pmdp_downvote_button").attr("src", DOWNVOTE_BUTTON_INACTIVE_LINK);
      $("#pmdp_downvote_button").css("cursor", "default");
      $("#pmdp_upvote_button").attr("src", UPVOTE_BUTTON_INACTIVE_LINK);
      $("#pmdp_upvote_button").css("cursor", "default");
    }

});

/******************************* Utility functions *******************************************/

//The voting AJAX POST call. Requires a string with either "up" or "down".
function vote (user_vote){
  //Check if the user has logged in.
  if (USER_ID == "None"){
    $(".pmdp_messages").html("<li class='error'> You cannot vote for this Pet Match because you are not logged in! <a href='"+ HOME_URLS["LOGIN"] + "'>Log in Here.</a></li>");
    return false;
  }

  //This is the value for the CSRF Token that must be passed into the POST request.
  var csrf_value = $("input").attr("value");

  //Perform the AJAX POST Request for Voting on a PetMatch.
  $.ajax({
    type:"POST",
    url: MATCHING_URLS["VOTE"],
    data: {"csrfmiddlewaretoken": csrf_value, "vote":user_vote, "match_id":PETMATCH_ID, "user_id":USER_ID},
    success: function(data){        
      $(".pmdp_messages").html("<li class='success'>" + data.message + "</li>");
      $("#pmdp_downvote_number").html(data.num_downvotes);
      $("#pmdp_upvote_number").html(data.num_upvotes);

      if (data.threshold_reached == true){
        //Disable the voting buttons - we are done voting on this PMDP.
        $("#pmdp_downvote_button").attr("src", DOWNVOTE_BUTTON_INACTIVE_LINK);
        $("#pmdp_downvote_button").css("cursor", "default");
        $("#pmdp_upvote_button").attr("src", UPVOTE_BUTTON_INACTIVE_LINK);
        $("#pmdp_upvote_button").css("cursor", "default");
      }

      return true;
    },
    error: function(data){
      alert("An unexpected error occurred when trying to " + user_vote +" this PetMatch."); 
      return false;
    }
  });                  
  return true;
}

//@ sourceURL=epm-petmatch.js
