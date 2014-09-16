//URLS - use for redirect calls (consistent with constants file)
URL_HOME = '/'
URL_GET_ACTIVITIES = "/get_activities"
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


function launch_dialog(modal_element, url){
    $(modal_element).modal({
        "remote": url,
        "data": "dialog"
    });
    $(".modal-backdrop:not(:first)").remove();
}

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
    $(item).addClass("pet-item");
    $(alink).attr("identity", report.ID);    
    $(alink).on("click", function(){ launch_dialog(modal_element, URL_PRDP + report.ID); });

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
    $(item).addClass("pet-item");
    $(alink).on("click", function(){ launch_dialog(modal_element, URL_PMDP + match.ID); });

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


//This function takes a petreport fields list, its index, and the table in which the attributes will be written.
function set_PetReport_fields_to_table(petreport, index_offset, table){
    if(index_offset != 0 && index_offset != 1)
        return null

    var rows = $(table).find("tbody tr");
    $(rows).each(function(index, row){
        var pet_rows = $(row).find(".pet-info-data");
        field = petreport[index]
        pet_rows[index_offset].innerText = field[Object.keys(field)[0]] 
    })
}

function clear_PetReport_fields_to_table(index_offset, table){
    petreport = []
    for (var i = 0; i < 20; i++)
        petreport.push({"":""})
    set_PetReport_fields_to_table(petreport, index_offset, table)
}

function highlight_field_matches(table){
    //First, initialize and clear off pre-existing highlights.
    var rows = $(table).find("tbody tr")
    $(rows).each(function(index, row){
        var pet_rows = $(row).find(".pet-info-data")
        var first_pet_info = pet_rows[0]
        var second_pet_info = pet_rows[1]
        if (first_pet_info.innerText == second_pet_info.innerText){
            $(first_pet_info).css("color", "#428bca")
            $(second_pet_info).css("color", "#428bca")
        }
    });
}


