//This function allows us to prepare HTML elements and their activites upon load of the HTML page.
$(document).ready(function(){

	//Link to click to open to the PRDP
	$(".prdp_dialog").click(function(){

		var link = $(this);
		var options = {

			autoOpen: true,
			position: "top",
			closeOnEscape: true,
			title:link.attr("name"),
			height: "auto",
			modal: true,
			width: 700,
			resizable: false,
			show: {effect:"fade", duration:500}
		};

		return load_dialog(link, options);
	});

	//Link to click to open to the PMDP
    $(".pmdp_dialog a").click(function(){

      var link = $(this).attr("value");
      var options = {

		autoOpen: true,
        position: "top",
        closeOnEscape: true,
        title: "Pet Match Detailed Page",
        width: 850,
        height: "auto",
        modal: true,
        resizable: false,
        show: {effect:"fade", duration:500}

      };
      return load_dialog(link, options);
    });	

});