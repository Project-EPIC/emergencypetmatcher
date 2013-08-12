//This function allows us to prepare HTML elements and their activites upon load of the HTML page.
$(document).ready(function(){

	//Some variation of color for the feedlist.
	$('#feedlist li:nth-child(odd)').addClass('alternate');

	//Link to click to open to the PRDP
	$(".pmdp_dialog").click(function(){
		var link = $(this);
		return load_dialog(link.attr("href"), link.attr("name"), 850, "auto");
	});	

	//Link to click to open to the PRDP
	$("#feedlist .feedlist_prdp_dialog").click(function(){
		var link = $(this);
		//load_dialog(link, title, width, height)
		return load_dialog(link.attr("href"), link.attr("name"), 700, "auto");
	});	

	//Link to click to open to the PMDP
	$(".feedlist_pmdp_dialog").click(function(){
		var link = $(this);
		//load_dialog(link, title, width, height)      
		return load_dialog(link.attr("href"), "Pet Match Detailed Page", 850, "auto");
	});	

	$('#tiles').imagesLoaded(function() {
		//Lost Cause: Increase width of Activity Feed as an #item
		var feedlist_item = $(this).find("#feedlist").parent();
		
		//Call the AJAX GET request.
		index_fetch_activities(feedlist_item);

		//Prepare_layout
		refresh_layout();
	});

	//Update the share buttons on click.
	$("#facebook_share_epm").click(function(){ share_on_facebook(HOME_URL, HOME_IMAGE, HOME_TITLE, HOME_CAPTION, HOME_SUMMARY); });

	$("#twitter_share_epm").click(function(){ share_on_twitter(HOME_URL, HOME_IMAGE, HOME_TITLE, HOME_SUMMARY); });

}); //END document.ready()