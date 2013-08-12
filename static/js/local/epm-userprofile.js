//This function allows us to prepare HTML elements and their activites upon load of the HTML page.
$(document).ready(function(){



	//Link to click to open to the PRDP
	$(".prdp_thumb a").click(function(){ load_dialog($(this).attr("link"), $(this).attr("name"), SIZE_WIDTH_PRDP, "auto"); });

	//Link to click to open to the PMDP
    $(".pmdp_dialog a").click(function(){ load_dialog($(this).attr("link"), $(this).attr("name"), SIZE_WIDTH_PMDP, "auto"); });	

    $("#userprof_msg_user").click(function(){

    	//If the form is not shown, show it.
    	if ($("#message_user_form").css("display") == "none"){
    		$("#message_user_form").css("display", "block");
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