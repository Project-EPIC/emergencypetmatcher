//URLS - use for redirect calls (consistent with constants file)
URL_HOME = '/'
URL_GET_ACTIVITIES = "/get_activities_json"
URL_GET_PETMATCHES = "/get_PetMatches"
URL_GET_SUCCESSFUL_PETMATCHES = "/get_successful_PetMatches"
URL_GET_PETREPORT = "/get_PetReport/"
URL_GET_PETREPORTS = "/get_PetReports"
URL_GET_BOOKMARKS = "/get_bookmarks"
URL_LOGIN = '/login'
URL_TC = '/tc'
URL_TC_18 = '/tc_18'
URL_USERPROFILE = '/users/'
URL_EDITUSERPROFILE = "/users/edituserprofile"
URL_EDITUSERPROFILE_INFO = "/users/edituserprofile/update_User_info"
URL_EDITUSERPROFILE_PWD = "/users/edituserprofile/update_User_pwd"
URL_SEND_MESSAGE_TO_USERPROFILE = "/users/message_UserProfile"
URL_FOLLOW = "/users/follow"
URL_UNFOLLOW = "/users/unfollow"
URL_PRDP = '/reporting/PetReport/'
URL_SUBMIT_PETREPORT ='/reporting/submit_PetReport'
URL_GET_PET_BREEDS = "/reporting/get_pet_breeds/"
URL_BOOKMARK_PETREPORT = "/reporting/bookmark_PetReport"
URL_SHARE_PETREPORT = "/sharing/share_PetReport"
URL_PMDP = '/matching/PetMatch/'
URL_VOTE_MATCH = '/matching/vote_PetMatch'
URL_MATCHING = "/matching/match_PetReport/"
URL_PROPOSE_MATCH = "/matching/propose_PetMatch/"
URL_VERIFY_PETMATCH = "/matching/verify_PetMatch/"
URL_EMAIL_VERIFICATION_COMPLETE = "/email_verification_complete/" 
URL_REGISTRATION = "/accounts/register/"
URL_REGISTRATION_COMPLETE = "/register/complete/"
URL_ACTIVATION_COMPLETE = "/accounts/activate/complete/"

/******************************* Utility functions *******************************************/
$(document).ready(function(){

    $('#epm-modal').on('hidden.bs.modal', function () {
        $(this).find(".modal-content").html("");
    }); 

});


//GLOBAL JS Functions
function share_on_facebook(url, image, title, caption, summary) {
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
        if (response && response.post_id){
            alert('The callback function returned a response!');
        }
        else{
            alert("You clicked Cancel button!");
        }
    }
    FB.ui(obj, callback);
    return false;
}


function share_on_twitter(url, image, title, summary){
    title = escape(title);
    summary = escape(summary);
	window.open('http://twitter.com/share?url=' + url + '&text=' + title + ': ' + summary, 'newWindow', 'width=700, height=430');
}


function convert_to_javascript_obj(json_str){
    var obj = $.parseJSON(json_str.replace(/&quot;/ig, '"'));
    return obj;
 }

//Helper for setting up PetReport Tile.
function setup_petreport_item(report, modal_element){
    var item = document.createElement("li");
    var alink = document.createElement("a");
    var pet_img = document.createElement("img");

    //Link attributes.
    $(item).addClass("item");
    $(alink).attr("identity", report.ID);    
    $(alink).on("click", function(){
        $(modal_element).modal({
            "remote": URL_PRDP + report.ID
        });
    });

    //Pet Img attributes.
    $(pet_img).attr("src", MEDIA_URL + report.img_path);
    $(pet_img).width(150);
    $(pet_img).height(150);
    $(pet_img).css("margin", "0 auto");
    $(pet_img).css("display", "block");

    //Appends
    $(alink).append("<strong style='display:block; text-align:center;'>" + report.pet_name + "</strong>");
    $(alink).append("<span style='display:block; text-align:center;'>Contact: " + report.proposed_by_username + "</span>");                 
    $(alink).append(pet_img);
    $(item).append(alink);                  
    return item;
} 

