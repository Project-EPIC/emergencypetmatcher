//This function allows us to prepare HTML elements and their activites upon load of the HTML page.
$(document).ready(function(){
	$("#epm-nav-links .nav-link-home").toggleClass("active");
	var pageNum = 1;

	//Retrieve Items!
	$("#epm-choices li").click(function(e){
		id = $(this).attr("id");
		pageNum = 1
		switch(id){
			case "epm-choices-petreports":
			$("#pet-report-filter-form").css("display", "block");
			fetch_PetReports(id, pageNum++, clear=true);
			break;

			case "epm-choices-petmatches":
			$("#pet-report-filter-form").css("display", "none");
			fetch_PetMatches(id, pageNum++, clear=true, successful=false);
			break;

			case "epm-choices-reunited-pets":
			$("#pet-report-filter-form").css("display", "none");
			fetch_PetMatches(id, pageNum++, clear=true, successful=true);
			break;

			case "epm-choices-bookmarked":
			$("#pet-report-filter-form").css("display", "none");
			fetch_bookmarks(id, pageNum++, clear=true);
			break;

			case "epm-choices-activity":
			$("#pet-report-filter-form").css("display", "none");
			fetch_activities(id, pageNum++, clear=true);
			break;
		}

		//Toggle the active nav tab inactive, and toggle the pets tab active.
		$("#epm-choices li.active").toggleClass("active");
		$("#" + id).toggleClass("active");
	});

	//Add more items when user scrolls down!
	$(window).scroll(function() {
		if ($(window).scrollTop() + $(window).height() == $(document).height()) {
			id = $("#epm-choices li.active").attr("id");
			switch(id){
				case "epm-choices-petreports":
				fetch_PetReports(id, pageNum++, clear=false);
				break;

				case "epm-choices-petmatches":
				fetch_PetMatches(id, pageNum++, clear=false, successful=false);
				break;

				case "epm-choices-reunited-pets":
				fetch_PetMatches(id, pageNum++, clear=true, successful=true);
				break;

				case "epm-choices-bookmarked":
				fetch_bookmarks(id, pageNum++, clear=false);
				break;

				case "epm-choices-activity":
				fetch_activities(id, pageNum++, clear=false);
				break;
			}

			//Toggle the active nav tab inactive, and toggle the pets tab active.
			$("#epm-choices li.active").toggleClass("active");
			$("#" + id).toggleClass("active");
		}
	});	

	/***** Start things off. *****/
	//Trigger the click event to retrieve PetReports.
	$("#epm-choices-petreports").trigger("click");
	
	//Refresh.
	refresh_layout(); 		

	$("#filter-submit").click(function(){
		pageNum = 1;
		fetch_PetReports("epm-choices-petreports", pageNum++, true);
	});

	//Grab Event Tags.
	perform_AJAX_call({
		type:"GET",
		url:REPORTING_URLS["EVENT_TAGS"],
		data: {},
		success: function(data){
			$("#filter-event-tag").select2({
				tags: true,
				tags: data.event_tags,
				maximumSelectionSize:1,
			});
		}
	});

	//Listen for a change in the pet type. If the user selects a pet type, load the breeds for that pet type!
	$("#filter-type").change(function(){
		var pet_type = $(this).val();
		if (pet_type != "All"){
			load_pet_breeds(pet_type, function(data){
				$("#filter-breed").html("").select2({data: {id:null, text: null}});
				$("#filter-breed").select2({ 
					tags: data.breeds,
					maximumSelectionSize:1,
				});
			});
			$("#filter-breed").toggleClass("hidden");			
		}
		else
			$("#filter-breed").addClass("hidden");
	});		

}); //END document.ready()

/******************************* Utility functions *******************************************/


