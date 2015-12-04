//URLS - use for redirect calls (consistent with constants file)
HOME_URLS = {
    "HOME":                 "/",
    "LOGIN":                "/login",
    "ACTIVITIES_DATA":      "/get_activities",
    "BOOKMARKS_DATA":       "/get_bookmarks",
}

SOCIALIZING_URLS = {
    "USERPROFILE":          "/users/",
    "USERPROFILES_JSON":    "/users/get_UserProfiles_JSON",
}

REPORTING_URLS = {
    "PETREPORT_JSON":       "/reporting/get_PetReport_JSON",
    "PETREPORTS_JSON":      "/reporting/get_PetReports_JSON",
    "PETREPORT":            "/reporting/",
    "PET_BREEDS":           "/reporting/get_pet_breeds",
    "BOOKMARK":             "/reporting/bookmark/",
    "EVENT_TAGS":           "/reporting/get_event_tags",
}

MATCHING_URLS = {
    "PETMATCH_JSON":        "/matching/get_PetMatch_JSON",
    "PETMATCHES_JSON":      "/matching/get_PetMatches_JSON",
    "PETMATCH":             "/matching/",
    "CANDIDATE_PETREPORTS": "/matching/get_candidate_PetReports_JSON",
    "MATCH":                "/matching/new/",
    "PROPOSE":              "/matching/propose/",
    "VOTE":                 "/matching/vote/",
}

VERIFYING_URLS = {
    "PETREUNIONS_JSON":     "/verifying/get_PetReunions_JSON",
    "PETREUNION":           "/verifying/"
}

//Twitter Asynchronous loading for Sharing.
window.twttr = (function(d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0],
    t = window.twttr || {};
  if (d.getElementById(id)) return t;
  js = d.createElement(s);
  js.id = id;
  js.src = "https://platform.twitter.com/widgets.js";
  fjs.parentNode.insertBefore(js, fjs);

  t._e = [];
  t.ready = function(f) {
    t._e.push(f);
  };
  return t;
}(document, "script", "twitter-wjs"));

//Facebook asynchronous loading for sharing.
(function(d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) return;
  js = d.createElement(s); js.id = id;
  js.src = "//connect.facebook.net/en_US/sdk.js#xfbml=1&version=v2.5&appId=315409715220911";
  fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));


/******************************* Utility functions *******************************************/

$(document).ready(function(){
    flash_message();

    //Reunion Labels
    $(".label-Reunited").addClass("label-success");
    $(".label-Rehomed").addClass("label-primary");
    $(".label-RIP").addClass("label-default");
    $(".label-Closed").addClass("label-default");
    $(".label-Lost").addClass("label-danger");
    $(".label-Found").addClass("label-warning");

});

function recaptcha_done(){
    $('#id_submit').removeAttr('disabled');
}

function flash_message(){
    $(".epm-alert").removeClass("hidden").delay(3500).fadeOut();
}

function add_flash_message(status, message){
    msg = document.createElement("div");
    $(msg).html(message);
    $(msg).addClass("alert epm-alert hidden");
    switch(status){
        case "success":
        $(msg).addClass("alert-success");
        break;
        case "danger":
        $(msg).addClass("alert-danger");
        break;
        default:
        $(msg).addClass("alert-info");
        break;
    }
    $("#messages").append(msg);
    flash_message()
}

//Helper for setting up PetReport Tile.
function setup_petreport_item(report){
    var item = document.createElement("li");
    var alink = document.createElement("a");
    var pet_img = document.createElement("img");
    var ribbon = document.createElement("span");
    var title = document.createElement("div");

    //Link attributes.
    $(item).addClass("pet-item");
    $(alink).attr("identity", report.ID);
    $(alink).attr("href", (REPORTING_URLS["PETREPORT"] + report.ID));

    //Pet Img attributes.
    $(pet_img).attr("src", MEDIA_URL + report.img_path);
    $(pet_img).width(150);
    $(pet_img).height(150);
    $(pet_img).css("margin", "0 auto");
    $(pet_img).css("display", "block");

    //Ribbon Attributes.
    $(title).css("text-align", "center");
    $(ribbon).addClass("label");

    if (report.status == "Lost"){
        $(ribbon).html("Lost");
        $(ribbon).addClass("label-danger");
    }
    else{
        $(ribbon).html("Found")
        $(ribbon).addClass("label-warning");
    }

    //Appends
    $(title).append("<b>" + report.pet_name + "</b>");
    $(title).append(ribbon);
    $(alink).append(title);
    $(alink).append("<span style='display:block; text-align:center;'>Contact: " + report.proposed_by_username + "</span>");
    $(alink).append(pet_img);
    $(item).append(alink);
    return item;
}

