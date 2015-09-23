//This function allows us to prepare HTML elements and their activites upon load of the HTML page.
$(document).ready(function(){
	var pageNum = 1;
	var resizeTimer;

	$(window).bind("resizeEnd", function(){
		refresh_layout();
	});

	$(window).resize(function() {
		if(this.resizeTO) 
			clearTimeout(this.resizeTO);
		this.resizeTO = setTimeout(function() {
			$(this).trigger('resizeEnd');
		}, 250);
	});

	//Click Handler for the Propose Match button.
	$("#button_propose_match").click(function(){
		$("#epm-modal").modal({
			"remote": MATCHING_URLS["PROPOSE"] + TARGET_PETREPORT_ID + "/" + CANDIDATE_PETREPORT_ID + "/"
		});
	});

	/***** Start things off. *****/

	//Click Handler for Target. 
	$("#matching-workspace-target-img img").click(function(){
		$("#epm-modal").modal({
			"remote": REPORTING_URLS["PETREPORT"] + TARGET_PETREPORT_ID
		}); 
	});

	//Need to subscribe to several DnD events.
	$("#matching-workspace-candidate-img").on("dragenter", handleDragEnter);
	$("#matching-workspace-candidate-img").on("dragover", handleDragOver);
	$("#matching-workspace-candidate-img").on("drop", handleDrop);
	$("#matching-workspace-candidate-img").on("dragleave", handleDragLeave);		

	//Add more items when user scrolls down!
	$("#tiles").scroll(function() {
		if($(this).scrollTop() + $(this).innerHeight() == $(this)[0].scrollHeight - 1)
			fetch_PetReports(pageNum++);
	});			

	//Make the first call to fetch PetReports!
	fetch_PetReports(pageNum++);

}); //end of document.ready()

/******************************* Utility functions *******************************************/

var dragSrcEl = null;
function handleDragStart(ev){ 
	this.style.opacity = "0.4"; 
	dragSrcEl = this;
}

function handleDragEnter(ev){ this.classList.add("over"); }
function handleDragOver(ev){
	if (ev.preventDefault)
		ev.preventDefault();
	return false;
}
function handleDragLeave(ev){ this.classList.remove("over"); }

//The Workspace Candidate Image assumes (this).
function handleDrop(ev){
	if (ev.stopPropagation)
		ev.stopPropagation();

	moveImage(dragSrcEl, $("#matching-workspace-candidate-img"));	
	return false;
}

//The Workspace Candidate Image assumes (this).
function handleDragEnd(ev){ this.style.opacity = "1.0";}

function refresh_layout(){
	// Prepare layout options.
	var options = {
		autoResize: true, // This will auto-update the layout when the browser window is resized.
		container: $('#tiles'), // Optional, used for some extra CSS styling
		offset:10,
		outerOffset: 20
	};

	$("#tiles li").attr("draggable", true);
	$("#tiles li").each(function(i, item){
		$(item).on("dragstart", handleDragStart);
		$(item).on("dragend", handleDragEnd);	
	});

	// Call the layout function.
	var handler = $('#tiles li');	
	handler.wookmark(options);
}

//This function accepts the draggable item and the container within which the item is placed, 
//and it makes an AJAX call to get the item's inherited PetReport attributes to display.
function moveImage(item, container) {
	var petreport_img = $(item).find("img").clone();
	var petreport_id = $(item).find("a").attr("identity");

	//Make an AJAX Call to get attributes for the Candidate PetReport.
	perform_AJAX_call({
		type: "GET",
		url: REPORTING_URLS["PETREPORT_JSON"],
		data: {"petreport_id": petreport_id},
		success: function(data){
			//Show the details of a candidate petreport after dropping its image to the droppable container
			var petreport = data.petreport;
			CANDIDATE_PETREPORT_ID = petreport.id;

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
				$(container).html(""); //Bring Workspace state back to initial state.
				$(container).append("<strong style='width:100%; margin-top:50%; display:inline-block; text-align:center; color:gray;'> Click and Drag a Pet Here </strong>");
				clear_PetReport_fields_to_table(1, $("#matching-info-table"));
				$("#target_prdpfields li").each(function(){ $(this).css("color", "black"); });
				$("#button_propose_match").prop("disabled", true);
				$(this).prop("disabled", true);
			});

			//Create the click handler for this candidate.
			$("#matching-workspace-candidate-img img").click(function(){ 
				$("#epm-modal").modal({
					"remote": REPORTING_URLS["PETREPORT"] + CANDIDATE_PETREPORT_ID
				});				
			});

			//Fill up the field list.
			set_PetReport_fields_to_table(petreport, 1, $("#matching-info-table"));	

			//Now, iterate through both lists and highlight the matches!
			highlight_field_matches($("#matching-info-table"));		
	
		}
	});
}

function fetch_PetReports(page){
	perform_AJAX_call({
    type:"GET",
    url: MATCHING_URLS["CANDIDATE_PETREPORTS"],
    data:{"target_petreport_id": TARGET_PETREPORT_ID, "page":page},
    success: function(data){
    	var petreports = data.pet_reports_list;
    	var count = data.count;
    	var total_count = data.total_count;

			//Create each tile and its elements.
			for (var i = 0; i < petreports.length; i++){
				var report = petreports [i];

				//Setup PetReport Tile here.
				var item = setup_petreport_item(report, $("#epm-modal"));
				$(item).css("cursor", "move");

				//Finally, add this item to the tiles.
				$("#tiles").append(item);		
			}
			//Don't forget to refresh the grid layout.
			refresh_layout();
		}
  });
}



