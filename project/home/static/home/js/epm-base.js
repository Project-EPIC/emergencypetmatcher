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

	$("#filter-submit").click(function(){ add_filters_to_URL(); });
	$("#filter-clear").click(function(){
		$("#filter-pet-name").val("");
		$("#filter-status").val("All");
		$("#filter-event-tag").select2("val", "All");
		$("#filter-pet-type").val("All");
		$("#filter-breed").select2({
			tags: ["All"]
		});
		$("#filter-breed").select2("val", "All");
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

	$(document).keypress(function(e) {
    if(e.which == 13)
			$("#filter-submit").click();
	});

	//Listen for a change in the pet type. If the user selects a pet type, load the breeds for that pet type!
	// if ($("#filter-breed").val() == "All" || $("#filter-breed")[0].value == "Breed")
	load_breeds();
	$("#filter-pet-type").change(load_breeds);

}); //END document.ready()

/******************************* Utility functions *******************************************/

function load_breeds(){
	var pet_type = $("#filter-pet-type").val();
	if (pet_type != "All" && pet_type != null){
		load_pet_breeds(pet_type, function(data){
			$("#filter-breed").html("").select2({data: {id:null, text: null}});
			$("#filter-breed").select2({
				tags: ["All"].concat(data.breeds),
				maximumSelectionSize:1,
			});
			$("#filter-breed").select2("val", BREED);
		});
		$("#filter-breed").toggleClass("hidden");
	}
	// else
	// 	$("#filter-breed").addClass("hidden");
}

function fetch_pet_data(tab, page, clear){
	id = $(tab).attr("id");
	switch (id){

		case "epm-choices-petreports":
		$("#pet-report-filter-form").css("display", "block");
		fetch_items({
			clear: clear,
			url: REPORTING_URLS["PETREPORTS_JSON"],
			page: page,
			failMsg: "An unexpected error occurred when trying to get Pets. Please try again!",
			fun: function(data){
				display_items({
					items: data.pet_reports_list,
					page: page,
					failMsg: "No Pets Available Yet!",
					successMsg: "Click on a Pet to Begin Matching. Scroll down to see more pets!",
					fun: function(items){
						for (var i = 0; i < items.length; i++){
							var item = setup_petreport_item(items[i]);
							$("#tiles").append(item);
						}
					}
				});
			}
		});
		break;

		case "epm-choices-petmatches":
		$("#pet-report-filter-form").css("display", "none");
		fetch_items({
			clear: clear,
			url: MATCHING_URLS["PETMATCHES_JSON"],
			page: page,
			failMsg: "An unexpected error occurred when trying to get Pet Matches. Please try again.",
			fun: function(data){
				display_items({
					items: data.pet_matches_list,
					page: page,
					failMsg: "No Pet Matches Available Yet!",
					successMsg: "Click on a Pet Match to Vote on it. Scroll down to see more matches!",
					fun: function(items){
						for (var i = 0; i < items.length; i++){
							var item = setup_petmatch_item(items[i]);
							$("#tiles").append(item);
						}
					}
				});
			}
		});
		break;

		case "epm-choices-reunited-pets":
		$("#pet-report-filter-form").css("display", "none");
		fetch_items({
			clear: clear,
			url: VERIFYING_URLS["PETREUNIONS_JSON"],
			page: page,
			failMsg: "An unexpected error occurred when trying to get Pets. Please try again!",
			fun: function(data){
				display_items({
					items: data.pet_reunions_list,
					page: page,
					failMsg: "No Pet Reunions Available Yet!",
					successMsg: "Welcome Home Pets!",
					fun: function(items){
						for (var i = 0; i < items.length; i++){
							var item = setup_petreunion_item(items[i]);
							$("#tiles").append(item);
						}
					}
				});
			}
		});
		break;

		case "epm-choices-bookmarked":
		$("#pet-report-filter-form").css("display", "none");
		fetch_items({
			clear: clear,
			url: HOME_URLS["BOOKMARKS_DATA"],
			page: page,
			failMsg: "An unexpected error occurred when trying to get bookmarks. Please try again!",
			fun: function(data){
				display_items({
					items: data.bookmarks_list,
					page: page,
					failMsg:"No Pets Available Yet!",
					successMsg: "Select a Pet to Begin Matching. Scroll down to see more bookmarks!",
					fun: function(items){
						for (var i = 0; i < items.length; i++){
							var report = items[i];
							var item = setup_petreport_item(report);
							$(item).attr("petreport_id", report.ID)

							$(item).hover(function mouseenter(){ //Setup Mouse-enter and Mouse-leave events.
								var img = document.createElement("img");
								$(img).attr("src", STATIC_URL + "home/icons/button_bookmark_X.png");
								$(img).addClass("bookmark_x");

								$(img).hover(function mouseenter(){
									$(this).attr("src", STATIC_URL + "home/icons/button_bookmark_X_hover.png");
								}, function mouseleave(){
									$(img).attr("src", STATIC_URL + "home/icons/button_bookmark_X.png");
								});

								$(img).click(function(){
									var tile = $(img).parent();
									remove_bookmark($(tile).attr("petreport_id"), tile);
								});
								$(this).append(img);

							}, function mouseleave(){
								var img = $(this).find(".bookmark_x");
								img.remove();
							});
							$("#tiles").append(item);
						}
					}
				});
			}
		});
		break;

		case "epm-choices-activity":
		$("#pet-report-filter-form").css("display", "none");
		fetch_items({
			clear: clear,
			url: HOME_URLS["ACTIVITIES_DATA"],
			page: page,
			failMsg: "An unexpected error occurred when trying to get activities. Please try again!",
			fun: function(data){
				display_items({
					items: data.activities,
					page: page,
					failMsg: "No Activities Yet.",
					successMsg: "Check out what these digital volunteers are doing. Scroll down to see more!",
					fun: function(items){
						for (var i = 0; i < items.length; i++){
							var activity = items[i];
							if (activity.source == null)
								continue
							var li = setup_activity_item(activity);
							$("#tiles").append(li);
						}
					}
				});
			}
		});
		break;

		case "epm-choices-map":
		$("#pet-report-filter-form").css("display", "none");
		break;
	}

	//Toggle the active nav tab inactive, and toggle the pets tab active.
	$("#epm-choices li.active").toggleClass("active");
	$("#" + id).toggleClass("active");
}

