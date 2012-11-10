//GLOBAL Variables
URL_HOME = '/'
URL_GET_ACTIVITIES_JSON = "/get_activities_json"
URL_LOGIN = '/login'
URL_SUBMIT_PETREPORT ='/reporting/submit_PetReport'
URL_USERPROFILE = '/UserProfile/'
URL_PRDP = '/reporting/PetReport/'
URL_PETREPORT_JSON = "/reporting/get_PetReport_json/"
URL_PMDP = '/matching/PetMatch/'
URL_VOTE_MATCH = '/matching/vote_PetMatch'
URL_MATCHING = "/matching/match_PetReport/"
URL_PROPOSE_MATCH = "/matching/propose_PetMatch/"
URL_BOOKMARK_PETREPORT = "/reporting/bookmark_PetReport/"



//GLOBAL JS Functions
function load_dialog(link, title, width, height){

	//Take care of the options first.
	var options = {

		autoOpen: true,
		position: "top",
		closeOnEscape: true,
		title: title,
		width: width,
		height: height,
		modal: true,
		resizable: false,
		show: {effect:"fade", duration:500},
		close: function (event, ui){
			dialog_box.dialog("destroy").remove();
		}
	};

	//Launch the dialog.
	var dialog_box = $("<div></div>").load(link).dialog(options);
	return false;

}

function get_PetReport_json (petreport_id){

	$.ajax({

		type:"GET",
		url:"/reporting/get_PetReport_json/" + petreport_id + "/",
		success: function(data){
			var petreport = data;
			return petreport;
		},
		error: function(data){
			alert("An unexpected error occurred when trying to retrieve this Pet Report's attributes. Please try again."); 
			return false;
		}
	});
}

/*function that sends out a synchronous post request by creating an invisible form*/

function postIt(url, data){

    $('body').append($('<form/>', {
      id: 'jQueryPostItForm',
      method: 'POST',
      action: url
    }));

    for(var i in data){
      $('#jQueryPostItForm').append($('<input/>', {
        type: 'hidden',
        name: i,
        value: data[i]
      }));
    }

    $('#jQueryPostItForm').submit();
}

function share_on_facebook(url, image, title, summary){
	window.open('http://www.facebook.com/sharer.php?s=100&p[url]=' + url + '&p[images][0]=' + image + '&p[title]=' + title + '&p[summary]=' + summary,'newWindow', 'width=700, height=430');
	return false;
}	

function share_on_twitter(url, image, title, summary){
	window.open('http://twitter.com/share?url=' + url + '&text=' + title + ': ' + summary, 'newWindow', 'width=700, height=430');
}

