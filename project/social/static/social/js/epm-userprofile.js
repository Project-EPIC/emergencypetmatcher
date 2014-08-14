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

    $("#userprofile-msg-btn").click(function(){

    	//If the form is not shown, show it.
    	if ($("#userprofile-message-form").css("display") == "none"){
    		$("#userprofile-message-form").css("display", "block");
    		$("#userprofile-msg-btn").prop("textContent", "Cancel");
    	}
    	else {
    		$("#userprofile-message-form").css("display", "none");
    		$("#userprofile-msg-btn").prop("textContent", "Send a Message");
    	}
    });

});