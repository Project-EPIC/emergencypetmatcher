$(document).ready(function(){

	//Make simple checks before making a round-trip to server.
	$("#update_User_info_button").click(function(){
		$("#update_User_info_form").submit();

	});

	$("#id_new_password").keyup(function(){
		var confirm_pwd = $("#id_confirm_password");
		if ($(this).val() != $(confirm_pwd).val())
			$("#messages").html("<li class='error'> New password fields must match.</li>");
		else
			$("#messages").html("");

	})


	//Make simple checks before making a round-trip to server.
	$("#update_User_pwd_button").click(function(){

		$("#update_User_pwd_form").submit();
	});	

});

	