

$(document).ready(function() {
    function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                 if (cookie.substring(0, name.length + 1) == (name + '=')) {
                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                     break;
                 }
             }
         }
         return cookieValue;
         }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    var upvote_button = $("#upvote_button");
    var prj_upvotes = $("#prj_upvotes");
    var voted = 0;

    upvote_button.click(function() {
        if (voted == 0) {
           $.ajax({
                type: "POST",
                url: '/upvote/',
                data: {'id': upvote_button.data()['projectId']},
                success: function(data) {
                    prj_upvotes.html(data['upvotes']);
                    upvote_button.html('Thank you for voting');
                    voted = 1;
                }
            });
        }

    });
});