//This function allows us to prepare HTML elements and their activites upon load of the HTML page.
$(document).ready(function(){

    //Keep dibs on the latest candidate petreport looked at.
    CANDIDATE_PETREPORT_ID = null;

	$('#tiles').imagesLoaded(function(){

		// Prepare layout options.
		var options = {
			autoResize: true, // This will auto-update the layout when the browser window is resized.
			container: $('#matching_container'), // Optional, used for some extra CSS styling
			offset: 2, // Optional, the distance between grid items
			itemWidth: 210 // Optional, the width of a grid item
		};

		// Get a reference to your grid items.
		var handler = $('#tiles li.item');

		// Call the layout function.
		handler.wookmark(options);
	});

	//Allow for each candidate petreport to pop up its PRDP upon click.
	$("#prdpdialog a").click(function(){ 
		show_prdp_dialog($(this)); 
		return false;
	});					

	/*Sticky - Make sure the workspace is fixed when scrolling down the page.
	$.waypoints.settings.scrollThrottle = 30;
	$('#workspace').waypoint(function(event, direction){
		$(this).parent().toggleClass('sticky', direction === "down");
		event.stopPropagation();
	}); */

	//Make the Candidate Petreports draggable.
	$("#tiles li.item").draggable({ 
		revert: "invalid",
		helper: "clone"
	});

	//Make the workspace dotted boxed divs droppable.
	$(".droppable").droppable({
		/* activeClass: "ui-state-hover", */
		hoverClass: "ui-state-active",
		drop: function (event, ui) {
			moveImage(ui.draggable, $(this));
		}
	});

	//Click Event handler for any candidate (Droppable) Petreport in the Workspace.
	$(".droppable").click(function(){

		if ($(this).has("img").length > 0){

			//Grab the Image from the candidate petreport and copy it in the Workspace Detail Div.
			var img = $(this).find("img");
			var petreport_id_element = $(this).find("#petreport_id");
			var petreport_id = $(petreport_id_element).attr("value");
			var success = get_PetReport_object(petreport_id, img);
			
		}
	});	

	//Click Event handler for the target petreport in the Workspace.
	$("#prtarget .target").click(function(){

		//Grab the Image from the target petreport and copy it in the Workspace Detail Div.
		var img = $(this);
		var success = get_PetReport_object(TARGET_PETREPORT_ID, img);

	});	


	$("#button_propose_match").click(function(){

		var link = URL_PROPOSE_MATCH + TARGET_PETREPORT_ID + "/" + CANDIDATE_PETREPORT_ID + "/";
		return load_dialog(link, "Propose Match", 900, "auto");

	});


	$("#button_bookmark_pet").click(function(){
		alert("BOOKMARK PET");
	});


	$("#workspace_match_detail .matching_img").click(function(){
		var link = $(this).find('a');
		show_prdp_dialog(link);
		return false;

	});

}); //end of document.ready()


/******************************* Utility functions *******************************************/

function move_petreport_to_workspace_match_detail (petreport, img){

	var img_src = img.attr("src");
	var workspace_match_detail = $("#workspace_match_detail");

	//If the workspace match detail div does not yet contain an img element...
	workspace_match_detail.find(".matching_img").html("<a href = '" + URL_PRDP + 
		petreport.id + "/' name = " + petreport.pet_name + "><img src= '" + img_src + "'/></a>");

	//Change the border colors as necessary.
	$(".droppable").each(function(){ $(this).css("border-color", "black"); });
	$("#prtarget .target").css("border-color", "black");

	//We are showing a Candidate Pet Report here.
	if (img.parent().hasClass("droppable") == true){

		img.parent().css("border-color", "yellow");

		//Update the candidate petreport id.
		CANDIDATE_PETREPORT_ID = petreport.id;

		//Show both the "Propose Match" and "Bookmark Pet" Buttons.
		$("#button_propose_match").show();
		$("#button_bookmark_pet").show();				
	}

	//We are showing the Target PetReport here.
	else {

		img.css("border-color", "yellow");

		//Hide both the "Propose Match" and "Bookmark Pet" Buttons - It doesn't make any sense to show them.
		$("#button_propose_match").hide();
		$("#button_bookmark_pet").hide();
	}

	//TODO: Fill up the list.
	$(".matching_petname").html("<b>Pet Name:</b> " + petreport.pet_name);
	$(".matching_lost_found").html("<b>Lost/Found:</b> " + petreport.status);
	$(".matching_contact").html("<b>Contact:</b> <a href= '" + URL_USERPROFILE + petreport.proposed_by + "/' >" + petreport.proposed_by_username + "</a>");
	$(".matching_date").html("<b>Date Lost/Found:</b> " + petreport.date_lost_or_found);
	$(".matching_location").html("<b>Location:</b> " + petreport.location);
	$(".matching_age").html("<b>Age:</b> " + petreport.age);
	$(".matching_sex").html("<b>Sex:</b> " + petreport.sex);
	$(".matching_breed").html("<b>Breed:</b> " + petreport.breed);
	$(".matching_color").html("<b>Color:</b> " + petreport.color);
	$(".matching_size").html("<b>Size:</b> " + petreport.size);
	$(".matching_desc").html("<b>Description:</b> <div class = 'pr_desc' style='border: 1px dotted'>" + petreport.description + "</div>");

	//Turn on the Workspace detail div.
	workspace_match_detail.show(); 
}

function moveImage(item, container) {

	var petreport_img = $(item).find("img").clone();
	var petreport_id_element = $(item).find("#petreport_id").clone();
	var petreport_id = petreport_id_element.attr("value");

	//get the PetReport object via AJAX call.
	var success = get_PetReport_object(petreport_id, petreport_img);
	
	//Animate the drop!
	var w = container.width();
	var h = container.height();
	petreport_img.animate({height: h, width: w});
	$(container).html(petreport_img);

	//Safeguard the ID Hidden Input element tag inside of the Droppable div.
	$(container).prepend(petreport_id_element);
}

function get_PetReport_object (petreport_id, img){

	$.ajax({

		type:"GET",
		url: URL_PETREPORT_JSON + petreport_id + "/",
		success: function(data){
			var petreport = data;
			move_petreport_to_workspace_match_detail(petreport, img);
		},
		error: function(data){
			alert("An unexpected error occurred when trying to retrieve this Pet Report's attributes. Please try again."); 
			return false;
		}
	});
}


function show_prdp_dialog (link){

	//load_dialog(link, title, width, height)
	return load_dialog(link.attr("href"), link.attr("name"), 700, "auto")
}
