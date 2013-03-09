
$(document).ready(function(){


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


});