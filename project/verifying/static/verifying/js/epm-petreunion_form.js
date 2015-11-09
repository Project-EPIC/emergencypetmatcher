$(document).ready(function(){

  //Required Red Markers for Labels.
  $("label[for=id_reason]").append("<b class='required-field-symbol'>*</b>")

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
});