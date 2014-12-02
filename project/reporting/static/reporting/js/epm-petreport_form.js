$(document).ready(function(){

	$("#epm-nav-links .nav-link-pet").toggleClass("active");
	//Image Size.
	var img_size = 0.0;
	var img_rotation = 0;

	//Initialize with today's date
	var today = new Date();
	var curYear = new Date().getUTCFullYear();
	$("#id_date_lost_or_found").datepicker({
		changeMonth: true, 
		showOn:"focus",
		changeYear: true, 
		yearRange: '1900:curYear'
	});

	$("#id_date_lost_or_found").attr("value", today.getMonth()+1 + '/' + today.getDate() + '/' + today.getFullYear());

	//If an input image comes through, preview it!
	$("#id_img_path").change(function(){

		if (this.files && this.files[0]) {
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
	});

	$("#id_tag_collar_info").keyup(function(){

		var count = PETREPORT_TAG_INFO_LENGTH - this.value.length;
		$("#id_tag_collar_info_count").html(count + " characters remaining");
	});
	
	$("#id_description").keyup(function(){

		var count = PETREPORT_DESCRIPTION_LENGTH - this.value.length;
		$("#id_description_count").html(count + " characters remaining");
	});

	$("#petreport_form_microchip_check").click(function(){ $("#petreport_form_microchip_field").toggleClass("hidden"); });
	$("#petreport_form_geo_check").click(function(){ $("#petreport_form_geo_fields").toggleClass("hidden"); });	


	$("#id_tag_info").bind('mouseleave', function() { 
		//alert(this.value.length)
		if ( this.value.length> PETREPORT_TAG_INFO_LENGTH ){
			alert("Tag and Collar Information is too long (maximum is " + PETREPORT_TAG_INFO_LENGTH  + " characters)");
			this.focus();
		}
	});

	$("#petreport_form_contact_check").click(function(){
		if($(this).prop("checked") == true)
			$("#petreport_form_contact_fields").css("display", "inline");
		else
			$("#petreport_form_contact_fields").css("display", "none");
	});		

	$('#id_img_path').change(function(){
           	img_size = this.files[0].size/1024/1024;
            if (img_size > 3.0) {
            	alert("Image size exceeds 3MB, please upload an image that is within 3MB.");
            	$('#id_img_path').attr("value","")
 				this.focus();
 			}          
    });

	$("#id_submit").click(function(){

			var conditions = true;
			var issues = "Please fix the following fields before submitting this form: \n";
			var num_issues = 0;

			/*check for date value = null and date value in future*/
			if ($("#id_date_lost_or_found").attr("value")==""){
				conditions = false;
				issues += (++num_issues)+" . Please fill in the Date Lost/Found.\n";
			}

			else if ((new Date($("#id_date_lost_or_found").attr("value"))) > (new Date()) ){
				conditions = false;
				issues += "Please fill in a valid Date Lost/Found.\n";
			}

			if (img_size > 3.0) {
				conditions = false;				
				issues += (++num_issues)+". Image size should be less that 3MB.\n";
			}	

			if(conditions == true)
				document.forms['petreport_form'].submit();
			else
				alert(issues);
	});

	//Listen for a change in the pet type. If the user selects a pet type, load the breeds for that pet type!
	$("#id_pet_type").change(function(){
		var pet_type = this.value;
		load_pet_breeds(pet_type);
	});	

	/******** Kick Things Off *********/
	load_pet_breeds("Dog");

});

//Load up the pet breeds here.
function load_pet_breeds (pet_type){

	id = 0;
	if (pet_type == "Dog")
		id = 0;
	else if (pet_type == "Cat")
		id = 1;
	else if (pet_type == "Horse")
		id = 2; 
	else if (pet_type == "Bird")
		id = 3;
	else if (pet_type == "Rabbit")
		id = 4;
	else if (pet_type == "Turtle")
		id = 5;
	else if (pet_type == "Snake")
		id = 6;
	else
		id = 7; //Other

	$.ajax ({
		type:"GET",
		url: URL_GET_PET_BREEDS + id, 
		success: function(data){
			$("#id_breed").select2({ 
				data: data.breeds
			});
		},
		error: function (data){
			return [];
		}
	});

}
















