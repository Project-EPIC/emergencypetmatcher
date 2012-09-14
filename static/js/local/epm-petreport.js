//This function allows us to prepare HTML elements and their activites upon load of the HTML page.
$(document).ready(function(){

  $(".prdp_pmdp_dialog a").click(function(){

    var link = $(this);
    return load_dialog(link.attr("href"), "Pet Match Detailed Page", 850, "auto");  

  });

});

function get_petreport_object (petreport_id, img){

  $.ajax({

    type:"POST",
    url: "{{ bookmark_petreport }}",
    success: function(data){
      var petreport = data;
      // This function does not exist
      //move_petreport_to_workspace_match_detail(petreport, img);
    },
    error: function(data){
      alert("An unexpected error occurred when trying to retrieve this Pet Report's attributes. Please try again."); 
      return false;
    }
  });
}