function get_pet_report_filter_options(){
	filters = {
		pet_name: $("#filter-pet-name").val(),
		status: $("#filter-status").val(),
		event_tag: $("#filter-event-tag").val(),
		pet_type: $("#filter-pet-type").val(),
		breed: $("#filter-breed").val()
	};

	$.each(filters, function(key, value){
		if (value === "" || value === "null" || value == undefined || value == "All" || value == null)
        delete filters[key];
		});
	return filters;
}

function add_filters_to_URL(){
	var filters = get_pet_report_filter_options();
	var results = [];
	for (key in filters)
		results.push(key + "=" + filters[key]);
	if (results.length != 0)
		location.href = location.protocol + '//' + location.host + location.pathname + "?" + results.join("&");
	else
		location.href = location.protocol + '//' + location.host + location.pathname;
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

function display_items(options){
	options["fun"](options["items"]);
	if (options["items"].length == 0 && options["page"] == 1)
		$(".tab-subtitle").text(options["failMsg"]);
	else
		$(".tab-subtitle").text(options["successMsg"]);
	$("#tiles-wait").css("display", "none");
	refresh_layout();
}

function fetch_items(options){
	if (options["clear"] == true)
		$("#tiles li").remove();

	$("#tiles-wait").css("display", "block");
	filter_options = get_pet_report_filter_options();
	data = {"page": options["page"]}
	for (var attr in filter_options){ data[attr] = filter_options[attr]} //Merge options.
	perform_AJAX_call({
		type:"GET",
		url: options["url"],
		data: data,
		success: function(response){ options["fun"](response); },
		error: function(response){ $(".tab-subtitle").text(options["failMsg"]); }
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
