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
			fetch_PetReports(pageNum++, true);
			break;

			case "epm-choices-petmatches":
			$("#pet-report-filter-form").css("display", "none");
			fetch_PetMatches(pageNum++, false, true);
			break;

			case "epm-choices-reunited-pets":
			$("#pet-report-filter-form").css("display", "block");
			fetch_PetMatches(pageNum++, true, true);
			break;

			case "epm-choices-bookmarked":
			$("#pet-report-filter-form").css("display", "block");
			fetch_bookmarks(pageNum++, true);
			break;

			case "epm-choices-activity":
			$("#pet-report-filter-form").css("display", "none");
			fetch_activities(pageNum++, true);
			break;
		}		
	});

	//Add more items when user scrolls down!
	$(window).scroll(function() {
		if ($(window).scrollTop() + $(window).height() == $(document).height()) {
			id = $("#epm-choices li.active").attr("id");
			switch(id){
				case "epm-choices-petreports":
				fetch_PetReports(pageNum++, false);
				break;

				case "epm-choices-petmatches":
				fetch_PetMatches(pageNum++, false, false);
				break;

				case "epm-choices-reunited-pets":
				fetch_PetMatches(pageNum++, true, false);
				break;

				case "epm-choices-bookmarked":
				fetch_bookmarks(pageNum++, false);
				break;

				case "epm-choices-activity":
				fetch_activities(pageNum++, false);
				break;
			}
		}
	});	

	/***** Start things off. *****/
	//Trigger the click event to retrieve PetReports.
	$("#epm-choices-petreports").trigger("click");
	
	//Refresh.
	refresh_layout(); 		

	$(".pet-filter").change(function(){
		pageNum = 1;
		fetch_PetReports(pageNum++, true);
	});

}); //END document.ready()

/******************************* Utility functions *******************************************/


function get_pet_report_filter_options(){
	options = {	
		"pet_name": $("#filter-name").val(), 
		"status": $("#filter-status").val(), 
		"pet_type": $("#filter-type").val() 
	};
	$.each(options, function(key, value){
    if (value === "" || value === null)
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
		offset: offset, // Optional, the distance between grid items
	};

	// Now we're ready to call some wookmarking and update layout.
	var handler = $("#tiles li");
	handler.wookmark(options);
}

function fetch_PetReports(page, clear){
	if (clear == true)
		$("#tiles li").remove();		

	//Create Loading GIF
	img = document.createElement("img")
	img.src = STATIC_URL + "home/icons/loading.gif"
	$(".tab-content .tab-subtitle").html(img);
	options = get_pet_report_filter_options() //get pet report filter values.

	//AJAX Away.
	$.ajax({
		type:"GET",
		url: HOME_URLS["PETREPORTS_DATA"],
		data:{"page":page, "pet_name":options["pet_name"], "status":options["status"], "pet_type":options["pet_type"]},
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

			//Toggle the active nav tab inactive, and toggle the pets tab active.
			$("#epm-choices li.active").toggleClass("active");
			$("#epm-choices-petreports").toggleClass("active");

			if (petreports.length == 0 && page == 1)
				$(".tab-subtitle").text("No Pets Available Yet!");
			else
				$(".tab-subtitle").text("Click on a Pet to Begin Matching. Scroll down to see more pets!");

			//Don't forget to refresh the grid layout.
			refresh_layout(10);			
		},
		error: function(data){
				alert("An unexpected error occurred when trying to get Pets. Please try again!"); 
				$(".tab-content .tab-subtitle").text("No Pets Available Yet!");
			}	
		});
}

function fetch_PetMatches(page, successful_petmatches, clear){
	if (clear == true)
		$("#tiles li").remove();		

	//Create Loading GIF
	img = document.createElement("img")
	img.src = STATIC_URL + "home/icons/loading.gif"
	$(".tab-content .tab-subtitle").html(img);	

	//AJAX Away.
	$.ajax({
		type:"GET",
		url: HOME_URLS["PETMATCHES_DATA"],
		data: {"successful_petmatches": successful_petmatches, "page":page},
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
			//Toggle the active nav tab inactive, and toggle the petmatches (or successful PetMatches) tab active.
			$("#epm-choices li.active").toggleClass("active");

			if (successful_petmatches == true)
				$("#epm-choices-reunited-pets").toggleClass("active");
			else
				$("#epm-choices-petmatches").toggleClass("active");

			if (matches.length == 0 && page == 1)
				$(".tab-subtitle").text("No Pet Matches Available Yet!");
			else {
				if (successful_petmatches == true)
					$(".tab-subtitle").text("Welcome Home, Reunited Pets!");			
				else
					$(".tab-subtitle").text("Click on a Pet Match to Vote on it. Scroll down to see more matches!");			
			}

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
function fetch_activities(page, clear){
	if (clear == true)
		$("#tiles li").remove();		

	//Create Loading GIF
	img = document.createElement("img")
	img.src = STATIC_URL + "home/icons/loading.gif"
	$(".tab-content .tab-subtitle").html(img);		

	activity_list = $("#tiles");
	$.ajax ({
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

			//Toggle the active nav tab inactive, and toggle the Activities tab active.
			$("#epm-choices li.active").toggleClass("active");		 	
			$("#epm-choices-activity").toggleClass("active");			

		 	if (activities.length == 0 && page == 1)
		 		$(".tab-subtitle").text("No Activities Yet.");
		 	else {
		 		$(".tab-subtitle").html("Check out what these digital volunteers are doing. Scroll down to see more!")
		 		refresh_layout(10);	//Don't forget to refresh the grid layout.
		 	}
		},
		error: function(data){
			alert("An unexpected error occurred when trying to retrieve activities. Please try again."); 
		 	return false;
		}						
	});
}

function fetch_bookmarks(page, clear){
	if (clear == true)
		$("#tiles li").remove();		

	$.ajax({
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

			//Toggle the active nav tab inactive, and toggle the pets tab active.
			$("#epm-choices li.active").toggleClass("active");
			$("#epm-choices-bookmarked").toggleClass("active");

			if (bookmarks.length == 0 && page == 1)
				$(".tab-subtitle").text("No Pets Available Yet!");
			else
				$(".tab-subtitle").text("Select a Pet to Begin Matching. Scroll down to see more bookmarks!");			
			
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
		var csrf_value = $("input").attr("value");

		//ajax request to remove the bookmark
		$.ajax({ 
			type:"POST",
			url: REPORTING_URLS["BOOKMARK"],
			data: {"csrfmiddlewaretoken":csrf_value, "petreport_id":petreport_id, "user_id": user_id, "action":"Remove Bookmark"},

			success: function(data){
	    	$("#messages").html("<li class='success'>" + data.message + "</li>");
	    	parent.remove();
	    	refresh_layout();			            	
	    	return true;
	    },

	    error: function(data){
	    	alert("An unexpected error occurred when trying to bookmark this Pet. Please try again."); 
	    	return false;
	    }
	  });
	}
}

