//This function allows us to prepare HTML elements and their activites upon load of the HTML page.
$(document).ready(function(){

    //Retrieve and display pet report fields
    display_PetReport_fields({ "petreport":TARGET_PETREPORT, "list": $(".target_petreport_fields") });
    display_PetReport_fields({ "petreport":CANDIDATE_PETREPORT, "list": $(".candidate_petreport_fields") });
   
});
