		function saveProfile(){
			// alert("we shall now save your changes!");
			
	        /*an anonymous user shouldn't be able to acess the bookmarks page*/
	        if (user_id == "None"){
	            return false;
	        }
        	var csrf_value = $(".edit_profile_input_box input").attr("value");
	        email = $("#id_email").attr("value");
	        first_name = $("#id_first_name").attr("value");
	        last_name = $("#id_last_name").attr("value");
	        username = $("#id_username").attr("value");
	        /*ajax request to save the changes*/
	        $.ajax({

	          type:"POST",
	          url:URL_EDITUSERPROFILE,
	          data: {"csrfmiddlewaretoken":csrf_value, "action":"saveProfile","username":username,"first_name":first_name,"last_name":last_name,"email":email},
	          success: function(data){
	            	$(".edituserprofile_messages").html(data.message);
	            	return true;
	          },
	          error: function(data){
	              alert("An unexpected error occurred when trying to save your changes. Please try again."); 
	              return false;
	          }
	        });
	        return true;
		}
		function savePassword(){

			
	        /*an anonymous user shouldn't be able to acess the bookmarks page*/
	        if (user_id == "None"){
	            return false;
	        }
	        var csrf_value = $("#edit_profile_password input").attr("value");
	        old_password = $("#id_old_password").attr("value");
	        new_password = $("#id_new_password").attr("value");
	        confirm_password = $("#id_confirm_password").attr("value");       
	        /*ajax request to save the password changes*/
	        $.ajax({

	          type:"POST",
	          url:URL_EDITUSERPROFILE,
	          data: {"csrfmiddlewaretoken":csrf_value, "action":"savePassword","old_password":old_password,"new_password":new_password,"confirm_password":confirm_password},
	            success: function(data){
	            	
	            	$("#id_old_password").attr("value","");
	            	$("#id_new_password").attr("value","");
	            	$("#id_confirm_password").attr("value","");
	            	$(".edituserprofile_messages").html( data.message );
           	
	              return true;
	            },
	            error: function(data){
	              // alert("An unexpected error occurred when trying to save your changes. Please try again."); 
	              $(".edituserprofile_messages").html("<li class='error'>" + data.message + "</li>");
	              alert(message);
	              return false;
	            }
	        });
	        return true;
		}