//Helper for setting up PetReunion Tile.
function setup_petreunion_item(reunion){
    var item = document.createElement("li");
    var alink = document.createElement("a");
    var pet_img = document.createElement("img");
    var ribbon = document.createElement("span");
    var title = document.createElement("div");

    //Link attributes.
    $(item).addClass("pet-item");
    $(alink).attr("identity", reunion.ID);
    $(alink).attr("href", (VERIFYING_URLS["PETREUNION"] + reunion.ID));

    //Pet Img attributes.
    $(pet_img).attr("src", MEDIA_URL + reunion.img_path);
    $(pet_img).width(150);
    $(pet_img).height(150);
    $(pet_img).css("margin", "0 auto");
    $(pet_img).css("display", "block");

    //Ribbon Attributes.
    $(title).css("text-align", "center");
    $(title).css("margin-bottom", "5px");
    switch(reunion.reason){
        case "Reunited":
        $(ribbon).addClass("label label-success");
        break;
        case "Rehomed":
        $(ribbon).addClass("label label-primary");
        break;
        case "RIP":
        $(ribbon).addClass("label label-default");
        break;
        case "Closed":
        $(ribbon).addClass("label label-default");
        break;
    }

    $(ribbon).html(reunion.reason);

    //Appends
    $(title).append("<b>" + reunion.pet_name + "</b>");
    $(title).append(ribbon);
    $(alink).append(title);
    $(alink).append("<span style='display:block; text-align:center;'>Contact: " + reunion.proposed_by_username + "</span>");
    $(alink).append(pet_img);
    $(item).append(alink);
    return item;
}

//Helper for setting up PetMatch Tile.
function setup_petmatch_item (match){
    var item = document.createElement("li");
    var alink = document.createElement("a");
    var lost_pet_img = document.createElement("img");
    var found_pet_img = document.createElement("img");

    //Deal with Attributes.
    $(item).addClass("pet-item");
    $(alink).attr("href", MATCHING_URLS["PETMATCH"] + match.ID);

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
    $(alink).append("<b style='display:block; text-align:center;'>" + match.lost_pet_name + " with " + match.found_pet_name + "</b>");
    $(alink).append("<span style='display:block; text-align:center;'>Contact: " + match.proposed_by_username + "</span>");
    $(alink).append(lost_pet_img);
    $(alink).append(found_pet_img);
    $(item).append(alink);
    return item;
}

