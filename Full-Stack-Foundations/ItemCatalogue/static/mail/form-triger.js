
$(document).ready(function() {
    $("#submit_btn").click(function() { 
       
	    var proceed = true;
        //simple validation at client's end
        //loop through each field and we simply change border color to red for invalid fields		
		$("#contact_form input[required=required]").each(function(){
			$(this).css('border-color',''); 
			if(!$.trim($(this).val())){ //if this field is empty 
				$(this).css('border-color','red'); //change border color to red   
				proceed = false; //set do not proceed flag
			}
			//check invalid email
			var email_reg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/; 
			if($(this).attr("type")=="email" && !email_reg.test($.trim($(this).val()))){
				$(this).css('border-color','red'); //change border color to red   
				proceed = false; //set do not proceed flag				
			}	
		});		
		
       
        if(proceed) //everything looks good! proceed...
        {
			//get input field values data to be sent to server
            post_data = {
				'user_fname'	: $('input[name=fname]').val(),
				'user_lphone'	: $('input[name=lname]').val(), 
				'user_email'	: $('input[name=email]').val(),
				'user_website'	: $('input[name=website]').val(), 
				'user_message'	: $('textarea[name=message]').val()
			};
            
            //Ajax post data to server
            $.post('mail/contact1.php', post_data, function(response){  
				if(response.type == 'error'){ //load json data from server and output message  
					output = '<div style="display:block;opacity:1;" class = "modal fade" id = "form" tabindex = "-1" role = "dialog" aria-labelledby = "myModalLabel" aria-hidden = "true"><div class = "listing-modal-1 modal-dialog"><div class = "modal-content"><div class = "modal-header"><a class="close" href="javascript:location.reload(true)">x</a><h4 class = "modal-title" id = "myModalLabel"> Ooops</h4></div><div class = "modal-body"><div class=" listing-message"><div class="error">'+response.text+'</div></div></div></div></div></div>';
				}else{
				    
					output = '<div style="display:block;opacity:1;" class = "modal fade" id = "form" tabindex = "-1" role = "dialog" aria-labelledby = "myModalLabel" aria-hidden = "true"><div class = "listing-modal-1 modal-dialog"><div class = "modal-content"><div class = "modal-header"><a class="close" href="javascript:location.reload(true)">x</a><h4 class = "modal-title" id = "myModalLabel"> Thank you</h4></div><div class = "modal-body"><div class=" listing-message"><div id="overlay_form" class="success">'+response.text+'</div></div></div></div></div></div>';
				
				}
				$("#contact_form #contact_results").hide().html(output).slideDown();
            }, 'json');
        }
    });
	
    
});