//GLOBAL Variables
URL_HOME = '/'
URL_GET_ACTIVITIES_JSON = "/get_activities_json"
URL_LOGIN = '/login'
URL_SUBMIT_PETREPORT ='/reporting/submit_PetReport'
URL_USERPROFILE = '/UserProfile/'
URL_PRDP = '/reporting/PetReport/'
URL_PMDP = '/matching/PetMatch/'
URL_VOTE_MATCH = '/matching/vote_PetMatch'
URL_MATCHING = "/matching/match_PetReport/"
URL_PROPOSE_MATCH = "/matching/propose_PetMatch/"
URL_BOOKMARK_PETREPORT = "/reporting/bookmark_PetReport/"
URL_SHARE_PETREPORT = "/sharing/share_PetReport"

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

function write_callback_data(str) {
    document.getElementById('fb-ui-return-data').innerHTML=str;
}

function publishToFeed(url, image, title, caption, summary) {
 
        var obj = {
            method: 'feed',
            redirect_uri: url,
            link: url,
            picture: image,
            name: title,
            caption: caption,
            description: summary           
        };
 
        function callback(response) {
            //alert('callback');
            if (response && response.post_id){
                document.getElementById('fb-ui-return-data').innerHTML = "Post ID: " + response.post_id;
                //write_callback_data("<br><b>Callback returns succeeded!</b>");
                alert('response');
            }
            else{
                alert("You clicked Cancel button, don't you want to share?");
            }
        }
        FB.ui(obj, callback);
        return false;
}


function share_on_twitter(url, image, title, summary){
	window.open('http://twitter.com/share?url=' + url + '&text=' + title + ': ' + summary, 'newWindow', 'width=700, height=430');
}


function convert_to_javascript_obj(json_str){
    return JSON.parse(json_str.replace(/&quot;/ig, '"'));
 }

function display_PetReport_fields(petreport, prdplist){

    // Assert that prdplist is an <ul> html tag element
    
    prdplist.html("");
    prdplist.append("<li><b>Pet Name:</b> " + petreport.pet_name + "</li>");
    prdplist.append("<li><b>Pet Type:</b> " + petreport.pet_type + "</li>");
    prdplist.append("<li><b>Lost/Found:</b> " + petreport.status + "</li>");
    prdplist.append("<li><b>Contact:</b> <a href= '" + URL_USERPROFILE + petreport.proposed_by + "/' >" + petreport.proposed_by_username + "</a></li>");
    prdplist.append("<li><b>Date " + petreport.status + ":</b> " + petreport.date_lost_or_found + "</li>");
    prdplist.append("<li style='word-wrap:break-word;'><b>Location:</b> " + petreport.location + "</li>");

    //Treat the microchip ID specially.
    if (petreport.microchip_id != "")
        prdplist.append("<li><b>Microchipped: </b>Yes</li>");
    else
        prdplist.append("<li><b>Microchipped: </b>No</li>");

    prdplist.append("<li><b>Spayed/Neutered:</b> " + petreport.spayed_or_neutered + "</li>");
    prdplist.append("<li><b>Age:</b> " + petreport.age + "</li>");
    prdplist.append("<li><b>Sex:</b> " + petreport.sex + "</li>");
    prdplist.append("<li><b>Breed:</b> " + petreport.breed + "</li>");
    prdplist.append("<li><b>Color:</b> " + petreport.color + "</li>");
    prdplist.append("<li><b>Size:</b> " + petreport.size + "</li>");
    prdplist.append("<li style='overflow:scroll;'><b>Description:</b> " + petreport.description + "</li>");

}




