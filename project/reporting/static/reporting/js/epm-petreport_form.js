$(document).ready(function(){

	$("#epm-nav-links .nav-link-pet").toggleClass("active");
	//Image Size.
	var img_size = 0.0;
	var img_rotation = 0;

	//Initialize with today's date
	var today = new Date();
	var curYear = new Date().getUTCFullYear();
	$("#id_date_lost_or_found").datepicker({
		format: "mm/dd/yyyy",
		changeMonth: true, 
		showOn:"focus",
		changeYear: true, 
		yearRange: '1900:curYear',
		startDate:"01/01/1950",
		endDate:"0d"
	});

	$("#id_date_lost_or_found").attr("value", today.getMonth()+1 + '/' + today.getDate() + '/' + today.getFullYear());

	//If an input image comes through, preview it!
	$("#id_img_path").change(function(){
		if (this.files && this.files[0]) {

			img_size = this.files[0].size/1000/1000; //Image size in MB.
			if (img_size > 3.0) {
				alert("Image size exceeds 3MB, please upload an image that is within 3MB.");
				$('#id_img_path').val("");
				$("#preview_img").html("");
				this.focus();
			}
			else {
				var reader = new FileReader();
				reader.onload = function (e) {
					//Create an image element, tack on the source, fit it into the container for preview, 
					//and keep tabs on rotation parameter. It will be sent off for POST.
					var img = document.createElement("img");
					$(img).attr("src", e.target.result);
					$(img).css("cursor", "pointer");
					$("#preview_img").html("");
					$("#preview_img").append(img);
					$("#rotate_instructions").css("display", "block");

					//Click handler for rotating image.
					$(img).click (function(){
						img_rotation= (img_rotation + 90) % 360;
						$(this).rotate(img_rotation);
						$("#id_img_rotation").attr("value", img_rotation);
					});
				}
				reader.readAsDataURL(this.files[0]);
    	}
		}
	});

	//Character Counters
	$("#id_tag_collar_info").keyup(function(){
		var count = PETREPORT_TAG_INFO_LENGTH - this.value.length;
		$("#id_tag_collar_info_count").html(count + " characters remaining");
	});
	
	//Character Counters
	$("#id_description").keyup(function(){
		var count = PETREPORT_DESCRIPTION_LENGTH - this.value.length;
		$("#id_description_count").html(count + " characters remaining");
	});		

	$("#id_submit").click(function(){
			var conditions = true;
			var issues = "Please fix the following fields before submitting this form: \n";
			var num_issues = 0;

			/*check for date value = null and date value in future*/
			if ($("#id_date_lost_or_found").attr("value")==""){
				conditions = false;
				issues += (++num_issues)+" . Please fill in the Date Lost/Found.\n";
			}

			else if ((new Date($("#id_date_lost_or_found").attr("value"))) > (new Date()) ){
				conditions = false;
				issues += "Please fill in a valid Date Lost/Found.\n";
			}

			if (img_size > 3.0) {
				conditions = false;				
				issues += (++num_issues)+". Image size should be less that 3MB.\n";
			}	

			if(conditions == true)
				document.forms['petreport_form'].submit();
			else
				alert(issues);
	});

	//Listen for a change in the pet type. If the user selects a pet type, load the breeds for that pet type!
	$("#id_pet_type").change(function(){
		var pet_type = this.value;
		load_pet_breeds(pet_type);
	});	

	//Toggle Display of Contact fields if Contact Box gets clicked.
	$("#contact-box").click(function(){
		toggle_display("id_contact_name");
		toggle_display("id_contact_number");
		toggle_display("id_contact_email");
		toggle_display("id_contact_link");		
	});

	$("#microchip-box").click(function(){
		toggle_display("id_microchip_id");
	});

	/******** Kick Things Off *********/
	load_pet_breeds(PET_TYPE, function(data){
    $("#id_breed").html("").select2({data: {id:null, text: null}});
    $("#id_breed").select2({ 
        tags: data.breeds,
        maximumSelectionSize:1,
    });
    if (PET_BREED != undefined)
    	$("#id_breed").val(PET_BREED).trigger("change");
	});

	//Grab Event Tags.
	perform_AJAX_call({
		type:"GET",
		url:REPORTING_URLS["EVENT_TAGS"],
		data: {},
		success: function(data){
			$("#id_event_tag").select2({
				tags: data.event_tags,
				placeholder:"Select Event Tag",
				maximumSelectionSize:1,
			});
		}
	});	

	//Required Red Markers for Labels.
	$("label[for=id_status]").append("<b class='required-field-symbol'>*</b>")
	$("label[for=id_date_lost_or_found]").append("<b class='required-field-symbol'>*</b>")
	$("label[for=id_pet_type]").append("<b class='required-field-symbol'>*</b>")

	//Reorganization of fields after render.
	$("#id_contact_name").parent(".form-group").appendTo("#contact-subform");
	$("#id_contact_number").parent(".form-group").appendTo("#contact-subform");
	$("#id_contact_email").parent(".form-group").appendTo("#contact-subform");
	$("#id_contact_link").parent(".form-group").appendTo("#contact-subform");
	toggle_display("id_contact_name");
	toggle_display("id_contact_number");
	toggle_display("id_contact_email");
	toggle_display("id_contact_link");	

	$("#label_id_geo_location_lat").remove();
	$("#label_id_geo_location_long").remove();
	$("#label_id_location").remove();
	$("#id_geo_location_lat").parent(".form-group").css("display", "inline-block").css("margin-right", "2.5px").attr("disabled", true).appendTo("#location-coordinates");
	$("#id_geo_location_long").parent(".form-group").css("display", "inline-block").css("margin-left", "2.5px").attr("disabled", true).appendTo("#location-coordinates");
	$("#id_location").parent(".form-group").appendTo("#location-coordinates");
	toggle_display("location-coordinates");
	toggle_display("location-map");

	$("#id_microchip_id").parent(".form-group").appendTo("#microchip-subform");
	$("#label_id_microchip_id").remove();
	toggle_display("id_microchip_id");

	var map;
	$("#location-box").click(function(){	
		toggle_display("location-coordinates");		
		toggle_display("location-map");	

		if (map != undefined)
			map.remove();

		map = new L.map('location-map').setView([PETREPORT_LOCATION_LAT, PETREPORT_LOCATION_LNG], 10);	
		L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6IjZjNmRjNzk3ZmE2MTcwOTEwMGY0MzU3YjUzOWFmNWZhIn0.Y8bhBaUMqFiPrDRW9hieoQ', {
			maxZoom: 18,
			attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
				'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
				'Imagery © <a href="http://mapbox.com">Mapbox</a>',
			id: 'mapbox.streets'
		}).addTo(map);	

		var markersLayer = new L.LayerGroup();
		map.addLayer(markersLayer);

		map.on("move", function(e){
			var latlng = map.getCenter();
			$("#id_geo_location_lat").val(latlng.lat);
			$("#id_geo_location_long").val(latlng.lng);
		});

		new L.Control.GeoSearch({
			provider: new L.GeoSearch.Provider.Google(),
			showMarker:false
		}).addTo(map);

		$("#leaflet-control-geosearch-qry").keyup(function(){
			$("#id_location").val($("#leaflet-control-geosearch-qry").val());
		})

		//Place marker when map click occurs.
		var marker;
		map.on('click', function(e){
			if (marker != null)
				map.removeLayer(marker);
			$("#id_geo_location_lat").val(e.latlng.lat);
			$("#id_geo_location_long").val(e.latlng.lng);
			marker = new L.Marker(e.latlng);
			map.addLayer(marker);
		});
	});

});

function toggle_display(field){
	$("#label_" + field).toggleClass("hidden");
	$("#" + field).toggleClass("hidden");
}















