$(document).ready(function(){
	var img_size = 0.0; //Image Size.
	var img_rotation = 0;
	$("#id_username").focus(); //Autofocus the Username field.
	//Required Red Markers for Labels.
	$("label[for=id_username]").append("<b class='required-field-symbol'>*</b>")
	$("label[for=id_email]").append("<b class='required-field-symbol'>*</b>")
	$("label[for=id_dob]").append("<b class='required-field-symbol'>*</b>")
	$("label[for=id_password1]").append("<b class='required-field-symbol'>*</b>")
	$("label[for=id_password2]").append("<b class='required-field-symbol'>*</b>")

	$("#id_dob").datepicker({
		format: "mm/dd/yyyy",
		autoclose: true,
		orientation:"top left",
		startDate: "01/01/1900",
		endDate:"01/01/2010"
	}).on("changeDate", function(ev){
		determine_consent ($(this)[0].value)
	}).on("change", function(e){
		determine_consent ($(this)[0].value)
	});

	//Check these attributes right off-the-bat.
	check_attribute("username", function(username){
		return !($.trim(username).indexOf(' ') >= 0);
	});
	//Check these attributes right off-the-bat.
	check_attribute("email", function(email){
		var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
		return re.test(email);
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

	$("#id_password2").change(function(e){
		if ($("#id_password1")[0].value != $(this)[0].value){
			$("#message_id_password2").text("Passwords do not match.");
			$("#message_id_password2").css("color","red");
		}
		else{
			$("#message_id_password2").text("Passwords are good!");
			$("#message_id_password2").css("color", "green");
		}
	});

	$("#register-toc").change(function(e){
		if (this.checked == true)
			$(".g-recaptcha").attr("hidden", false);
		else
			$(".g-recaptcha").attr("hidden", true);
	})

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
						img_rotation= (img_rotation + 90) % 360;
						$(this).rotate(img_rotation);
						$("#id_img_rotation").attr("value", img_rotation);
					});
				}
				reader.readAsDataURL(this.files[0]);
    	}
		}
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

	function determine_consent(age){
		age = (new Date() - new Date(age)) / 1000 / 60 / 60 / 24 / 365.25
		if (age > 6 && age < 18){
			$("#message_id_dob").text("You will be considered an under-aged participant in this study.");
			$("#message_id_dob").css("color", "green");
			$("#tos-container").removeClass("hidden");
			$("#tos-minor-container").removeClass('hidden');
			$("#tos-adult-container").addClass('hidden');
		}
		else if (age > 18){
			$("#message_id_dob").text("You will be considered an adult participant for this study.");
			$("#message_id_dob").css("color", "green");
			$("#tos-container").removeClass("hidden");
			$("#tos-adult-container").removeClass('hidden');
			$("#tos-minor-container").addClass('hidden');
		}
		else {
			$("#message_id_dob").text("Sorry, you must be at least 6 years of age for this study.");
			$("#message_id_dob").css("color", "red");
			$("#tos-container").addClass("hidden");
			$("#tos-adult-container").addClass('hidden');
			$("#tos-minor-container").addClass('hidden');
		}
	}

});
