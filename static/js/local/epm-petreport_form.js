
	var	PETREPORT_TAG_INFO_LENGTH = 1000;
	var PETREPORT_DESCRIPTION_LENGTH = 1000;
	function countChars(textbox, counter, max) {
		var count = max - document.getElementById(textbox).value.length;
		if (count < 0) { 
			document.getElementById(counter).innerHTML = "<span style=\"color: red;\">" + count +" characters remaining" + "</span>"; 
		}
	  	else { 
	  		document.getElementById(counter).innerHTML = count+" characters remaining"; 
	  	}

	}

$(document).ready(function(){

	$("#id_status").bind('change', function() { 
		document.getElementsByClassName("id_pet_report_location")[0]
			.innerHTML="<strong>Location "+$("#id_status").attr("value")+"</strong>";
	});

	$("#petreport_form_microchip_check").click(function(){

		if($(this).prop("checked") == true)
			$("#petreport_form_microchip_field").css("display", "inline")
		else
			$("#petreport_form_microchip_field").css("display", "none")
	});

	$("#petreport_form_geo_check").click(function(){

		if($(this).prop("checked") == true)
			$("#petreport_form_geo_fields").css("display", "inline");
		else
			$("#petreport_form_geo_fields").css("display", "none"); 
	});	

	$("#petreport_form_contact_check").click(function(){

		if($(this).prop("checked") == true)
			$("#petreport_form_contact_fields").css("display", "inline");
		else
			$("#petreport_form_contact_fields").css("display", "none");
	});		

	var img_size = 0.0;

	$('#id_img_path').bind('change', function() {
           	img_size = this.files[0].size/1024/1024;
            if (img_size > 3.0) 
            	alert("Image size exceeds 3MB, please upload an image that is within 3MB");
    });

	$("#id_submit").click(function(){

			var conditions = true;
			var issues = "Please fix the following fields before submitting this form: \n";
			var num_issues = 0;
			if (img_size > 3.0)
			{
				conditions = false;
				
				issues += (++num_issues)+". Image size should be less that 3MB\n";

			}		
			var description = $("#id_description").attr("value").length;
			if ( description> PETREPORT_DESCRIPTION_LENGTH){

				conditions = false;
				var exceeds = description - PETREPORT_DESCRIPTION_LENGTH;
				issues += (++num_issues)+". Pet description should be within "+PETREPORT_DESCRIPTION_LENGTH+" characters, your description is "+exceeds+" characters over that limit.\n"
			}
			var tag_info_length = $("#id_tag_info").attr("value").length;
			if ( tag_info_length> PETREPORT_TAG_INFO_LENGTH){

				conditions = false;
				var exceeds = tag_info_length - PETREPORT_TAG_INFO_LENGTH ;
				alert (exceeds);
				issues += (++num_issues)+". Tag and Collar information should be within "+PETREPORT_TAG_INFO_LENGTH+" characters, the content you entered is "+exceeds+" characters over that limit.\n"
			}

			/*check for date value = null and date value in future*/
			if ($("#id_date_lost_or_found").attr("value")==""){
				conditions = false;
				issues += (++num_issues)+" . Please fill in the Date field";
			}

			else if ((new Date($("#id_date_lost_or_found").attr("value"))) > (new Date()) ){
				conditions = false;
				issues += (++num_issues)+" . Please fill in a valid Date";
			}

			if(conditions){
				document.forms['petreport_form'].submit();
			}
			else{
				alert(issues);
				
			}

	});
});

