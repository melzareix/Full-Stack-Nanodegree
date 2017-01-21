// jQuery Initialization
jQuery(document).ready(function($){
"use strict"; 


        /* =================================
        ===  MAILCHIMP                 ====
        =================================== */

        $('.mailchimp').ajaxChimp({
            callback: mailchimpCallback,
            url: "http://designsvilla.us10.list-manage.com/subscribe/post?u=8d6fd5258003daa5d449677a9&amp;id=fb984af59f" //Replace this with your own mailchimp post URL. Don't remove the "". Just paste the url inside "".  
        });

        function mailchimpCallback(resp) {
             if (resp.result === 'success') {
                $('.subscription-success').html('<div class="modal" id="myModal" role="dialog"><div class="modal-dialog"><div class="modal-content"><div class="modal-header"><a class="close" href="javascript:location.reload(true)">x</a><h4 class="modal-title">THANK YOU!</h4></div><div class="modal-body"><div class="success">' + resp.msg+ '</div></div></div></div></div>').fadeIn(1000);
                //window.location.href="www.yourdomain.com";
				$('.subscription-error').fadeOut(500);
                
            } else if(resp.result === 'error') {
                $('.subscription-error').html('<div class="modal" id="myModal" role="dialog"><div class="modal-dialog"><div class="modal-content"><div class="modal-header"><a class="close" href="javascript:location.reload(true)">x</a><h4 class="modal-title">Ooops! !</h4></div><div class="modal-body"><div class="error">' + resp.msg + '</div></div></div></div></div>').fadeIn(1000);
            }  
        }



        //======================================================================================================
        //  END OF DOCUMENT
        //=================
});