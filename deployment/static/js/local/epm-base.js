//This function allows us to prepare HTML elements and their activites upon load of the HTML page.
$(document).ready(function(){

	//Retrieve PetMatches to show as tiles.
	$("#nav_petreports").click(function(){ 
		$(".pagination").pagination({
			items:PETREPORT_COUNT,
			itemsOnPage:50,
			cssStyle:"light-theme",
			onPageClick: function(pageNum){
				fetch_PetReports(pageNum);
			}
		});	

		//Adjust the pagination container for centering
		update_pagination();

		//Make the AJAX GET call here.
		fetch_PetReports(1); 
	});	

	//Retrieve PetMatches to show as tiles.
	$("#nav_petmatches").click(function(){ 
		$(".pagination").pagination({
			items:PETMATCH_COUNT,
			itemsOnPage:25,
			cssStyle:"light-theme",
			onPageClick: function(pageNum){
				fetch_PetMatches(pageNum, false);
			}
		});	

		//Adjust the pagination container for centering
		update_pagination();

		//Make the AJAX GET call here.
		fetch_PetMatches(1, false); 
	});	

	//Retrieve Bookmarks to show as tiles.
	$("#nav_bookmarked").click(function(){
		$(".pagination").pagination({
			items:BOOKMARK_COUNT,
			itemsOnPage:50,
			cssStyle:"light-theme",
			onPageClick: function(pageNum){
				fetch_bookmarks(pageNum);
			}
		});	

		//Adjust the pagination container for centering
		update_pagination();

		//Make the AJAX GET call here.
		fetch_bookmarks(1); 
	});

	//Retrieve Successful PetMatches to show as tiles.
	$("#nav_successful_petmatches").click(function(){
		$(".pagination").pagination({
			items:BOOKMARK_COUNT,
			itemsOnPage:50,
			cssStyle:"light-theme",
			onPageClick: function(pageNum){
				fetch_PetMatches(pageNum, true);
			}
		});	

		//Adjust the pagination container for centering
		update_pagination();

		//Make the AJAX GET call here.
		fetch_PetMatches(1, true); 
	})	

	//Update the share buttons on click.
	$("#facebook_share_epm").click(function(){ share_on_facebook(HOME_URL, HOME_IMAGE, HOME_TITLE, HOME_CAPTION, HOME_SUMMARY); });
	$("#twitter_share_epm").click(function(){ share_on_twitter(HOME_URL, HOME_IMAGE, HOME_TITLE, HOME_SUMMARY); });	

	/***** Start things off. *****/
	//Trigger the click event to retrieve PetReports.
	$("#nav_petreports").trigger("click");
	
	//Call the AJAX GET for activities.
	fetch_activities($("#feedlist"));	

	//Refresh.
	refresh_layout(); 		

}); //END document.ready()

/******************************* Utility functions *******************************************/

function refresh_layout(){
	// Prepare layout options.
	var options = {
		autoResize: true, // This will auto-update the layout when the browser window is resized.
		container: $('#tiles'), // Optional, used for some extra CSS styling
		offset: 10, // Optional, the distance between grid items
	};

	// Now we're ready to call some wookmarking and update layout.
	var handler = $("#tiles li.item");
	handler.wookmark(options);
}

function update_pagination(){
	//It's important to adjust pagination width for centering.
	var numPages = $(".pagination").pagination("getPagesCount");
	numPages = (numPages > 10) ? 10 : numPages;
	$(".pagination_container").css("width", 110 + 35 * numPages);
	$(".pagination").pagination("redraw");		
}

