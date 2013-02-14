//This function allows us to prepare HTML elements and their activites upon load of the HTML page.
$(document).ready(function(){
  
    var bookmark_button = $("#prdp_bookmark");

    //user is authenticated and has bookmarked this pet 
    if (BOOKMARKED == "true"){
      bookmark_button.text("Remove Bookmark");
      bookmark_button.attr("title","Remove Bookmark");
    }

    //user has not bookmarked this pet (or) user is not authenticated
    else {
      bookmark_button.text("Bookmark this Pet");
      bookmark_button.attr("title","Bookmark this Pet");
    }

    $(".prdp_pmdp_dialog a").click(function(){

      var link = $(this);
      return load_dialog(link.attr("href"), "Pet Match Detailed Page", 850, "auto");  

    });

    //Update the share buttons' click event.
    $("#facebook_share_pr").click(function(){
      //share_on_facebook(URL, IMAGE, TITLE, SUMMARY);
      publishToFeed(URL, IMAGE, TITLE, CAPTION, SUMMARY);
    });

    $("#twitter_share_pr").click(function(){
      share_on_twitter(URL, IMAGE, TITLE, SUMMARY);
    });

    //Retrieve and display the current pet report fields using json data   
    display_PetReport_fields(PETREPORT_JSON, $(".prdpfields"));
});

function bookmark(){

  var bookmark_button = $("#prdp_bookmark");
    
  
  if (USER_ID == "None"){
    login_link = "Log in <a href="+URL_LOGIN+"?next={% firstof request.path '/' %} > here.</a>";
    $(".prdp_messages").html("<li class='error'> You cannot bookmark this Pet Report because you are not logged in! "+login_link+ "</li>");
    return false;
  }

  csrf_value = $("input").attr("value");

  $.ajax({

    type:"POST",
    url:URL_BOOKMARK_PETREPORT,
    data: {"csrfmiddlewaretoken":csrf_value, "petreport_id":PETREPORT_ID, "action":bookmark_button.text()},
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

