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

    if (petreport == null || list == null)
        return null;

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
    list.append("<li class='pr_desc'>" + petreport.tag_info + "</li>");
    list.append("<li><b>Description:</b></li>");
    list.append("<li class='pr_desc'>" + petreport.description + "</li>");
}

function highlight_matches(list1, list2){
    //First, initialize and clear off pre-existing highlights.
    var items1 = $(list1).children("li");
    var items2 = $(list2).children("li");
    $(items1).each(function(){ $(this).css("color", "black"); });
    $(items2).each(function(){ $(this).css("color", "black"); });

    //Iterate through each field and check if the value matches in both lists.
    for (var i = 0; i < items1.length; i++){
        innerText1 = items1[i].innerText;
        innerText2 = items2[i].innerText;

        if (innerText1.match("Tag and Collar Information:") != null)
            continue;

        if (innerText1.match("Description:") != null)
            continue;

        if (innerText1 == "" || innerText2 == "")
            continue;

        if (innerText1 == innerText2){
            $(items1[i]).css("color", "blue");
            $(items2[i]).css("color", "blue");
        }
    }
}


