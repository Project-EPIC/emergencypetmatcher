//This function allows us to prepare HTML elements and their activites upon load of the HTML page.
$(document).ready(function(){

	//Some variation of color for the feedlist.
	$('#feedlist li:nth-child(odd)').addClass('alternate');

	//Link to click to open to the PRDP
	$(".prdp_dialog").click(function(){

		var link = $(this);
		//load_dialog(link, title, width, height)
		return load_dialog(link.attr("href"), link.attr("name"), 700, "auto");
	});

	//Link to click to open to the PMDP
	$("#pmdp_dialog").click(function(){

		alert("HEY");
		var link = $(this);
		//load_dialog(link, title, width, height)      
		return load_dialog(link.attr("href"), "Pet Match Detailed Page", 850, "auto");
	});	

	$('#tiles').imagesLoaded(function() {

		//Lost Cause: Increase width of Activity Feed as an #item
		var feedlist_item = $(this).find("#feedlist").parent();
		
		//Call the AJAX GET request.
		index_fetch_activities(feedlist_item);
	});

}); //END document.ready()


//Function to fetch the local activities using AJAX GET
function index_fetch_activities (feedlist_item){

	var feedlist = feedlist_item.find("#feedlist");

	$.ajax ({

		type:"GET",
		url: URL_GET_ACTIVITIES_JSON,
		success: function(data){

			 var activities = data.activities;

			 //Iterate through the activities and append them to the list.
			 for (var i = 0; i < activities.length; i++){

			 	var activity = activities [i];
			 	if (activity == "")
			 		continue;
			 	//Now add it to the list.
			 	if (activity.indexOf("you") > 0)
			 		feedlist.append("<li style=background:#FFFEB3; margin-left:2px; padding-left:0px;>" + activities[i] + "</li>");
			 	else if (activity.indexOf("Bookmark") >= 0)
			 		feedlist.append("<li style=background:#CCE6FF; margin-left:2px; padding-left:0px;>" + activities[i] + "</li>");
			 	else
			 		feedlist.append("<li style=margin-left:2px; padding-left:0px;>" + activities[i] + "</li>");
			}

			// Prepare layout options.
			var options = {
				autoResize: true, // This will auto-update the layout when the browser window is resized.
				container: $('#tiles'), // Optional, used for some extra CSS styling
				offset: 2, // Optional, the distance between grid items
				itemWidth: 210 // Optional, the width of a grid item
			};

			// Now we're ready to call some wookmarking: get reference to your grid items.
			var handler = $('#tiles li.item');

			// Call the layout function.
			handler.wookmark(options);								 
		
		},
		error: function(data){
			alert("An unexpected error occurred when trying to retrieve the activities. Please try again."); 
			return false;
		}						
	});


}

