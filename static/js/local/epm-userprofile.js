//This function allows us to prepare HTML elements and their activites upon load of the HTML page.
$(document).ready(function(){

	//Link to click to open to the PRDP
	$(".prdp_dialog a").click(function(){

		var link = $(this);
		//load_dialog(link, title, width, height)
		return load_dialog(link.attr("href"), link.attr("name"), 700, "auto");

	});

	//Link to click to open to the PMDP
    $(".pmdp_dialog a").click(function(){

  		var link = $(this);
		//load_dialog(link, title, width, height)
		return load_dialog(link.attr("href"), link.attr("name"), 850, "auto");

    });	

});