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

    $("#userprof_msg_user").click(function(){

    	//If the form is not shown, show it.
    	if ($("#message_user_form").css("display") == "none"){
    		$("#message_user_form").css("display", "inline");
            $("#message_user_form_helptext").css("display", "inline");
    		$("#userprof_msg_user").prop("textContent", "Cancel");
    	}
    	else {
            $("#message_user_form_helptext").css("display", "none");
    		$("#message_user_form").css("display", "none");
    		$("#userprof_msg_user").prop("textContent", "Send a Message");
    	}
    });

});