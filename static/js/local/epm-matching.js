//This function allows us to prepare HTML elements and their activites upon load of the HTML page.
$(document).ready(function(){

	/*Sticky - Make sure the workspace is fixed when scrolling down the page.
	$.waypoints.settings.scrollThrottle = 30;
	$('#workspace').waypoint(function(event, direction){
		$(this).parent().toggleClass('sticky', direction === "down");
		event.stopPropagation();
	}); */

	//Make the workspace dotted boxed divs droppable.

	//Click Handler for the Propose Match button.
	$("#button_propose_match").click(function(){
		var link = URL_PROPOSE_MATCH + TARGET_PETREPORT.id + "/" + CANDIDATE_PETREPORT.id + "/";
		load_dialog(link, "Propose Match", 900, "auto");
	});

	/***** Start things off. *****/

	//Click Handler for Target.
	$("#matching_workspace_target_img img").click(function(){ load_dialog(URL_PRDP + TARGET_PETREPORT.id, TARGET_PETREPORT.pet_name, SIZE_WIDTH_PRDP, "auto"); });

	//display fields of the target pet report
	display_PetReport_fields(TARGET_PETREPORT, $("#target_prdpfields"));	

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
		offset:5,
		itemWidth: 175 // Optional, the width of a grid item
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
				load_dialog(URL_PRDP + CANDIDATE_PETREPORT.id, CANDIDATE_PETREPORT.pet_name, SIZE_WIDTH_PRDP, "auto"); 
			});

			//Fill up the field list.
			display_PetReport_fields(petreport, $("#candidate_prdpfields"));	

			//Now, iterate through both lists and highlight the matches!
			highlight_matches($("#target_prdpfields"), $("#candidate_prdpfields"));		
	
		},
		error: function(data){
			alert("An unexpected error occurred when trying to get information for this Pet. Please try again."); 
		}
	});
}

function highlight_matches(list1, list2){
	//First, initialize and clear off pre-existing highlights.
	var items1 = $(list1).children("li");
	var items2 = $(list2).children("li");
	$(items1).each(function(){ $(this).css("color", "black"); });
	$(items2).each(function(){ $(this).css("color", "black"); });

	//Iterate through each field and check if the value matches in both lists.
	for (var i = 0; i < items1.length; i++){
		innerText1 = items1[i].innerText;
		innerText2 = items2[i].innerText;

		if (innerText1.match("Tag and Collar Information:") != null)
			continue;

		if (innerText1.match("Description:") != null)
			continue;

		if (innerText1 == "" || innerText2 == "")
			continue;

		if (innerText1 == innerText2){
			$(items1[i]).css("color", "blue");
			$(items2[i]).css("color", "blue");
		}
	}
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
	$(item).width(150);
	$(item).height(150);
	$(item).css("margin", "10px");

	$(alink).attr("name", report.pet_name);
	$(alink).attr("link", URL_PRDP + report.ID);
	$(alink).attr("identity", report.ID);
	$(alink).on("click", function(){
		load_dialog($(this).attr("link"), $(this).attr("name"), SIZE_WIDTH_PRDP, "auto");
	});

	$(pet_img).attr("src", STATIC_URL + report.img_path);
	$(pet_img).width(120);
	$(pet_img).height(120);
	$(pet_img).css("margin", "0 auto");

	//Appends
	$(alink).append("<strong>" + report.pet_name + "</strong><br/>");
	$(alink).append("Contact: " + report.proposed_by_username);					
	$(alink).append(pet_img);
	$(item).append(alink);					
	return item;
}