function get_pet_report_filter_options(){
	options = {	
		"pet_name": $("#filter-name").val(), 
		"status": $("#filter-status").val(), 
		"event_tag": $("#filter-event-tag").val(),
		"pet_type": $("#filter-type").val(),
		"breed": $("#filter-breed").val(),
	};
	$.each(options, function(key, value){
    if (value === "" || value === null || value == undefined || value == "All")
        delete options[key];
    });
	return options;
}

// Prepare layout for home page grid.
function refresh_layout(offset){
	if (offset == null)
		offset = 20

	var options = {
		autoResize: true, // This will auto-update the layout when the browser window is resized.
		container: $('#tiles'), // Optional, used for some extra CSS styling
		outerOffset: 20,
		verticalOffset:5,
		offset: offset, // Optional, the distance between grid items
	};

	// Now we're ready to call some wookmarking and update layout.
	$("#tiles li").wookmark(options);
}

function fetch_PetReports(tab, page, clear){
	if (clear == true)
		$("#tiles li").remove();		

	$("#tiles-wait").css("display", "block");
	options = get_pet_report_filter_options() //get pet report filter values.
	data = {"page":page}
	for (var attr in options){ data[attr] = options[attr]} //Merge options.

	perform_AJAX_call({
		type:"GET",
		url: REPORTING_URLS["PETREPORTS_JSON"],
		data: data,
		success: function(data){
			var petreports = data.pet_reports_list;
			var count = data.count;
			var total_count = data.total_count;

			//Create each tile and its elements.
			for (var i = 0; i < petreports.length; i++){
				var report = petreports [i];
				//Setup PetReport Tile here.
				var item = setup_petreport_item(report, $("#epm-modal"));
				//Finally, add this item to the tiles.
				$("#tiles").append(item);		
			}

			if (petreports.length == 0 && page == 1)
				$(".tab-subtitle").text("No Pets Available Yet!");
			else{
				$(".tab-subtitle").text("Click on a Pet to Begin Matching. Scroll down to see more pets!");
			}
			
			$("#tiles-wait").css("display", "none");

			//Don't forget to refresh the grid layout.
			refresh_layout(10);			
		},
		error: function(data){
				alert("An unexpected error occurred when trying to get Pets. Please try again!"); 
				$(".tab-content .tab-subtitle").text("No Pets Available Yet!");
			}	
		});
}

function fetch_PetMatches(tab, page, clear, successful){
	if (clear == true)
		$("#tiles li").remove();		

	$("#tiles-wait").css("display", "block");

	perform_AJAX_call({
		type:"GET",
		url: MATCHING_URLS["PETMATCHES_JSON"],
		data: {"successful_petmatches": successful, "page":page},
		success: function(data){
			var matches = data.pet_matches_list;
			var count = data.count;
			var total_count = data.total_count;

			//Create each tile and its elements.
			for (var i = 0; i < matches.length; i++){
				var match = matches [i];

				//Setup PetMatch tile here.
				var item = setup_petmatch_item(match, $("#epm-modal"));			

				//Finally, add this item to the tiles.
				$("#tiles").append(item);		
			}

			if (matches.length == 0 && page == 1)
				$(".tab-subtitle").text("No Pet Matches Available Yet!");
			else {
				if (successful == true)
					$(".tab-subtitle").text("Welcome Home, Reunited Pets!");		
				else
					$(".tab-subtitle").text("Click on a Pet Match to Vote on it. Scroll down to see more matches!");			
			}

			$("#tiles-wait").css("display", "none");

			//Don't forget to refresh the grid layout.
			refresh_layout();
		},
		error: function(data){
			alert("An unexpected error occurred when trying to get Pet Matches. Please try again."); 
			$(".tab-content .tab-subtitle").text("No Pet Matches Available Yet!");
		}	
	});
}


