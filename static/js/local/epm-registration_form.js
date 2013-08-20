$(document).ready(function(){

	var curYear = new Date().getUTCFullYear();
	$("#id_date_born").datepicker({changeMonth: true, changeYear: true, yearRange: '1900:curYear'});

	//Calculate the user's age
	$("#id_date_born").bind('change', function() {
		var now = new Date();
	  	var born = new Date($(this).attr("value"));
		var age = Math.floor((now.getTime() -  born.getTime()) / (365.25 * 24 * 60 * 60 * 1000));    
	    //document.getElementById('id_age').value = age;

	    /* 
	    if (age > 18)
		else
		*/
	});

	//Check box to accept the T&C
	$("#id_tc_check").click(function(){

		if ($("#id_date_born").attr('value') == ""){
			$(this).attr("checked",false);
			alert("Sorry! You need to enter your date of birth.")			
			document.getElementById("id_date_born").focus();				
		}
		else{
			if($(this).prop("checked") == true)
				// $("#register_button").css({ "background-color": "red" });			
				document.getElementById("id_register_button").disabled = false;				
			else
				// $("#register_button").css({ "background-color": "green" });
				document.getElementById("id_register_button").disabled = true;
		}
	});		
	
});

