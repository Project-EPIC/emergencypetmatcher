//URLS - use for redirect calls (consistent with constants file)
HOME_URLS = {
    "HOME":                 "/",
    "LOGIN":                "/login",
    "ACTIVITIES_DATA":      "/get_activities/",
    "PETMATCHES_DATA":      "/get_PetMatches/",
    "PETREPORT_DATA":       "/get_PetReport/",
    "PETREPORTS_DATA":      "/get_PetReports/",
    "BOOKMARKS_DATA":       "/get_bookmarks/",    
}

SOCIALIZING_URLS = {
    "USERPROFILE":          "/users/",
}

REPORTING_URLS = {
    "PETREPORT":            "/reporting/",
    "PET_BREEDS":           "/reporting/get_pet_breeds/",
    "BOOKMARK":             "/reporting/bookmark/",
}

MATCHING_URLS = {
    "PETMATCH":             "/matching/",
    "CANDIDATE_PETREPORTS": "/matching/get_candidate_PetReports",
    "MATCH":                "/matching/new/",
    "PROPOSE":              "/matching/propose/",
    "VOTE":                 "/matching/vote/",
}

/******************************* Utility functions *******************************************/
$(document).ready(function(){
    $('#epm-modal').on('hidden.bs.modal', function () { $(this).find(".modal-content").html(""); }); 
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
    $(alink).on("click", function(){ launch_dialog(modal_element, REPORTING_URLS["PETREPORT"] + report.ID); });

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
    $(alink).on("click", function(){ launch_dialog(modal_element, MATCHING_URLS["PETMATCH"] + match.ID); });

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

//Helper for setting up Activity Item Tile.
function setup_activity_item (activity, modal_element){
    //Deal with Activity Attributes and Elements.
    var activity_type       = activity.activity;
    var source_id           = null;
    var source_thumb_path   = null;
    var text                = activity.text;
    var username            = text.split(" ")[0];

    if (activity.source != null){
        source_id           = activity.source.id
        source_thumb_path   = activity.source.thumb_path;
    }

    var item            = document.createElement("li");
    var profile_link    = document.createElement("a");
    var profile_img     = document.createElement("img");
    var source_img_div  = document.createElement("div");
    var date            = document.createElement("div");
    var text_element    = document.createElement("p");

    $(item).addClass("activity-item");  
    $(profile_link).attr("href", SOCIALIZING_URLS["USERPROFILE"] + activity.profile.id).html(activity.profile.username);
    $(profile_img).attr("src", MEDIA_URL + activity.profile.thumb_path);
    $(date).addClass("date").html(activity.date_posted);
    $(item).append(profile_img);
    $(text_element).append(profile_link);    

    //Grab image paths and organize them.
    if (source_thumb_path != null){
        $(source_img_div).addClass("source");
        if(typeof(source_thumb_path) != "object")
            source_thumb_path = [source_thumb_path];

        for (var i = 0; i < source_thumb_path.length; i++){
            source_img = document.createElement("img");    
            $(source_img).attr("src", MEDIA_URL + source_thumb_path[i]);
            $(source_img_div).append(source_img);
        }
    }

    //Use this for PetMatch activity item preparation.
    var petmatch_options = {    "item": item,
                                "text": text,
                                "source_id": source_id,
                                "source_img_div": source_img_div,
                                "text_element": text_element,
                                "modal": modal_element };    

    //Now create the activity.
    switch(activity_type){
        case "ACTIVITY_ACCOUNT_CREATED":
        case "ACTIVITY_USER_SET_PHOTO":
        case "ACTIVITY_USER_CHANGED_USERNAME":
        text = text.split(" ").slice(1).join(" ");
        $(text_element).append(" ");
        $(text_element).append(text);
        $(item).append(text_element);
        break;        

        case "ACTIVITY_SOCIAL_FOLLOW":
        followed_username = text.split(" ")[4];
        text = text.split(" ").slice(1, 4).join(" ");
        follow_link = document.createElement("a");
        $(follow_link).attr("href", SOCIALIZING_URLS["USERPROFILE"] + source_id);
        $(follow_link).html(followed_username);        
        $(text_element).append(" ");
        $(text_element).append(text);
        $(text_element).append(" ");
        $(text_element).append(follow_link);
        $(item).append(text_element);
        $(item).append(source_img_div);
        break;

        case "ACTIVITY_PETREPORT_SUBMITTED":
        pet_name = text.split(" ")[6];
        text = text.split(" ").slice(1, 6).join(" ");
        pet_link = document.createElement("a");
        $(pet_link).attr("href", "#");
        $(pet_link).on("click", function(){ launch_dialog(modal_element, REPORTING_URLS["PETREPORT"] + source_id); });
        $(pet_link).html(pet_name);
        $(text_element).append(" ");
        $(text_element).append(text);
        $(text_element).append(" ");
        $(text_element).append(pet_link);
        $(item).append(text_element);
        $(item).append(source_img_div);
        break;

        case "ACTIVITY_PETMATCH_PROPOSED":
        petmatch_options["name_offset"] = 3;
        setup_petmatch_activity_item(petmatch_options);
        break;

        case "ACTIVITY_PETMATCH_UPVOTE":
        case "ACTIVITY_PETMATCH_DOWNVOTE":
        petmatch_options["name_offset"] = 4;
        setup_petmatch_activity_item(petmatch_options);
        break;

        case "ACTIVITY_PETCHECK_VERIFY":
        petmatch_options["source_id"] = activity.source.petmatch.id
        petmatch_options["name_offset"] = 6;
        setup_petmatch_activity_item(petmatch_options);
        break;

        case "ACTIVITY_PETCHECK_VERIFY_SUCCESS":
        petmatch_options["source_id"] = activity.source.petmatch.id
        petmatch_options["name_offset"] = 6
        setup_petmatch_activity_item(petmatch_options);
        break;

        case "ACTIVITY_PETCHECK_VERIFY_SUCCESS_OWNER":
        petmatch_options["source_id"] = activity.source.petmatch.id
        petmatch_options["name_offset"] = 6
        setup_petmatch_activity_item(petmatch_options);
        break;        

        case "ACTIVITY_PETCHECK_VERIFY_FAIL":
        petmatch_options["source_id"] = activity.source.petmatch.id
        petmatch_options["name_offset"] = 7
        setup_petmatch_activity_item(petmatch_options);
        break;

        default: 
        $(text_element).html(text);
        $(item).append(text_element);
    }
    $(item).append(date);
    return item;
}

function setup_petmatch_activity_item(options){
    item            = options["item"];
    text            = options["text"];
    source_id       = options["activity"];
    source_img_div  = options["source_img_div"];
    text_element    = options["text_element"];
    petmatch_name   = text.split(" ").slice(options["name_offset"]).join(" ");
    text            = text.split(" ").slice(1, options["name_offset"]).join(" ");
    petmatch_link   = document.createElement("a");

    $(petmatch_link).attr("href", "#");
    $(petmatch_link).on("click", function(){ launch_dialog(options["modal"], MATCHING_URLS["PETMATCH"] + options["source_id"]); });
    $(petmatch_link).html(petmatch_name);
    $(text_element).append(" ");
    $(text_element).append(text);
    $(text_element).append(" ");
    $(text_element).append(petmatch_link);
    $(item).append(text_element);
    $(item).append(source_img_div);
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
        else {
            $(first_pet_info).css("color", "black")
            $(second_pet_info).css("color", "black")            
        }
    });
}


