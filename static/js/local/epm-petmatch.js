//This function allows us to prepare HTML elements and their activites upon load of the HTML page.
$(document).ready(function(){

    //Variables to control for upvoting and downvoting and for readability.
    var downvote_button = $("#pmdp_downvote_button");
    var upvote_button = $("#pmdp_upvote_button");
    var UPVOTE = "upvote";
    var DOWNVOTE = "downvote";
    var DOWNVOTE_BUTTON_ACTIVE_LINK = STATIC_URL + "images/icons/button_downvote_active.png";
    var DOWNVOTE_BUTTON_INACTIVE_LINK = STATIC_URL + "images/icons/button_downvote_inactive.png";
    var UPVOTE_BUTTON_ACTIVE_LINK = STATIC_URL + "images/icons/button_upvote_active.png";
    var UPVOTE_BUTTON_INACTIVE_LINK = STATIC_URL + "images/icons/button_upvote_inactive.png";  
    //alert(VOTED + " " + UPVOTE + " " + DOWNVOTE); //Diagnose problems

    //User has upvoted before
    if (VOTED == UPVOTE){
      upvote_button.attr("src", UPVOTE_BUTTON_INACTIVE_LINK);
      upvote_button.css("cursor", "default");
    }

    //User has downvoted before
    else if (VOTED == DOWNVOTE){
      downvote_button.attr("src", DOWNVOTE_BUTTON_INACTIVE_LINK);
      downvote_button.css("cursor", "default");
    }

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
      share_on_facebook(URL, IMAGE, TITLE, SUMMERY);
    });

    $("#twitter_share_pm").click(function(){
      share_on_twitter(URL, IMAGE, TITLE, SUMMERY);
    });

});

//The voting AJAX POST call. Requires a string with either "up" or "down".
function vote (user_vote){

  //Check if the user has logged in.
  if (USER_ID == "None"){
    $(".pmdp_messages").html("<li class='error'> You cannot vote for this Pet Match because you are not logged in! "+ URL_LOGIN + "</li>");
    return false;
  }

  //This is the value for the CSRF Token that must be passed into the POST request.
  csrf_value = $("input").attr("value");

  //Perform the AJAX POST Request for Voting on a PetMatch.
  $.ajax({
    type:"POST",
    url: URL_VOTE_PETMATCH,
    data: {"csrfmiddlewaretoken": csrf_value, "vote":user_vote, "match_id":PETMATCH_ID, "user_id":USER_ID},
    success: function(data){        
      $(".pmdp_messages").html("<li class='success'>" + data.message + "</li>");
      $("#pmdp_downvote_number").html(data.num_downvotes);
      $("#pmdp_upvote_number").html(data.num_upvotes);
      return true;
    },
    error: function(data){
      alert("An unexpected error occurred when trying to " + user_vote +" this PetMatch."); 
      return false;
    }
  });                  
  return true;
}


