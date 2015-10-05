$(document).ready(function(){
    $("#epm-nav-links .nav-link-profile").toggleClass("active");
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