//Function to fetch the local activities using AJAX GET
function fetch_activities(tab, page, clear){
	if (clear == true)
		$("#tiles li").remove();		

	$("#tiles-wait").css("display", "block");
	activity_list = $("#tiles");

	perform_AJAX_call({
		type:"GET",
		url: HOME_URLS["ACTIVITIES_DATA"],
		data: {"page": page},
		success: function(data){
			var activities = data.activities;

			//Iterate through the activities and append them to the list.
			for (var i = 0; i < activities.length; i++){
				
				var activity = activities[i];

				if (activity.source == null)
					continue
				
		 		//Setup the list item.
		 		var li = setup_activity_item(activity, $("#epm-modal"));			 		
		 		activity_list.append(li);
		 	}

		 	if (activities.length == 0 && page == 1)
		 		$(".tab-subtitle").text("No Activities Yet.");
		 	else {
		 		$(".tab-subtitle").html("Check out what these digital volunteers are doing. Scroll down to see more!")
		 		refresh_layout(10);	//Don't forget to refresh the grid layout.
		 	}
		 	$("#tiles-wait").css("display", "none");
		},
		error: function(data){
			alert("An unexpected error occurred when trying to retrieve activities. Please try again."); 
		 	return false;
		}						
	});
}

function fetch_bookmarks(tab, page, clear){
	if (clear == true)
		$("#tiles li").remove();		

	$("#tiles-wait").css("display", "block");

	perform_AJAX_call({
		type:"GET",
		url: HOME_URLS["BOOKMARKS_DATA"],
		data: {"page": page},
		success: function(data){
			var bookmarks = data.bookmarks_list;
			var count = data.count;
			var total_count = data.total_count;

			//Create each tile and its elements.
			for (var i = 0; i < bookmarks.length; i++){
				var report = bookmarks [i];

				//Setup PetReport Tile here.
				var item = setup_petreport_item(report, $("#epm-modal"));
				$(item).attr("petreport_id", report.ID)

				//Setup Mouse-enter and Mouse-leave events.
				$(item).hover(function mouseenter(){
					var img = document.createElement("img");
					$(img).attr("src", STATIC_URL + "home/icons/button_bookmark_X.png");
					$(img).addClass("bookmark_x");

					$(img).hover(function mouseenter(){
						$(this).attr("src", STATIC_URL + "home/icons/button_bookmark_X_hover.png");
					}, function mouseleave(){
						$(img).attr("src", STATIC_URL + "home/icons/button_bookmark_X.png");
					});

					//Setup Bookmark remove click handler.
					$(img).click(function(){
						var tile = $(img).parent();
						remove_bookmark($(tile).attr("petreport_id"), tile);
					});							

					//Finally, append img to tile.
					$(this).append(img);

				}, function mouseleave(){
					var img = $(this).find(".bookmark_x");
					img.remove();
				});

				//Finally, add this item to the tiles.
				$("#tiles").append(item);		
			}

			if (bookmarks.length == 0 && page == 1)
				$(".tab-subtitle").text("No Pets Available Yet!");
			else
				$(".tab-subtitle").text("Select a Pet to Begin Matching. Scroll down to see more bookmarks!");			
			
			$("#tiles-wait").css("display", "none");

			//Don't forget to refresh the grid layout.
			refresh_layout();
		},
		error: function(data){
				alert("An unexpected error occurred when trying to get bookmarks. Please try again."); 
		}	
	});
}

function remove_bookmark(petreport_id, parent){
	var c = confirm("Are you sure you want to remove this bookmark?");
	if (c == true){
		var user_id = USER_ID;
		var csrf_value = $("input[name='csrfmiddlewaretoken']").attr("value");

		perform_AJAX_call({ 
			type:"POST",
			url: REPORTING_URLS["BOOKMARK"],
			data: {"csrfmiddlewaretoken":csrf_value, "petreport_id":petreport_id, "user_id": user_id, "action":"Remove Bookmark"},
			success: function(data){
				add_flash_message("success", data.message);
	    	parent.remove();
	    	refresh_layout();			            	
	    	return true;
	    },
	    error: function(data){
	    	add_flash_message("danger", "An unexpected error occurred when trying to bookmark this Pet. Please try again.")
	    	return false;
	    }
	  });
	}
}

