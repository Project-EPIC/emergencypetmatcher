//This function allows us to prepare HTML elements and their activites upon load of the HTML page.
$(document).ready(function(){

	//Click Handler for the Propose Match button.
	$("#button_propose_match").click(function(){
		var link = URL_PROPOSE_MATCH + TARGET_PETREPORT.id + "/" + CANDIDATE_PETREPORT.id + "/";
		load_dialog({
			"link": link, 
			"title": "Propose Match", 
			"width": 800
		});
	});

	/***** Start things off. *****/

	//Click Handler for Target.
	$("#matching_workspace_target_img img").click(function(){ 
		load_dialog({
			"link": URL_PRDP + TARGET_PETREPORT.id, 
			"title": TARGET_PETREPORT.pet_name, 
			"width": SIZE_WIDTH_PRDP
		});
	});

	//display fields of the target pet report
	display_PetReport_fields({ "petreport": TARGET_PETREPORT, "list": $("#target_prdpfields") });

	//Setup PetReport Pagination here.
	$(".pagination").pagination({
		items:CANDIDATE_COUNT,
		itemsOnPage:50,
		cssStyle:"light-theme",
		onPageClick: function(pageNum){
			fetch_PetReports(pageNum);
		}
	});

	//It's important to adjust pagination width for centering.
	var numPages = $(".pagination").pagination("getPagesCount");
	numPages = (numPages > 10) ? 10 : numPages;
	$(".pagination_container").css("width", 110 + 35 * numPages);
	$(".pagination").pagination("redraw");		

	//Make the first call to fetch PetReports!
	fetch_PetReports(1);

}); //end of document.ready()

/******************************* Utility functions *******************************************/

function refresh_layout(){
	// Prepare layout options.
	var options = {
		autoResize: true, // This will auto-update the layout when the browser window is resized.
		container: $('#tiles'), // Optional, used for some extra CSS styling
		offset:10
	};

	// Get a reference to your grid items.
	var handler = $('#tiles li.item');

	//Make the Candidate Petreports draggable.
	$("#tiles li.item").draggable({ 
		zIndex:10,
		revert: "invalid",
		helper: "clone",
		stack: "#tiles .droppable"
	});	

	//Make the Candidate workspace droppable.
	$(".droppable").droppable({
		/* activeClass: "ui-state-hover", */
		hoverClass: "ui-state-active",
		accept: ".item",
		drop: function (event, ui) {
			moveImage(ui.draggable, $(this));
		}
	});	

	// Call the layout function.
	handler.wookmark(options);
}

//This function accepts the draggable item and the container within which the item is placed, 
//and it makes an AJAX call to get the item's inherited PetReport attributes to display.
function moveImage(item, container) {
	var petreport_img = $(item).find("img").clone();
	var petreport_a = $(item).find("a");
	var petreport_id = $(petreport_a).attr("identity");

	//Make an AJAX Call to get attributes for the Candidate PetReport.
	$.ajax({
		type:"GET",
		url: URL_GET_PETREPORT + petreport_id,
		success: function(data){
			//Show the details of a candidate petreport after dropping its image to the droppable container
			var petreport = CANDIDATE_PETREPORT = data.petreport;

			//Animate the drop!
			var w = container.width();
			var h = container.height();
			petreport_img.animate({height: h, width: w});
			$(container).html(petreport_img);		

			//Enable the Propose Match and Clear buttons.
			$("#button_propose_match").removeAttr("disabled");
			$("#button_clear_candidate").removeAttr("disabled");

			//Clear button to remove Candidate from droppable container.
			$("#button_clear_candidate").click(function(){

				//Bring Workspace state back to initial state.
				$(container).html("");
				$(container).append("<strong style='width:100%; margin-top:50%; display:inline-block; text-align:center; color:gray;'> Click and Drag a Pet Here </strong>");
				$("#candidate_prdpfields").html("");
				$("#target_prdpfields li").each(function(){ $(this).css("color", "black"); });
				$("#button_propose_match").prop("disabled", true);
				$(this).prop("disabled", true);
			});

			//Create the click handler for this candidate.
			$("#matching_workspace_candidate_img img").click(function(){ 
				load_dialog({
					"link": URL_PRDP + CANDIDATE_PETREPORT.id, 
					"title": CANDIDATE_PETREPORT.pet_name, 
					"width": SIZE_WIDTH_PRDP
				});
			});

			//Fill up the field list.
			display_PetReport_fields({ "petreport": petreport, "list":$("#candidate_prdpfields") });	

			//Now, iterate through both lists and highlight the matches!
			highlight_field_matches($("#target_prdpfields"), $("#candidate_prdpfields"));		
	
		},
		error: function(data){
			alert("An unexpected error occurred when trying to get information for this Pet. Please try again."); 
		}
	});
}

function fetch_PetReports(page){
	//First, remove all tile elements
	$("#tiles li.item").remove();
	$("#tiles h3").remove();
	$.ajax({
	    type:"GET",
	    url:URL_MATCHING + TARGET_PETREPORT.id + "/" + page,
	    success: function(data){
	    	var petreports = data.pet_reports_list;
	    	var count = data.count;
	    	var total_count = data.total_count;

			//Create each tile and its elements.
			for (var i = 0; i < petreports.length; i++){
				var report = petreports [i];

				//Setup PetReport Tile here.
				var item = setup_petreport_item(report);

				//Finally, add this item to the tiles.
				$("#tiles").append(item);		
			}

			if (petreports.length == 0)
				$("#tiles").append("<strong style='width:100%; display:inline-block; text-align:center;'> No Pets Available! </strong>");			
			
			//Don't forget to refresh the grid layout.
			refresh_layout();
		},
		error: function(data){
			alert("An unexpected error occurred when trying to get Pet Reports. Please try again."); 
	    }	
  	});
}

//Helper for setting up PetReport Tile.
function setup_petreport_item(report){
	var item = document.createElement("li");
	var alink = document.createElement("a");
	var pet_img = document.createElement("img");

	//Deal with attributes.
	$(item).addClass("item");
	//$(item).width(150);
	//$(item).height(150);
	//$(item).css("margin", "10px");

	$(alink).attr("name", report.pet_name);
	$(alink).attr("link", URL_PRDP + report.ID);
	$(alink).attr("identity", report.ID);
	$(alink).on("click", function(){
		load_dialog({
			"link": $(this).attr("link"), 
			"title": $(this).attr("name"),
			"width": SIZE_WIDTH_PRDP
		});
	});

	$(pet_img).attr("src", STATIC_URL + report.img_path);
	$(pet_img).width(150);
	$(pet_img).height(150);
	$(pet_img).css("margin", "0 auto");

	//Appends
	$(alink).append("<strong style='display:block; text-align:center;'>" + report.pet_name + "</strong>");
	$(alink).append("<span style='display:block; text-align:center;'>Contact: " + report.proposed_by_username + "</span>");					
	$(alink).append(pet_img);
	$(item).append(alink);					
	return item;
}