function fetch_PetReports(page){
	//First, remove all tile elements
	$("#tiles li.item").remove();
	$("#tile_container span").remove();
	$.ajax({
	    type:"GET",
	    url:URL_GET_PETREPORTS + "/" + page,
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

			//Toggle the active nav tab inactive, and toggle the pets tab active.
			$("#nav li.active").toggleClass("active");
			$("#nav_petreports").toggleClass("active");

			if (petreports.length == 0)
				$("#tile_container").prepend("<span style='margin:10px; display:block; font-size:24px; color:gray; text-align:center;'> No Pets Available Yet! </span>");
			else
				$("#tile_container").prepend("<span style='margin:10px; display:block; font-size:24px; color:gray; text-align:center;'> Select a Pet to Begin Matching.</span>");

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

	//Link attributes.
	$(item).addClass("item");
	$(alink).attr("name", report.pet_name);
	$(alink).attr("link", URL_PRDP + report.ID);
	$(alink).on("click", function(){
		load_dialog({
			"link": $(this).attr("link"),
			"title": $(this).attr("name"),
			"width": SIZE_WIDTH_PRDP
		});
	});

	//Pet Img attributes.
	$(pet_img).attr("src", STATIC_URL + report.img_path);
	$(pet_img).width(150);
	$(pet_img).height(150);
	$(pet_img).css("margin", "5px auto");
	$(pet_img).css("display", "block");

	//Appends
	$(alink).append("<strong style='display:block; text-align:center;'>" + report.pet_name + "</strong>");
	$(alink).append("<span style='display:block; text-align:center;'>Contact: " + report.proposed_by_username + "</span>");					
	$(alink).append(pet_img);
	$(item).append(alink);					
	return item;
}

function fetch_PetMatches(page, successful_petmatches){
	//First, remove all tile elements (except activity feed)
	$("#tiles li.item").remove();
	$("#tile_container span").remove();

	if (successful_petmatches == true)
		url = URL_GET_SUCCESSFUL_PETMATCHES + "/" + page;
	else
		url = URL_GET_PETMATCHES + "/" + page;

	$.ajax({
	    type:"GET",
	    url: url,
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

			//Toggle the active nav tab inactive, and toggle the petmatches (or successful PetMatches) tab active.
			$("#nav li.active").toggleClass("active");
			if (successful_petmatches == true)
				$("#nav_successful_petmatches").toggleClass("active");
			else
				$("#nav_petmatches").toggleClass("active");


			if (matches.length == 0)
				$("#tile_container").prepend("<span style='margin:10px; display:block; font-size:24px; color:gray; text-align:center;'> No Pet Matches Available Yet! </span>");
			else
				$("#tile_container").prepend("<span style='margin:10px; display:block; font-size:24px; color:gray; text-align:center;'> Select a Pet Match to Vote on it.</span>");			

			//Don't forget to refresh the grid layout.
			refresh_layout();
		},
		error: function(data){
			alert("An unexpected error occurred when trying to get Pet Matches. Please try again."); 
	    }	
  	});
}

//Helper for setting up PetMatch Tile.
function setup_petmatch_item (match){
	var item = document.createElement("li");
	var alink = document.createElement("a");
	var lost_pet_img = document.createElement("img");
	var found_pet_img = document.createElement("img");

	//Deal with Attributes.
	$(item).addClass("item");
	$(alink).attr("name", match.lost_pet_name + " with " + match.found_pet_name);					
	$(alink).attr("link", URL_PMDP + match.ID);
	$(alink).on("click", function(){
		load_dialog({
			"link": $(this).attr("link"), 
			"title": $(this).attr("name"), 
			"width": SIZE_WIDTH_PMDP
		});
	});

	$(lost_pet_img).attr("src", STATIC_URL + match.lost_pet_img_path);
	$(found_pet_img).attr("src", STATIC_URL + match.found_pet_img_path);
	$(lost_pet_img).width(150);
	$(lost_pet_img).height(150);
	$(lost_pet_img).css("margin", "5px auto");
	$(lost_pet_img).css("display", "block");	
	$(found_pet_img).width(150);
	$(found_pet_img).height(150);
	$(found_pet_img).css("margin", "5px auto");
	$(found_pet_img).css("display", "block");	
	$(lost_pet_img).css("border", "white solid 1px");
	$(found_pet_img).css("border", "white solid 1px");

	//Appends
	$(alink).append("<strong style='display:block; text-align:center;'>" + match.lost_pet_name + " with " + match.found_pet_name + "</strong>");
	$(alink).append("<span style='display:block; text-align:center;'>Contact: " + match.proposed_by_username + "</span>");					
	$(alink).append(lost_pet_img);
	$(alink).append(found_pet_img);
	$(item).append(alink);				
	return item;
}


//Function to fetch the local activities using AJAX GET
function fetch_activities (feedlist){
	$.ajax ({
		type:"GET",
		url: URL_GET_ACTIVITIES,
		success: function(data){
			var activities = data.activities;

			//Iterate through the activities and append them to the list.
		 	for (var i = 0; i < activities.length; i++){
		 		var activity_dict = activities [i];

		 		//Setup the list item.
		 		var li = setup_activity_item(activity_dict);			 		

		 		//Bad Li element - just get the next one.
		 		if (li == null)
		 			continue;

		 		feedlist.append(li);
			}

			if (activities.length == 0 || feedlist.children().length == 0)
				feedlist.append("<h3 style='font-color:gray; text-align:center;'> No Activities Yet.</h3>");

			return true;
		},

		error: function(data){
			alert("An unexpected error occurred when trying to retrieve the activities. Please try again."); 
			return false;
		}						
	});
}

//Given an activity payload, construct the list item and return the HTML li element.
function setup_activity_item (activity_dict){
	var activity = activity_dict.activity;

	if (activity_dict == undefined || activity == undefined)
		return null;		

	var current_userprofile_id = activity_dict.current_userprofile_id;
		var li = document.createElement("li");
		var userprofile_a = document.createElement("a");
		var a = document.createElement("a");
		$(li).css("margin-left", "2px");
		$(li).css("padding-left", "0px");
		//$(li).css("background", "#CCE6FF");
		$(userprofile_a).attr("href", URL_USERPROFILE + activity_dict.userprofile_id);
		$(userprofile_a).html(activity_dict.userprofile_username);

		//Construct the activity here.
		switch (activity){
			case "ACTIVITY_ACCOUNT_CREATED":
				$(li).append(userprofile_a);
				$(li).append(" has just joined EPM!");
				break;

			case "ACTIVITY_PETREPORT_SUBMITTED":
				$(li).append(userprofile_a);
				$(a).attr("href", "#");
				$(a).attr("link", URL_PRDP + activity_dict.petreport_id);
				$(a).on("click", function(){
					load_dialog({
						"link": $(this).attr("link"), 
						"title": activity_dict.petreport_name, 
						"width": SIZE_WIDTH_PRDP
					});
				});

				if (activity_dict.petreport_name != undefined){
					$(a).html(activity_dict.petreport_name);
					$(li).append(" submitted a Pet Report named ");
					$(li).append(a);
					$(li).append(".");
				} else {
					$(a).html("Pet Report");
					$(li).append(" submitted a ");
					$(li).append(a);
					$(li).append(" with no name.");
				}

				break;

			case "ACTIVITY_PETREPORT_ADD_BOOKMARK":
				$(li).append(userprofile_a);
				$(a).attr("href", "#");
				$(a).attr("link", URL_PRDP + activity_dict.petreport_id);
				$(a).on("click", function(){
					load_dialog({
						"link": $(this).attr("link"), 
						"title": activity_dict.petreport_name, 
						"width": SIZE_WIDTH_PRDP
					});
				});

				if (activity_dict.petreport_name != undefined){
					$(a).html(activity_dict.petreport_name);
					$(li).append(" bookmarked a Pet Report named ");
					$(li).append(a);
					$(li).append(".");
				} else {
					$(a).html("Pet Report");
					$(li).append(" bookmarked a ");
					$(li).append(a);
					$(li).append(" with no name.");
				}

				break;

			case "ACTIVITY_PETMATCH_PROPOSED": 
				$(a).attr("href", "#");
				$(a).attr("link", URL_PMDP + activity_dict.petmatch_id);
				$(a).html("Pet Match");
				$(a).on("click", function(){
					load_dialog({
						"link": $(this).attr("link"), 
						"title": activity_dict.lostpet_name + ":" + activity_dict.foundpet_name, 
						"width": SIZE_WIDTH_PMDP
					});
				});

				$(li).append(userprofile_a);			 				
				$(li).append(" proposed a ");
				$(li).append(a);
				$(li).append(" matching two " + activity_dict.petmatch_type + "s.");
				break;

			case "ACTIVITY_PETMATCH_PROPOSED_FOR_BOOKMARKED_PETREPORT":
				$(a).attr("href", "#");
				$(a).attr("link", URL_PMDP + activity_dict.petmatch_id);
				$(a).html("Pet Match");
				$(a).on("click", function(){
					load_dialog({
						"link": $(this).attr("link"), 
						"title": activity_dict.lostpet_name + ":" + activity_dict.foundpet_name, 
						"width": SIZE_WIDTH_PMDP
					});
				});

				var a2 = document.createElement("a");
				$(a2).attr("href", "#");
				$(a2).attr("link", URL_PRDP + activity_dict.petreport_id);
				$(a2).html("Pet Report");
				$(a2).on("click", function(){
					load_dialog({
						"link": $(this).attr("link"), 
						"title": activity_dict.petreport_name, 
						"width": SIZE_WIDTH_PRDP
					});
				});

				$(li).append(userprofile_a);
				$(li).append(" proposed a ");
				$(li).append(a);
				$(li).append(" for the ");
				$(li).append(a2);
				$(li).append(" that you bookmarked.");
				break;

			case "ACTIVITY_PETMATCH_VOTE":
				$(a).attr("href", "#");
				$(a).attr("link", URL_PMDP + activity_dict.petmatch_id)
				$(a).html("Pet Match");
				$(a).on("click", function(){
					load_dialog({
						"link": $(this).attr("link"), 
						"title": activity_dict.lostpet_name + ":" + activity_dict.foundpet_name, 
						"width": SIZE_WIDTH_PMDP
					});
				});

				$(li).append(userprofile_a);
				$(li).append(" voted on a ");
				$(li).append(a);
				$(li).append(" matching two " + activity_dict.petmatch_type + "s.");
				break;
			
			case "ACTIVITY_FOLLOWING":
				//Avoid activities where person A is now following A...
				if (activity_dict.userprofile2_id == activity_dict.userprofile_id)
					return null;

				//Also avoid Person B is now following A (you).
				if (current_userprofile_id == activity_dict.userprofile2_id)
					return null;

				$(a).attr("href", URL_USERPROFILE + activity_dict.userprofile2_id);
				$(a).html(activity_dict.userprofile2_username);
				$(li).append(userprofile_a);			 				
				$(li).append(" is now following ");
				$(li).append(a);
				$(li).append(".");
				break;

			case "ACTIVITY_FOLLOWER":
				if (activity_dict.userprofile2_id == activity_dict.userprofile_id)
					return null;

				/** If the current userprofiles matches the predicated userprofile...
					(i.e. we wouldn't like to know what we have already done.) **/
				if (current_userprofile_id == activity_dict.userprofile2_id)
					return null;

				$(a).attr("href", URL_USERPROFILE + activity_dict.userprofile2_id);
				$(a).html(activity_dict.userprofile2_username);

				//If the current userprofile matches the targetted userprofile...
				if (current_userprofile_id == activity_dict.userprofile_id){
					$(li).append(a);
					$(li).append(" is now following you!");
				} else {
					$(li).append(userprofile_a);			 					
					$(li).append(" is now being followed by ");
					$(li).append(a);
					$(li).append(".");
				}

				break;
		}//end switch

		return li;
}	

function fetch_bookmarks(page){
	//First, remove all tile elements
	$("#tiles li.item").remove();
	$("#tile_container span").remove();
	$.ajax({
	    type:"GET",
	    url:URL_GET_BOOKMARKS + "/" + page,
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
					$(img).attr("src", STATIC_URL + "images/icons/button_bookmark_X.png");
					$(img).addClass("bookmark_x");
					$(img).width(30);
					$(img).height(30);
					$(img).css("top", "-15px");
					$(img).css("left", "160px");

					$(img).hover(function mouseenter(){
						$(this).attr("src", STATIC_URL + "images/icons/button_bookmark_X_hover.png");
					}, function mouseleave(){
						$(img).attr("src", STATIC_URL + "images/icons/button_bookmark_X.png");
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
			$("#nav li.active").toggleClass("active");
			$("#nav_bookmarked").toggleClass("active");

			if (bookmarks.length == 0)
				$("#tile_container").prepend("<span style='margin:10px; display:block; font-size:24px; color:gray; text-align:center;'> No Pets Available Yet! </span>");
			else
				$("#tile_container").prepend("<span style='margin:10px; display:block; font-size:24px; color:gray; text-align:center;'> Select a Pet to Begin Matching.</span>");			
			
			//Don't forget to refresh the grid layout.
			refresh_layout();
		},
		error: function(data){
			alert("An unexpected error occurred when trying to get bookmarks. Please try again."); 
	    }	
  	});
}

function remove_bookmark(petreport_id, parent){
	/* display a confirmation dialog with options yes and no */
	$('<div></div>').appendTo('body').html('<div><h4>Are you sure you want to remove this bookmark?</h4></div>').dialog({ 	
		modal: true, 
		title: 'Confirm Bookmark Removal', 
		zIndex: 10000, 
		autoOpen: true,
		width: 'auto', 
		resizable: false,
		buttons: {
        	/*if the option is yes, an AJAX request will be sent to remove the bookmark*/
            Yes: function () {
                $(this).dialog("close");
                var user_id = USER_ID;
		        var csrf_value = $("input").attr("value");

				//ajax request to remove the bookmark
		        $.ajax({ 
		          type:"POST",
		          url: URL_BOOKMARK_PETREPORT,
		          data: {"csrfmiddlewaretoken":csrf_value, "petreport_id":petreport_id, "user_id": user_id, "action":"Remove Bookmark"},

		          success: function(data){
	            	//$("bookmarks_messages").html("<li class='success'>" + data.message + "</li>");
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
		        return true;
		    },

            No: function () {
            	$(this).dialog("close");
            }
    	},
        close: function (event, ui) {
            $(this).remove();
        }
	});
}

