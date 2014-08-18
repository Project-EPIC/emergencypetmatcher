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

	//If an input image comes through, preview it!
	$("#img_path").change(function(){

		if (this.files && this.files[0]) {
			var reader = new FileReader();

			reader.onload = function (e) {
				//Create an image element, tack on the source, fit it into the container for preview, 
				//and keep tabs on rotation parameter. It will be sent off for POST.
				var img = document.createElement("img");
				$(img).attr("src", e.target.result);
				$(img).width(198);
				$(img).height(223);
				$(img).css("cursor", "pointer");
				$(".userprofile-img-wrapper").html("");
            	$(".userprofile-img-wrapper").append(img);
        	}
        	reader.readAsDataURL(this.files[0]);
    	}
	});

	$('#img_path').change(function(){
           	img_size = this.files[0].size/1024/1024;
            if (img_size > 3.0) {
            	alert("Image size exceeds 3MB, please upload an image that is within 3MB.");
            	$(this).attr("value", "")
 				this.focus();
 			}          
    });		
});

	