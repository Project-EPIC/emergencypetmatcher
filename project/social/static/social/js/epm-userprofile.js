//This function allows us to prepare HTML elements and their activities upon load of the HTML page.
$(document).ready(function(){

	//Link to click to open to the PRDP
	$("#userprofile-submitted-petreports a").click(function(){ 
        $("#epm-modal").modal({
            "remote": $(this).attr("link")
        });
    });

    //Link to click to open to the PRDP
    $("#userprofile-proposed-petmatches a").click(function(){ 
        $("#epm-modal").modal({
            "remote": $(this).attr("link")
        });
    });    

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