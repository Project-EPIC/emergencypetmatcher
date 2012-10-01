//This function allows us to prepare HTML elements and their activites upon load of the HTML page.
$(document).ready(function(){

  
  var bookmark_button = $("#prdp_bookmark");

  //user is authenticated and has bookmarked this pet 
  if (bookmarked == "true"){
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

});

function bookmark(){

  var bookmark_button = $("#prdp_bookmark");
    
  
  if (user_id == "None"){
    login_link = "Log in <a href="+URL_LOGIN+"?next={% firstof request.path '/' %} > here.</a>";
    $(".prdp_messages").html("<li class='error'> You cannot bookmark this Pet Report because you are not logged in! "+login_link+ "</li>");
    return false;
  }

  csrf_value = $("input").attr("value");

  $.ajax({

    type:"POST",
    url:URL_BOOKMARK_PETREPORT,
    data: {"csrfmiddlewaretoken":csrf_value, "petreport_id":petreport_id, "action":bookmark_button.text()},
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
