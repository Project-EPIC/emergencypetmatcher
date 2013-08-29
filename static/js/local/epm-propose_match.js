//This function allows us to prepare HTML elements and their activites upon load of the HTML page.
$(document).ready(function(){

    //Retrieve and display pet report fields
    display_PetReport_fields({ "petreport":TARGET_PETREPORT, "list": $(".target_petreport_fields") });
    display_PetReport_fields({ "petreport":CANDIDATE_PETREPORT, "list": $(".candidate_petreport_fields") });

    //Use the Zoom plugin to zoom Lost pet pic.
    $("#first_prdp_pic_wrapper img").on("mouseover", function(){
      $(this).parent().zoom();
      $("#first_prdp_pic_wrapper img:not(:first)").remove();
    });    

    //Use the Zoom plugin to zoom Found pet pic.
    $("#second_prdp_pic_wrapper img").on("mouseover", function(){
      $(this).parent().zoom();
      $("#second_prdp_pic_wrapper img:not(:first)").remove();
    });    
   
});
