$(document).ready(function(){
	$("#register-submit")[0].disabled = true

	$("#register-dob").datepicker({
		format: "mm/dd/yyyy",
		autoclose: true,
		startDate: "01/01/1900",
		endDate:"01/01/2010"
	}).on("changeDate", function(ev){
		determine_consent ($(this)[0].value)
	}).on("change", function(e){
		determine_consent ($(this)[0].value)
	});

	$("#password2").change(function(e){
		if ($("#password1")[0].value != $(this)[0].value){
			$("#register-passwords").text("Passwords do not match.")
			$("#register-passwords").css("color","red")
		}
		else{
			$("#register-passwords").text("Passwords are good!")
			$("#register-passwords").css("color", "green")
		}
	});

	$("#register-toc").change(function(e){
		if ($(this)[0].checked == true)
			$("#register-submit")[0].disabled = false
		else
			$("#register-submit")[0].disabled = true
	})

	function determine_consent(age){
		age = (new Date() - new Date(age)) / 1000 / 60 / 60 / 24 / 365.25
		if (age > 6 && age < 18){
			$("#register-age").text("You will be considered an under-aged participant in this study.");
			$("#tos-container").removeClass("hidden");
			$("#tos-minor-container").removeClass('hidden');
			$("#tos-adult-container").addClass('hidden');
		}
		else if (age > 18){
			$("#register-age").text("You will be considered an adult participant for this study.");
			$("#tos-container").removeClass("hidden");
			$("#tos-adult-container").removeClass('hidden');
			$("#tos-minor-container").addClass('hidden');
		}
		else {
			$("#register-age").text("Sorry, you must be at least 6 years of age for this study.");	
			$("#tos-container").addClass("hidden");
			$("#tos-adult-container").addClass('hidden');
			$("#tos-minor-container").addClass('hidden');					
		}
	}






});