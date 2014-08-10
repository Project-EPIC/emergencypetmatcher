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
URL_USERPROFILE = '/UserProfile/'
URL_EDITUSERPROFILE = "/UserProfile/edituserprofile"
URL_EDITUSERPROFILE_INFO = "/UserProfile/edituserprofile/update_User_info"
URL_EDITUSERPROFILE_PWD = "/UserProfile/edituserprofile/update_User_pwd"
URL_SEND_MESSAGE_TO_USERPROFILE = "/UserProfile/message_UserProfile"
URL_FOLLOW = "/UserProfile/follow"
URL_UNFOLLOW = "/UserProfile/unfollow"
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

//Constants
SIZE_WIDTH_PRDP = 690
SIZE_WIDTH_PMDP = 770

/******************************* Utility functions *******************************************/

//GLOBAL JS Functions
function load_dialog(options){

    link = options ["link"] || null;
    title = options ["title"] || "";
    width = options ["width"] || "auto";
    height = options ["height"] || "auto";

    if (link == null)
        return null;

    //Take care of the options first.
    var dialog_options = {
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
    var dialog_box = $("<div></div>").load(link).dialog(dialog_options);
}

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

function highlight_field_matches(table){
    //First, initialize and clear off pre-existing highlights.
    var rows = $(table).find("tbody tr")
    $(rows).each(function(row){
        var pet_rows = $(row).find(".pet-info")
        first_pet_info = pet_rows[0]
        second_pet_info = pet_rows[1]
        if (first_pet_info.text.match(second_pet_info.text != null)
            $(first_pet_info).css("color", "blue")
            $(second_pet_info).css("color", "blue")

    });
}


