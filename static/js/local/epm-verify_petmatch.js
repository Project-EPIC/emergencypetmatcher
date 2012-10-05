//This function uses the postIt j/s function to send a post request to the server to vevrify the petmatch
function post_user_response(response){
      var url = URL_VERIFY_PETMATCH+PETMATCH_ID+"/";
      var message =response;
      var csrf_value = $("input").attr("value");
      var data= {"csrfmiddlewaretoken":csrf_value, "message":message};
      postIt(url,data);
      // $.ajax({
      //     type:"POST",
      //     url:url,
      //     // async:false,
      //     data: {"csrfmiddlewaretoken":csrf_value, "message":message},
      //       success: function(data){
      //         alert("post success!");
      //         return true;
      //       },
      //       error: function(data){
      //         alert("An unexpected error occured."); 
      //         return false;
      //       }
      //   });
}