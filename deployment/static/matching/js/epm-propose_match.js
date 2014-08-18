//This function allows us to prepare HTML elements and their activites upon load of the HTML page.
$(document).ready(function(){

    //Retrieve and display pet report fields
    highlight_field_matches($("#pmdp-info-table"));

    //Use the Zoom plugin to zoom Lost pet pic.
    $("#target-pic img").on("mouseover", function(){
      $(this).parent().zoom();
      $("#target-pic img:not(:first)").remove();
    });    

    //Use the Zoom plugin to zoom Found pet pic.
    $("#candidate-pic img").on("mouseover", function(){
      $(this).parent().zoom();
      $("#candidate-pic img:not(:first)").remove();
    });    
   
});
