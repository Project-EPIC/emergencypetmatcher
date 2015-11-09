$(document).ready(function(){
	$("#epm-nav-links .nav-link-home").toggleClass("active");
	var pageNum = 1;

	//Retrieve Items!
	$("#epm-choices li").click(function(e){
		fetch_pet_data(this, pageNum=1, clear=true);
	});

	//Add more items when user scrolls down!
	$(window).scroll(function() {
		if ($(window).scrollTop() + $(window).height() == $(document).height())
			fetch_pet_data("#epm-choices li.active", ++pageNum, clear=false);
	});

	/***** Start things off. *****/

	//Trigger the click event to retrieve PetReports.
	fetch_pet_data($("#epm-choices-petreports"), pageNum=1, clear=true)

	//Refresh.
	refresh_layout();

	$("#filter-submit").click(function(){
		fetch_pet_data("#epm-choices-petreports", pageNum=1, clear=true);
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

function fetch_pet_data(tab, page, clear){
	id = $(tab).attr("id");
	switch (id){
		case "epm-choices-petreports":
		$("#pet-report-filter-form").css("display", "block");
		fetch_PetReports(page, clear);
		break;

		case "epm-choices-petmatches":
		$("#pet-report-filter-form").css("display", "none");
		fetch_PetMatches(page, clear);
		break;

		case "epm-choices-reunited-pets":
		$("#pet-report-filter-form").css("display", "none");
		fetch_PetReunions(page, clear);
		break;

		case "epm-choices-bookmarked":
		$("#pet-report-filter-form").css("display", "none");
		fetch_bookmarks(page, clear);
		break;

		case "epm-choices-activity":
		$("#pet-report-filter-form").css("display", "none");
		fetch_activities(page, clear);
		break;
	}

	//Toggle the active nav tab inactive, and toggle the pets tab active.
	$("#epm-choices li.active").toggleClass("active");
	$("#" + id).toggleClass("active");
}

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

function fetch_PetReports(page, clear){
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

			for (var i = 0; i < petreports.length; i++){
				var report = petreports [i];
				var item = setup_petreport_item(report);
				$("#tiles").append(item);
			}

			if (petreports.length == 0 && page == 1)
				$(".tab-subtitle").text("No Pets Available Yet!");
			else{
				$(".tab-subtitle").text("Click on a Pet to Begin Matching. Scroll down to see more pets!");
			}

			$("#tiles-wait").css("display", "none");
			refresh_layout();
		},
		error: function(data){
				alert("An unexpected error occurred when trying to get Pets. Please try again!");
				$(".tab-content .tab-subtitle").text("No Pets Available Yet!");
			}
		});
}

function fetch_PetMatches(page, clear){
	if (clear == true)
		$("#tiles li").remove();

	$("#tiles-wait").css("display", "block");

	perform_AJAX_call({
		type:"GET",
		url: MATCHING_URLS["PETMATCHES_JSON"],
		data: {"page":page},
		success: function(data){
			var matches = data.pet_matches_list;
			var count = data.count;
			var total_count = data.total_count;

			//Create each tile and its elements.
			for (var i = 0; i < matches.length; i++){
				var match = matches [i];
				//Setup PetMatch tile here.
				var item = setup_petmatch_item(match);
				//Finally, add this item to the tiles.
				$("#tiles").append(item);
			}

			if (matches.length == 0 && page == 1)
				$(".tab-subtitle").text("No Pet Matches Available Yet!");
			else
				$(".tab-subtitle").text("Click on a Pet Match to Vote on it. Scroll down to see more matches!");

			$("#tiles-wait").css("display", "none");
			refresh_layout();
		},
		error: function(data){
			alert("An unexpected error occurred when trying to get Pet Matches. Please try again.");
			$(".tab-content .tab-subtitle").text("No Pet Matches Available Yet!");
		}
	});
}


//Function to fetch the local activities using AJAX GET
function fetch_activities(page, clear){
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

		 		var li = setup_activity_item(activity);
		 		activity_list.append(li);
		 	}

		 	if (activities.length == 0 && page == 1)
		 		$(".tab-subtitle").text("No Activities Yet.");
		 	else
		 		$(".tab-subtitle").html("Check out what these digital volunteers are doing. Scroll down to see more!")

		 	$("#tiles-wait").css("display", "none");
		 	refresh_layout();
		},
		error: function(data){alert("An unexpected error occurred when trying to retrieve activities. Please try again.");}
	});
}

function fetch_bookmarks(page, clear){
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
				var item = setup_petreport_item(report);
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

				$("#tiles").append(item);
			}

			if (bookmarks.length == 0 && page == 1)
				$(".tab-subtitle").text("No Pets Available Yet!");
			else
				$(".tab-subtitle").text("Select a Pet to Begin Matching. Scroll down to see more bookmarks!");

			$("#tiles-wait").css("display", "none");
			refresh_layout();
		},
		error: function(data){ alert("An unexpected error occurred when trying to get bookmarks. Please try again.");}
	});
}

function fetch_PetReunions(page, clear){
	if (clear == true)
		$("#tiles li").remove();
	$("#tiles-wait").css("display", "block");

	perform_AJAX_call({
		type:"GET",
		url: VERIFYING_URLS["PETREUNIONS_JSON"],
		data: {"page":page},
		success: function(data){
			var petreunions = data.pet_reunions_list;
			var count = data.count;
			var total_count = data.total_count;

			//Create each tile and its elements.
			for (var i = 0; i < petreunions.length; i++){
				var reunion = petreunions [i];
				var item = setup_petreunion_item(reunion);
				$("#tiles").append(item);
			}

			if (petreunions.length == 0 && page == 1)
				$(".tab-subtitle").text("No Pet Reunions Available Yet!");
			else
				$(".tab-subtitle").text("Welcome Home Pets!");

			$("#tiles-wait").css("display", "none");
			refresh_layout();
		},
		error: function(data){ alert("An unexpected error occurred when trying to get bookmarks. Please try again.");}
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
