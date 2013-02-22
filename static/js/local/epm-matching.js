//This function allows us to prepare HTML elements and their activites upon load of the HTML page.
$(document).ready(function(){

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
			move_petreport_to_workspace_match_detail(CANDIDATE_PETREPORT, img);
			
		}
	});	

	//Click Event handler for the target petreport in the Workspace.
	$("#prtarget .target").click(function(){

		//Grab the Image from the target petreport and copy it in the Workspace Detail Div.
		var img = $(this);
		move_petreport_to_workspace_match_detail(TARGET_PETREPORT, img);

	});	


	$("#button_propose_match").click(function(){

		var link = URL_PROPOSE_MATCH + TARGET_PETREPORT.id + "/" + CANDIDATE_PETREPORT.id + "/";
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

	//Fill up the field list.
	display_PetReport_fields(petreport, $(".prdpfields"));

	//Turn on the Workspace detail div.
	workspace_match_detail.show(); 
}

function moveImage(item, container) {

	var petreport_img = $(item).find("img").clone();

	//Animate the drop!
	var w = container.width();
	var h = container.height();
	petreport_img.animate({height: h, width: w});
	$(container).html(petreport_img);

	//Show the details of a candidate petreport after dropping its image to the droppable container
	move_petreport_to_workspace_match_detail(CANDIDATE_PETREPORT, petreport_img);

}

function show_prdp_dialog (link){

	//load_dialog(link, title, width, height)
	return load_dialog(link.attr("href"), link.attr("name"), 700, "auto")
}
