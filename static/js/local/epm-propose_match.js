//This function allows us to prepare HTML elements and their activites upon load of the HTML page.
$(document).ready(function(){

    //Retrieve and display the lost pet report fields
    display_PetReport_fields(TARGET_PETREPORT, $(".target_petreport_fields"));

    //Retrieve and display the found pet report fields
    display_PetReport_fields(CANDIDATE_PETREPORT, $(".candidate_petreport_fields"));
   
});
