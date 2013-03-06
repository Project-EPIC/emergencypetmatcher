
$(document).ready(function(){

	$("#petreport_form_microchip_check").click(function(){

		if($(this).prop("checked") == true)
			$("#petreport_form_microchip_field").html("<input name='microchip_id' type='text'/>");
		else
			$("#petreport_form_microchip_field").html("");
	});

	$("#petreport_form_geo_check").click(function(){

		if($(this).prop("checked") == true){
			$("#petreport_form_geo_lat_field").html("<strong>Lattitude (Lat) Coordinate: </strong><input name='geo_location_lat' type='text'/>"); 
			$("#petreport_form_geo_long_field").html("<strong>Longitude (Long) Coordinate: </strong><input name='geo_location_long' type='text'/>");
		}
		else{
			$("#petreport_form_geo_lat_field").html(""); 
			$("#petreport_form_geo_long_field").html("");
		}
	});	

	$("#petreport_form_contact_check").click(function(){

		if($(this).prop("checked") == true){
			$("#petreport_form_contact_name_field").html("<strong>Contact Name: </strong><input name='contact_name' type='text'/>"); 
			$("#petreport_form_contact_number_field").html("<strong>Contact Phone Number: </strong><input name='contact_number' type='text'/>");
			$("#petreport_form_contact_email_field").html("<strong>Contact Email Address: </strong><input name='contact_email' type='text'/>");
		}
		else{
			$("#petreport_form_contact_name_field").html(""); 
			$("#petreport_form_contact_number_field").html("");
			$("#petreport_form_contact_email_field").html("");
		}
	});		


});