//Helper for setting up Activity Item Tile.
function setup_activity_item (activity){
    var activity_type       = activity.activity;
    var source_id           = null;
    var source_thumb_path   = null;
    var text                = activity.text;
    var text_slices         = text.split(" ");
    var username            = text_slices[0];

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
    var petmatch_options = {
        "item": item,
        "text": text,
        "source_id": source_id,
        "source_img_div": source_img_div,
        "text_element": text_element
    };

    //Now create the activity.
    switch(activity_type){
        case "ACTIVITY_ACCOUNT_CREATED":
        case "ACTIVITY_USER_SET_PHOTO":
        case "ACTIVITY_USER_CHANGED_USERNAME":
        text = text_slices.slice(1).join(" ");
        $(text_element).append(" ");
        $(text_element).append(text);
        $(item).append(text_element);
        break;

        case "ACTIVITY_SOCIAL_FOLLOW":
        followed_username = text_slices[4];
        text = text_slices.slice(1, 4).join(" ");
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
        pet_name = text_slices[6];
        text = text_slices.slice(1, 6).join(" ");
        pet_link = document.createElement("a");
        $(pet_link).attr("href", REPORTING_URLS["PETREPORT"] + source_id);
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

        case "ACTIVITY_PETMATCHCHECK_VERIFY":
        petmatch_options["source_id"] = activity.source.petmatch.id
        petmatch_options["name_offset"] = 6;
        setup_petmatch_activity_item(petmatch_options);
        break;

        case "ACTIVITY_PETMATCHCHECK_VERIFY_SUCCESS":
        petmatch_options["source_id"] = activity.source.petmatch.id
        petmatch_options["name_offset"] = 6
        setup_petmatch_activity_item(petmatch_options);
        break;

        case "ACTIVITY_PETMATCHCHECK_VERIFY_SUCCESS_OWNER":
        petmatch_options["source_id"] = activity.source.petmatch.id
        petmatch_options["name_offset"] = 6
        setup_petmatch_activity_item(petmatch_options);
        break;

        case "ACTIVITY_PETMATCHCHECK_VERIFY_FAIL":
        petmatch_options["source_id"] = activity.source.petmatch.id
        petmatch_options["name_offset"] = 7
        setup_petmatch_activity_item(petmatch_options);
        break;

        case "ACTIVITY_PETREUNION_CREATED":
        petreunion = text_slices.slice(2, 6).join(" ");
        pet_name = text_slices[7];
        pet_reunion_link = document.createElement("a");
        pet_link = document.createElement("a");
        $(pet_reunion_link).attr("href", VERIFYING_URLS["PETREUNION"] + source_id);
        $(pet_reunion_link).html(petreunion);
        $(pet_link).attr("href", REPORTING_URLS["PETREPORT"] + activity.source.petreport_id);
        $(pet_link).html(pet_name);
        $(text_element).append(" " + text_slices[1] + " ");
        $(text_element).append(pet_reunion_link);
        $(text_element).append(" " + text_slices[6] + " ");
        $(text_element).append(pet_link);
        $(item).append(text_element);
        $(item).append(source_img_div);
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

    $(petmatch_link).attr("href", MATCHING_URLS["PETMATCH"] + options["source_id"]);
    $(petmatch_link).html(petmatch_name);
    $(text_element).append(" ");
    $(text_element).append(text);
    $(text_element).append(" ");
    $(text_element).append(petmatch_link);
    $(item).append(text_element);
    $(item).append(source_img_div);
}

//This function takes a petreport object, its index, and the table in which the attributes will be written.
function set_PetReport_fields_to_table(petreport, index_offset, table){
    if (index_offset != 0 && index_offset != 1)
        return null;

    var rows = $(table).find("tbody tr");
    $(rows).each(function(index, row){
        var header = $(row).find(".pet-info-header");
        field = petreport[header.attr("attr")];
        col = $(row).find(".pet-info-data")[index_offset];
        col.innerHTML = field;
    });
}

function clear_PetReport_fields_to_table(index_offset, table){
    $(table).find("tbody tr").each(function(index, row){
        pet_row = $(row).find(".pet-info-data")[index_offset];
        pet_row.innerHTML = "";
    });
}

function highlight_field_matches(table){
    //First, initialize and clear off pre-existing highlights.
    var rows = $(table).find("tbody tr")
    $(rows).each(function(index, row){
        var pet_rows = $(row).find(".pet-info-data")
        if (pet_rows [0] == undefined || pet_rows [1] == undefined)
            return true;

        var first_pet_info = pet_rows [0];
        var second_pet_info = pet_rows [1];
        if (first_pet_info.innerHTML.trim() == second_pet_info.innerHTML.trim()){
            $(first_pet_info).css("color", "deepskyblue")
            $(second_pet_info).css("color", "deepskyblue")
        }
        else {
            $(first_pet_info).css("color", "black")
            $(second_pet_info).css("color", "black")
        }
    });
}

function perform_AJAX_call(options){
    if (options["error"] == undefined || options["error"] == null)
        options["error"] = function(data){ add_flash_message("danger", "Oops! Something went wrong. Please try again!");}

    $.ajax({
        type:options["type"],
        url:options["url"],
        data:options["data"],
        success: options["success"],
        error: options["error"]
    });
}

function load_pet_breeds (pet_type, callback){
    perform_AJAX_call ({
        type:"GET",
        url: REPORTING_URLS["PET_BREEDS"],
        data: {"pet_type": pet_type},
        success: function(data){ callback(data);},
        error: function (data){ return [];}
    });
}
