

$(document).ready(function(){

	var curYear = new Date().getUTCFullYear();
	$("#id_date_born").datepicker({changeMonth: true, changeYear: true, yearRange: '1950:curYear'});

	//Calculate the user's age
	$("#id_date_born").bind('change',function() {

		var now = new Date();
	  	var born = new Date($(this).attr("value"));
		var age = Math.floor((now.getTime() -  born.getTime()) / (365.25 * 24 * 60 * 60 * 1000));    
	    //document.getElementById('id_age').value = age;
	    if (age>18){
	    	// alert("old than 18.")
	    	$("#id_tc_link").attr("href", "/tc");
		}
		else{
			// alert("18 or younger")
			$("#id_tc_link").attr("href",  "/tc_18");
		}

	});


	// $("#id_y").bind('change',function() {

	//     // var curYear = new Date().getUTCFullYear();
	//     // var age = curYear - document.getElementById('id_y').value;
	//  	var mm = document.getElementById('id_m').value;
	//     var dd = document.getElementById('id_d').value;;
	//     var yy = document.getElementById('id_y').value;
	//     var now = new Date();
	//     var born = new Date();
	//     born.setFullYear(yy, mm-1, dd);
	// 	var age = Math.floor((now.getTime() - born.getTime()) / (365.25 * 24 * 60 * 60 * 1000));    
	//     document.getElementById('id_age').value = age;

	// });


	//Link to click to open to the T&C dialog box
	$("#id_tc_link").click(function(){

		if ($("#id_date_born").attr('value') == ""){
			alert("Sorry! You need to enter your date of birth.")
			document.getElementById("id_date_born").focus();		
		}
		else{
			var link = $(this);
			return load_dialog(link.attr("href"), link.attr("name"), 600, "auto");
		}

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

