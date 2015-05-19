//This function allows us to prepare HTML elements and their activites upon load of the HTML page.
$(document).ready(function(){
  var bookmark_button = $("#prdp-bookmark");

  //Bookmark click handler.
  $(bookmark_button).click(function(){ 
    if (USER_ID == "None"){
      login_link = "Log in <a href="+ HOME_URLS["LOGIN"] +"?next={% firstof request.path '/' %} > here.</a>";
      $(".prdp_messages").html("<li class='error'> You cannot bookmark this Pet Report because you are not logged in! "+login_link+ "</li>");
    } 

    else 
      bookmark(); 
  });

  //user is authenticated and has bookmarked this pet 
  if (BOOKMARKED == "True"){
    bookmark_button.text("Remove Bookmark");
    bookmark_button.attr("title","Remove Bookmark");
  }
  //user has not bookmarked this pet (or) user is not authenticated
  else {
    bookmark_button.text("Bookmark this Pet");
    bookmark_button.attr("title","Bookmark this Pet");
  }

  $(".thumb-wrapper a").click(function(){ launch_dialog($("#epm-modal"), $(this).attr("link")); });

  //Update the share buttons' click event.
  $("#facebook_share_pr").click(function(){
    share_on_facebook(PETREPORT_URL, PETREPORT_IMAGE, PETREPORT_TITLE, PETREPORT_CAPTION, PETREPORT_SUMMARY);
  });

  $("#prdp-share").click(function(){
    share_on_twitter(PETREPORT_URL, PETREPORT_IMAGE, PETREPORT_TITLE, PETREPORT_SUMMARY);
  });


  //Use the Zoom plugin to zoom into pictures.
  $(".img-wrapper img").on("mouseover", function(){
    $(this).css("display", "block");
    $(this).parent().zoom();
    $(".pet_picwrapper img:not(:first)").remove();
  });

  //Retrieve and display the current pet report fields using json data   
  function bookmark(){
    $.ajax({
      type: "POST",
      url: REPORTING_URLS["BOOKMARK"],
      data: { 
        "csrfmiddlewaretoken":$("input[name='csrfmiddlewaretoken']").attr("value"), 
        "petreport_id": PETREPORT_ID, 
        "action":bookmark_button.text()
      },
      success: function(data){
        bookmark_button.text(data.text);
        bookmark_button.attr("title",data.text);
        $(".prdp_messages").html("<li class='success'>" + data.message + "</li>");
        return true;
      },
      error: function(data){
        alert("An unexpected error occurred when trying to bookmark this Pet Report. Please try again."); 
        return false;
      }
    });
    return true;
  }    

});



//@ sourceURL=epm-petreport.js