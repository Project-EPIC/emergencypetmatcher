$(document).ready(function(){
	var img_size = 0.0; //Image Size.
	var img_rotation = 0;

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
	});

	//Make simple checks before making a round-trip to server.
	$("#update_User_pwd_button").click(function(){
		$("#update_User_pwd_form").submit();
	});

	$("#id_username").change(function(e){
		check_attribute("username", function(username){
			return !($.trim(username).indexOf(' ') >= 0);
		});
	});

	$("#id_email").change(function(e){
		check_attribute("email", function(email){
			var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
			return re.test(email);
		});
	});

	//If an input image comes through, preview it!
	$("#id_img_path").change(function(){
		if (this.files && this.files[0]) {
			img_size = this.files[0].size/1000/1000; //Image size in MB.

			if (img_size > 3.0) {
				alert("Image size exceeds 3MB, please upload an image that is within 3MB.");
				$('#id_img_path').val("");
				$("#preview_img").html("");
				this.focus();
			}
			else {
				var reader = new FileReader();
				reader.onload = function (e) {
					//Create an image element, tack on the source, fit it into the container for preview,
					//and keep tabs on rotation parameter. It will be sent off for POST.
					var img = document.createElement("img");
					$(img).attr("src", e.target.result);
					$(img).css("cursor", "pointer");
					$("#preview_img").html("");
					$("#preview_img").append(img);
					$("#rotate_instructions").css("display", "block");

					//Click handler for rotating image.
					$(img).click (function(){
						img_rotation = (img_rotation + 90) % 360;
						$(this).rotate(img_rotation);
						$("#id_img_rotation").attr("value", img_rotation);
					});
				}
				reader.readAsDataURL(this.files[0]);
    	}
		}
	});

	$('#id_img_path').change(function(){
	 	img_size = this.files[0].size/1024/1024;
	  if (img_size > 3.0) {
	  	alert("Image size exceeds 3MB, please upload an image that is within 3MB.");
	  	$(this).attr("value", "")
			this.focus();
 		}
  });
});


function check_attribute(attribute, check_fun){
	var id = "#id_" + attribute;
	var message_id = $("#message_id_" + attribute);
	if ($(id).val().trim() != ""){
		data = {"page":1};
		data[attribute] = $(id).val();
		perform_AJAX_call({
			url: SOCIALIZING_URLS["USERPROFILES_JSON"],
			data: data,
			success: function(data){
				if (data["count"] > 0 && data["userprofiles_list"][0][attribute] == $(id).val()){
					$(message_id).text(attribute + " has already been taken!");
					$(message_id).css("color", "red");
				}
				else {
					if (check_fun != undefined){
						if (check_fun($(id).val()) == true){
							$(message_id).text(attribute + " is good!");
							$(message_id).css("color", "green");
						} else {
							$(message_id).text("Please make sure " + attribute + " is valid.");
							$(message_id).css("color", "red");
						}
					}
				}
			}
		});
	}
}
