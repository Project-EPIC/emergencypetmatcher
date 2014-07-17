//This function allows us to prepare a popup upon clicking several elements.
$(document).ready(function(){

	$("img.bookmark_x").click(function(){
		var img = $(this);
		remove_bookmark(img.attr('petreportid'),img.parent())
		//$(this).parent().remove();
			
	});

	$(".prdpdialog").click(function(){

		var link = $(this);
		var dialog_box = $("<div></div>").load(link.attr('url')).dialog ({

			autoOpen: true,
			position: "top",
			closeOnEscape: true,
			title:link.attr("name"),
			height: "auto",
			modal: true,
			width: 700,
			resizable: false,
			show: {effect:"fade", duration:500},
			close: function(event, ui){ 
				dialog_box.dialog("destroy").remove();
			}

		});
		return false;
	});

	$('#tiles').imagesLoaded(function() {
		//Prepare_layout
		refresh_layout();
	});

}); //END document.ready()

function remove_bookmark(petreport_id, parent){
	/* display a confirmation dialog with options yes and no */
	$('<div></div>').appendTo('body')
        .html('<div><h4>Are you sure you want to remove this bookmark?</h4></div>')
        .dialog({

            modal: true, title: 'Confirm Bookmark Removal', zIndex: 10000, autoOpen: true,
            width: 'auto', resizable: false,
            buttons: {
            	/*if the option is yes, an AJAX request will be sent to remove the bookmark*/
                Yes: function () {
                    
                    $(this).dialog("close");
                    var user_id = USER_ID;
			        /*an anonymous user shouldn't be able to acess the bookmarks page*/
			        if (user_id == "None"){
			        	return false;
				    }

			        csrf_value = $("input").attr("value");
			        /*ajax request to remove the bookmark*/
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
		              	alert("An unexpected error occurred when trying to bookmark this Pet Report. Please try again."); 
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

function refresh_layout(){

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
}