//Helper for setting up PetMatch Tile.
function setup_petmatch_item (match, modal_element){
    var item = document.createElement("li");
    var alink = document.createElement("a");
    var lost_pet_img = document.createElement("img");
    var found_pet_img = document.createElement("img");

    //Deal with Attributes.
    $(item).addClass("item");
    $(alink).on("click", function(){
        $(modal_element).modal({
            "remote": URL_PMDP + match.ID
        });        
    });

    $(lost_pet_img).attr("src", MEDIA_URL + match.lost_pet_img_path);
    $(found_pet_img).attr("src", MEDIA_URL + match.found_pet_img_path);
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


function display_PetReport_fields(options){
    var petreport = options ["petreport"] || null;
    var list = options ["list"] || null;
    var showContactInfo = false;

    //If PetReport is not available, exit.
    if (petreport == null || list == null)
        return null;

    //Is there contact information to show? Need to check.
    if (petreport.contact_name != null || petreport.contact_email != null || petreport.contact_number != null || petreport.contact_link != null)
        showContactInfo = true;

    list.html("");
    list.append("<li><b>Pet Name:</b> " + petreport.pet_name + "</li>");
    list.append("<li><b>Pet Type:</b> " + petreport.pet_type + "</li>");
    list.append("<li><b>Lost/Found:</b> " + petreport.status + "</li>");
    list.append("<li><b>Contact:</b> <a href= '" + URL_USERPROFILE + petreport.proposed_by + "/' >" + petreport.proposed_by_username + "</a></li>");
    list.append("<li><b>Date " + petreport.status + ":</b> " + petreport.date_lost_or_found + "</li>");
    list.append("<li><b>Location:</b> " + petreport.location + "</li>");

    //Treat the microchip ID specially.
    if (petreport.microchip_id != "")
        list.append("<li><b>Microchipped: </b>Yes</li>");
    else
        list.append("<li><b>Microchipped: </b>No</li>");

    list.append("<li><b>Spayed/Neutered:</b> " + petreport.spayed_or_neutered + "</li>");
    list.append("<li><b>Age:</b> " + petreport.age + "</li>");
    list.append("<li><b>Sex:</b> " + petreport.sex + "</li>");
    list.append("<li><b>Breed:</b> " + petreport.breed + "</li>");
    list.append("<li><b>Color:</b> " + petreport.color + "</li>");
    list.append("<li><b>Size:</b> " + petreport.size + "</li>");
    list.append("<li><b>Tag and Collar Information:</b></li>");
    list.append("<li>" + petreport.tag_info + "</li>");
    list.append("<li><b>Description:</b></li>");
    list.append("<li>" + petreport.description + "</li>");

    //Show Contact information.
    if (showContactInfo == true){
        list.append("<hr size='0' width='100%' color='white'/>")
        list.append("<li><b>Contact Information</b></li>");
        list.append("<li style='margin:10px;'><b>Name:</b> " + (petreport.contact_name || "") + "</li>");
        list.append("<li style='margin:10px;'><b>Email:</b> " + (petreport.contact_email || "") + "</li>");
        list.append("<li style='margin:10px;'><b>Phone Number:</b> " + (petreport.contact_number || "") + "</li>");

        //Alternative Link should not be shown if it doesn't exist.
        if (petreport.contact_link)
            list.append("<li style='margin:10px;'><a href='" + petreport.contact_link +  "'> Alternative Link for this Pet </a></li>");
    }    
}

function highlight_matches(list1, list2){
    //First, initialize and clear off pre-existing highlights.
    var items = null;
    var items1 = $(list1).children("li");
    var items2 = $(list2).children("li");
    $(items1).each(function(){ $(this).css("color", "black"); });
    $(items2).each(function(){ $(this).css("color", "black"); });

    if (items1.length < items2.length)
        items = items1;
    else
        items = items2;

    //Iterate through each field and check if the value matches in both lists.
    for (var i = 0; i < items.length; i++){
        var innerText1 = items1[i].innerText;
        var innerText2 = items2[i].innerText;

        if (innerText1.match("Tag and Collar Information") != null)
            continue;

        if (innerText1.match("Description") != null)
            continue;

        if (innerText1 == "" || innerText2 == "")
            continue;

        if (innerText1.match("Contact Information") != null)
            continue;

        if (innerText1 == innerText2){
            $(items1[i]).css("color", "blue");
            $(items2[i]).css("color", "blue");
        }
    }
}


