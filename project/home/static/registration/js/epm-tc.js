//This function allows us to prepare HTML elements and their activites upon load of the HTML page.

$(document).ready(function() {

    $.get(TC_FILE, function(data) {
 
    	//alert(data);
    	var lines = data.split("\n");
        $.each(lines, function(n, elem) {
        	
        	if (elem==""){
        		$('#id_TC_Content').append('</br>');
        	}
        	else{
            	$('#id_TC_Content').append('<div>' + elem + '</div>');
        	}
        });

    });

});

